#!/usr/bin/env python3
"""`./lkf test`: corre las pruebas del cambio actual en addons, modules y Sanic.

Corre en el HOST y lanza pytest en docker con el codigo local de los repos
montado (el cambio completo, aunque nada este mergeado). Se puede correr desde
addons o desde lkf-sanic-apps (su ./lkf test llama a este archivo).

Repos (Sanic es opcional: si ../lkf-sanic-apps no existe se omite):
  addons + modules                        back "addons": imagen linkaform/lkf_test:develop
  lkf-sanic-apps + sdk-modules-sanic      back "sanic":  imagen linkaform/sanic-app:test
                                          (cd lkf-sanic-apps && ./lkf build test)
La suite es la misma (sdk_testing); con LKF_BACK=sanic los tests reciben la
clase de Sanic en vez de la de addons (test/sdk_testing/lkf_back.py). Cada back
corre solo si alguno de sus repos tiene cambios (sin cambios en ningun repo:
corre addons, como antes).

Pasos (se detiene en el primero que falla en rojo):
  1. Detectar (bin/lkf_changes.py): funciones cambiadas en cada repo.
     modules / sdk-modules-sanic en rama de cuenta (seguridad, hergo...) ->
     tu checkout no se toca; se arma un worktree temporal (.lkf-test/<repo>-wt):
       - la rama que se llame igual que tu rama de trabajo (la de addons o
         la de lkf-sanic-apps), si existe (local o en origin): se evalua;
       - si no, origin/master: no lo tocaste, solo se usa para probar.
  2. Compilar los .py cambiados.                                    bloquea
  3. ruff --select E9,F63,F7,F82 en los .py cambiados.              bloquea
  4. pytest -m unit de unit/test_unit_cases.py de las secciones      bloquea
     tocadas, por back y suite. Cada test_unit_cases.py trae los
     unitarios principales de la seccion (maximo 10) y en C10_TRIGGERS las
     funciones que la disparan. Los demas archivos de unit/ no corren aqui.
     Ante la duda corren todas las secciones (ver unit_plan); en Sanic no:
     solo las que tienen trigger. Un test que usa un metodo que Sanic no
     tiene sale SKIPPED y se avisa.
  5. pytest --target=<funciones> -m "not unit" (integration/prod_test de las
     funciones cambiadas, cada back con las suyas) contra la cuenta activa,
     que debe ser la 10 (./lkf workwith seguridad). Si no, PENDIENTE. bloquea
  Funciones cambiadas sin ningun test con su target -> aviso.

El resultado se guarda en .lkf-test/<shas>.json y se publica
(bin/lkf_publish.py): status lkf-test + comentario en el PR de cada repo con
cambios. Si algun SHA no esta pusheado, haz push y luego
`./lkf test --publicar`, que sube el resultado guardado sin volver a correr.
`--no-publicar` corre sin tocar GitHub.
"""
import argparse
import ast
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import lkf_changes  # noqa: E402
import lkf_publish  # noqa: E402

IMAGE = {"addons": "linkaform/lkf_test:develop", "sanic": "linkaform/sanic-app:test"}
SP = "/usr/local/lib/python3.12/site-packages"
SANIC = "/srv/lkf-sanic-app"
TEST_ACCOUNT = 10
RUFF_RULES = "E9,F63,F7,F82"
TRIGGERS_FILE = "test_unit_cases.py"
REPOS = ("addons", "modules", "lkf-sanic-apps", "sdk-modules-sanic")
CHILD = {"modules": "addons", "sdk-modules-sanic": "lkf-sanic-apps"}   # repo de modulos -> su repo
BACK = lkf_changes.BACK


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


class Runner:
    def __init__(self, a, paths):
        self.sdk, self.env, self.paths = a.sdk, a.env_from, paths
        api = os.path.join(os.path.dirname(self.env), "linkaform_api", "linkaform_api")
        repo_mounts = [(p, f"/srv/repo/{name}") for name, p in paths.items()]
        self.mounts = {"addons": [
            (os.path.join(self.env, "secrets/lkf_jwt_key.pub"), "/etc/ssl/certs/lkf_jwt_key.pub"),
            (api, f"{SP}/linkaform_api"),
            (os.path.join(paths["addons"], "lkf_addons"), f"{SP}/lkf_addons"),
            (paths["modules"], f"{SP}/lkf_modules"),
            (self.sdk, "/srv/lkf_test/sdk_testing"),
            (os.path.join(self.env, "config"), "/srv/scripts/addons/config"),
            (os.path.join(self.env, "secrets"), "/srv/scripts/addons/secrets"),
            *repo_mounts,
        ]}
        if "lkf-sanic-apps" in paths:
            # Igual que lkf-sanic-app en el docker-compose de clave10-sdk.
            sanic = paths["lkf-sanic-apps"]
            self.mounts["sanic"] = [
                (os.path.join(sanic, "addons"), f"{SP}/lkf_addons"),
                (api, f"{SP}/linkaform_api"),
                (os.path.join(sanic, "app"), f"{SANIC}/app"),
                (paths["sdk-modules-sanic"], f"{SANIC}/app/modules"),
                (os.path.join(sanic, "app", "config"), f"{SANIC}/config"),
                (os.path.join(sanic, "secrets"), f"{SANIC}/secrets"),
                (os.path.join(self.env, "secrets"), "/srv/addons/secrets"),
                (paths["modules"], "/srv/repo/modules"),   # accesos_testing.py (lkf_back.py)
                (self.sdk, "/srv/lkf_test/sdk_testing"),
            ]

    def docker(self, workdir, *cmd, back="addons"):
        args = ["docker", "run", "--rm", "-w", workdir]
        if back == "sanic":
            args += ["-e", "LKF_BACK=sanic", "-e", "USE_LOCAL_SETTINGS=1"]
        for src, dst in self.mounts[back]:
            args += ["-v", f"{os.path.realpath(src)}:{dst}"]
        return sh(args + [IMAGE[back], *cmd])

    def has_image(self, back):
        return sh(["docker", "image", "inspect", IMAGE[back]]).returncode == 0

    def suites(self):
        """Carpetas de sdk_testing con pytest.ini propio (accesos, ...)."""
        return sorted(
            d for d in os.listdir(self.sdk)
            if not d.startswith(("_", ".")) and os.path.isfile(os.path.join(self.sdk, d, "pytest.ini"))
        )

    def unit_sections(self, suite):
        """{seccion: C10_TRIGGERS (set) o None} de las secciones con unitarios en unit/."""
        out = {}
        for d in sorted(os.listdir(os.path.join(self.sdk, suite))):
            unit = os.path.join(self.sdk, suite, d, "unit")
            if d.startswith(("_", ".")) or not os.path.isdir(unit):
                continue
            if not any(f.endswith(".py") and (f.startswith("test_") or f.endswith("_test.py"))
                       for _, _, files in os.walk(unit) for f in files):
                continue
            out[d] = read_triggers(os.path.join(unit, TRIGGERS_FILE))
        return out

    def pytest(self, back, suite, *args):
        res = self.docker(
            f"/srv/lkf_test/sdk_testing/{suite}",
            "pytest", "-p", "no:cacheprovider", "-p", "no:warnings", "-q", "-o", "log_cli=false", *args,
            back=back,
        )
        tail = [l for l in res.stdout.strip().splitlines() if l.strip()]
        return res.returncode, (tail[-1] if tail else res.stderr.strip()[-300:]), res.stdout

    def active_account(self):
        res = self.docker(
            "/srv/scripts/addons", "python", "-c",
            "import sys; sys.path.insert(0,'config'); from account_settings import settings; "
            "print(settings.config.get('ACCOUNT_ID'))",
        )
        try:
            return int(res.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            return None


FALTA_SANIC = re.compile(r"^SKIPPED \[\d+\] .*?: falta en sanic: (\w+)", re.M)


UNIT_STATES = {"PASSED": "passed", "FAILED": "failed", "ERROR": "error",
               "SKIPPED": "skipped", "XFAIL": "xfailed", "XPASS": "xpassed"}


def unit_by_section(out):
    """{seccion: {"passed": n, "failed": n, ...}} desde el resumen de `pytest -rA`.

    Lineas: "PASSED notas/x_test.py::test_y", "FAILED notas/x.py::t - msg",
    "SKIPPED [1] notas/x.py:12: razon". La seccion es la primera carpeta.
    """
    secs = {}
    for line in out.splitlines():
        word, _, rest = line.partition(" ")
        if word not in UNIT_STATES:
            continue
        if word == "SKIPPED":
            rest = rest.split("] ", 1)[-1].split(":", 1)[0]
        path = rest.split("::", 1)[0].split(" ", 1)[0]
        sec = path.split("/", 1)[0] if "/" in path else "(raiz)"
        counts = secs.setdefault(sec, {})
        counts[UNIT_STATES[word]] = counts.get(UNIT_STATES[word], 0) + 1
    return secs


def read_triggers(path):
    """La lista C10_TRIGGERS de un test_unit_cases.py (sin importarlo); None si no hay."""
    try:
        with open(path) as fh:
            tree = ast.parse(fh.read())
    except (OSError, SyntaxError):
        return None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "C10_TRIGGERS" for t in node.targets):
            try:
                return set(ast.literal_eval(node.value))
            except ValueError:
                return None
    return None


def module_of(path):
    """Modulo de un archivo cambiado: lkf_addons/addons/accesos/app.py (addons),
    addons/accesos/service.py (lkf-sanic-apps) y accesos/items/scripts/...
    (modules, sdk-modules-sanic) -> accesos."""
    parts = path.split("/")
    if parts[:2] == ["lkf_addons", "addons"] and len(parts) > 2:
        return parts[2]
    if parts[0] == "addons" and len(parts) > 2:
        return parts[1]
    return parts[0]


def unit_plan(suite, suites, triggers, changed, sueltos, solo_triggers=False):
    """(secciones a correr, avisos) de los unitarios de una suite.

    triggers: {seccion: C10_TRIGGERS o None}, de Runner.unit_sections.
    changed: {funcion: rutas de lkf_changes ("app.py", "x.py (eliminada)", ...)}.
    sueltos: .py cambiados fuera de cualquier funcion.

    Corren las secciones cuya lista trae alguna funcion cambiada. Si hay duda
    se corren todas (secciones = None): una funcion del modulo que no esta en
    ninguna lista, una de un modulo sin suite propia (base, ...), un .py
    cambiado fuera de una funcion, o ninguna funcion cambiada.

    solo_triggers (back sanic): la duda no corre todo, solo avisa. Sanic aun no
    tiene todo lo de addons (falta buscador facets, auto-activacion...): correr
    todas las secciones dejaria rojo cualquier PR por secciones que no toco.
    """
    avisos, todo, secs = [], False, set()
    sin_lista = sorted(s for s, t in triggers.items() if t is None)
    if sin_lista:
        avisos.append(f"sin {TRIGGERS_FILE} con C10_TRIGGERS (./lkf test no corre sus unitarios): "
                      + ", ".join(sin_lista))
    if not changed and not sueltos:
        return ([] if solo_triggers else None), avisos
    for fn, whys in sorted(changed.items()):
        mods = {module_of(w.split(" (", 1)[0]) for w in whys}
        hit = {s for s, t in triggers.items() if t and fn in t}
        if hit and all(w.endswith("(eliminada)") for w in whys):
            avisos.append(f"{fn} ya no existe y sigue en C10_TRIGGERS de: " + ", ".join(sorted(hit)))
        if hit:
            secs |= hit
        elif suite in mods:
            avisos.append(f"{fn} no esta en ningun C10_TRIGGERS de {suite}: corren todas las secciones")
            todo = True
        elif not mods & set(suites):
            avisos.append(f"{fn} es de {', '.join(sorted(mods))} (sin suite propia): corren todas las secciones")
            todo = True
    for p in sueltos:
        if module_of(p) == suite or module_of(p) not in suites:
            avisos.append(f"{p}: cambio fuera de una funcion, corren todas las secciones")
            todo = True
    if solo_triggers and todo:
        avisos = [a.replace("corren todas las secciones", "sin seccion, en Sanic no se corren las demas") for a in avisos]
        todo = False
    return (None if todo else sorted(secs)), avisos


def sdk_behind(sdk):
    sh(["git", "-C", sdk, "fetch", "-q", "origin", "master"])
    out = sh(["git", "-C", sdk, "rev-list", "--count", "HEAD..origin/master"]).stdout.strip()
    return int(out or 0)


def branch_of(repo):
    return sh(["git", "-C", repo, "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()


def account_branch(repo):
    """Nombre de la rama si es de cuenta (sin '/', no master); si no, None."""
    br = branch_of(repo)
    return br if br and "/" not in br and br not in ("master", "HEAD") else None


def sibling_ref(repo, branch):
    """La rama de `repo` que se llama igual que la de trabajo: local, en origin o None."""
    if not branch or "/" not in branch:
        return None
    for ref in (f"refs/heads/{branch}", f"refs/remotes/origin/{branch}"):
        if sh(["git", "-C", repo, "rev-parse", "-q", "--verify", ref]).returncode == 0:
            return ref
    return None


def layout(a):
    """{repo: ruta} de los repos que existen (Sanic es opcional)."""
    paths = {"addons": a.addons, "modules": a.modules,
             "lkf-sanic-apps": a.sanic, "sdk-modules-sanic": a.sanic_modules}
    return {k: v for k, v in paths.items() if v and os.path.exists(os.path.join(v, ".git"))}


def work_branch(paths):
    """La rama de trabajo (con '/'): la de addons o, si no, la de lkf-sanic-apps."""
    for name in ("addons", "lkf-sanic-apps"):
        if name in paths and "/" in branch_of(paths[name]):
            return branch_of(paths[name])
    return None


def child_target(paths, name, work):
    """(ref a probar, rama de cuenta) si el repo de modulos esta en rama de cuenta; si no (None, None)."""
    cuenta = account_branch(paths[name])
    if not cuenta:
        return None, None
    return sibling_ref(paths[name], work) or "origin/master", cuenta


def tested_shas(paths):
    """SHA que se prueba de cada repo (ver child_target), en el orden de REPOS."""
    work = work_branch(paths)
    out = []
    for name in REPOS:
        if name not in paths:
            continue
        ref = child_target(paths, name, work)[0] if name in CHILD else None
        out.append(sh(["git", "-C", paths[name], "rev-parse", ref or "HEAD"]).stdout.strip())
    return out


def result_path(addons, shas):
    return os.path.join(addons, ".lkf-test", "_".join(x[:8] for x in shas) + ".json")


def do_publish(out):
    try:
        _, msgs = lkf_publish.publish(out)
    except RuntimeError as exc:
        msgs = [f"x fallo al publicar: {exc}"]
    print("\npublicacion:")
    for m in msgs:
        print(f"  {m}")


def publish_saved(a, paths):
    shas = tested_shas(paths)
    path = result_path(a.addons, shas)
    if not os.path.exists(path):
        print(f"x no hay resultado para {' / '.join(x[:8] for x in shas)}: corre ./lkf test primero")
        return 2
    with open(path) as fh:
        out = json.load(fh)
    print(f"publicando {os.path.relpath(path, a.addons)} ({out['veredicto']})")
    do_publish(out)
    return 0


def main():
    here = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sanic = os.path.join(os.path.dirname(here), "lkf-sanic-apps")
    ap = argparse.ArgumentParser(description="Pruebas del cambio actual (addons, modules y Sanic)")
    ap.add_argument("--addons", default=here)
    ap.add_argument("--modules", default=os.path.join(here, "modules"))
    ap.add_argument("--sanic", default=sanic, help="repo lkf-sanic-apps (si no existe, se omite Sanic)")
    ap.add_argument("--sanic-modules", default=os.path.join(sanic, "app", "modules"))
    ap.add_argument("--sdk", default=os.path.join(here, "test", "sdk_testing"))
    ap.add_argument("--env-from", default=here, help="addons de donde salen config/ y secrets/")
    ap.add_argument("--publicar", action="store_true", help="solo publica el resultado guardado de los SHAs actuales")
    ap.add_argument("--no-publicar", action="store_true", help="corre sin publicar en GitHub")
    a = ap.parse_args()
    paths = layout(a)
    if a.publicar:
        return publish_saved(a, paths)

    work = work_branch(paths)
    notes, worktrees = {}, []
    try:
        for name in CHILD:
            if name not in paths or not account_branch(paths[name]):
                continue
            real = paths[name]
            sh(["git", "-C", real, "fetch", "-q", "origin"])
            ref, cuenta = child_target(paths, name, work)
            tmp = os.path.join(a.addons, ".lkf-test", f"{name}-wt")
            sh(["git", "-C", real, "worktree", "remove", "--force", tmp])
            sh(["git", "-C", real, "worktree", "prune"])
            if ref.startswith("refs/heads/"):        # rama hermana local: se usa tal cual
                cmd = ["worktree", "add", "-q", tmp, ref[len("refs/heads/"):]]
            elif ref.startswith("refs/remotes/"):    # solo en origin: rama local que la sigue
                cmd = ["worktree", "add", "-q", "--track", "-b", ref[len("refs/remotes/origin/"):], tmp, ref]
            else:                                    # sin rama hermana: origin/master
                cmd = ["worktree", "add", "-q", "--detach", tmp, "origin/master"]
            res = sh(["git", "-C", real, *cmd])
            if res.returncode:
                print(f"x no se pudo preparar {name} ({ref}) en un worktree: {res.stderr.strip()}")
                return 2
            worktrees.append((real, tmp))
            paths[name] = tmp
            notes[name] = (cuenta, ref)
        return run_all(a, paths, notes, work)
    finally:
        for real, tmp in worktrees:
            sh(["git", "-C", real, "worktree", "remove", "--force", tmp])


CODE_PREFIX = {"addons": "lkf_addons/", "lkf-sanic-apps": "addons/"}


def changed(r):
    """El repo trae cambios que prueba sdk_testing (no tooling como lkf, docker/, bin/)."""
    if any(r[k] for k in ("funciones", "rotos", "eliminados", "sin_funcion")):
        return True
    prefix = CODE_PREFIX.get(r["repo"], "")
    return any(p.startswith(prefix) for p in r["sin_tests"])


def run_all(a, paths, notes, work):
    run = Runner(a, paths)
    steps, t0 = [], time.time()

    def step(name, state, detail=""):
        icon = {"ok": "✓", "rojo": "✗", "pendiente": "…", "aviso": "!", "omitido": "-"}[state]
        print(f"  {icon} {name:28s} {detail}")
        steps.append({"paso": name, "estado": state, "detalle": detail})

    # 1. detectar
    heads = {k: "HEAD" for k in paths}
    repos = []
    for name, path in paths.items():
        cuenta, ref = notes.get(name, (None, None))
        if ref == "origin/master":   # rama de cuenta sin rama hermana: no se evalua
            sha = sh(["git", "-C", path, "rev-parse", "HEAD"]).stdout.strip()
            repos.append({"repo": name, "ruta": path, "ok": True, "rama": f"origin/master (tu checkout: {cuenta})",
                          "sha": sha, "base": sha, "sin_commit": False, "funciones": {}, "sin_tests": [],
                          "rotos": [], "eliminados": [], "sin_funcion": []})
            continue
        sh(["git", "-C", path, "fetch", "-q", "origin", "master"])
        repos.append(lkf_changes.analyze(path, name, paths, heads))
    lkf_changes.print_human(repos)
    print()
    for name, (cuenta, ref) in notes.items():
        if ref == "origin/master":
            step(name, "aviso", f"tu checkout esta en '{cuenta}' (rama de cuenta) y no hay rama "
                 f"'{work or CHILD[name]}' en {name}: no se evalua y se prueba con origin/master")
        else:
            step(name, "aviso", f"tu checkout esta en '{cuenta}' (rama de cuenta): se evalua la rama "
                 f"hermana {ref.replace('refs/remotes/', '').replace('refs/heads/', '')} en un worktree temporal")
    for r in repos:
        if not r["ok"]:
            print(f"✗ {r['repo']} {r['error']}.")
            if r.get("ayuda"):
                print("\n" + r["ayuda"])
            print("\nNo se corrieron pruebas ni se publico nada.")
            return 2
        if r["sin_commit"]:
            step(f"{r['repo']}: sin commit", "aviso", "lo no commiteado no cuenta para el status")
    targets = sorted({fn for r in repos for fn in r["funciones"]})
    changed_py = [
        (r["repo"], p)
        for r in repos
        for p in lkf_changes.changed_lines(r["ruta"], r["base"], "HEAD")
        if p.endswith(".py") and os.path.exists(os.path.join(r["ruta"], p))
    ]
    # Que back corre: el de los repos con cambios; sin cambios en ninguno, addons.
    backs = [b for b in ("addons", "sanic") if any(changed(r) for r in repos if BACK[r["repo"]] == b)] or ["addons"]
    by_back = {b: [r for r in repos if BACK[r["repo"]] == b] for b in backs}

    behind = sdk_behind(a.sdk)
    if behind:
        step("sdk_testing", "aviso", f"{behind} commits atras de origin/master: corres tests viejos")

    def finish(code):
        verdict = {0: "verde", 1: "rojo", 3: "pendiente"}[code]
        # pytest corre sobre el arbol de trabajo; el status va sobre HEAD. Con
        # cambios sin commit lo probado no es lo commiteado: no se publica.
        out = {
            "veredicto": verdict, "repos": repos, "targets": targets, "pasos": steps,
            "segundos": round(time.time() - t0),
            "publicable": not any(r["sin_commit"] for r in repos),
        }
        os.makedirs(os.path.join(a.addons, ".lkf-test"), exist_ok=True)
        path = result_path(a.addons, [r["sha"] for r in repos])
        with open(path, "w") as fh:
            json.dump(out, fh, indent=2, ensure_ascii=False)
        print(f"\n== {verdict.upper()} ({out['segundos']} s)  -> {os.path.relpath(path, a.addons)}")
        if not a.no_publicar:
            do_publish(out)
        return code

    # 2. compilar
    rotos = [x for r in repos for x in r["rotos"]]
    if rotos:
        step("compilar", "rojo", "; ".join(f"{x['archivo']}: {x['error']}" for x in rotos))
        return finish(1)
    step("compilar", "ok", f"{len(changed_py)} .py cambiados")

    # 3. ruff (en la imagen de addons para todos los repos: es analisis estatico)
    if changed_py:
        # Bloquea solo errores en lineas que cambiaste: master ya trae ~140 F821
        # y conflictos sin resolver; revisar archivos completos dejaria rojo
        # cualquier PR que toque app.py. Lo viejo del archivo sale como aviso.
        lines = {f"/srv/repo/{r['repo']}/{p}": info["new"]
                 for r in repos
                 for p, info in lkf_changes.changed_lines(r["ruta"], r["base"], "HEAD").items()}
        files = [f"/srv/repo/{repo}/{p}" for repo, p in changed_py]
        res = run.docker("/srv/repo", "sh", "-c",
                         "command -v ruff >/dev/null || exit 127; "
                         f"ruff check -q --output-format json --select {RUFF_RULES} \"$@\"",
                         "ruff", *files)
        if res.returncode == 127:
            step("ruff", "aviso", "no esta en la imagen: ./lkf -p build test (requires.txt ya lo trae)")
        else:
            try:
                found = json.loads(res.stdout or "[]")
            except json.JSONDecodeError:
                found = [{"filename": "?", "location": {"row": 0}, "code": "ruff", "message": res.stdout[:300]}]
            mine = [e for e in found if e["location"]["row"] in lines.get(e["filename"], ())]
            fmt = lambda e: (f"{e['filename'].replace('/srv/repo/', '')}:{e['location']['row']} "
                             f"{e['code']} {e['message']}")
            if mine:
                step("ruff", "rojo", "; ".join(fmt(e) for e in mine)[:800])
                return finish(1)
            step("ruff", "ok", f"{RUFF_RULES} en lineas cambiadas")
            if found:
                step("ruff (ya en master)", "aviso",
                     f"{len(found)} en los archivos tocados, fuera de tus lineas; ej. {fmt(found[0])}"[:300])
    else:
        step("ruff", "omitido", "sin .py cambiados")

    pending = False
    if "sanic" in backs and not run.has_image("sanic"):
        step("sanic", "pendiente", f"falta la imagen {IMAGE['sanic']}: cd lkf-sanic-apps && ./lkf build test")
        backs.remove("sanic")
        pending = True

    # 4. unit: el test_unit_cases.py de las secciones cuyo C10_TRIGGERS trae
    # una funcion cambiada (ver unit_plan), en una sola corrida por suite y
    # back (cada corrida paga ~15 s de arranque de Accesos); el resultado se
    # reparte por seccion con -rA.
    for back in backs:
        tag = "" if back == "addons" else "sanic "
        changed_fns = {}
        for r in by_back[back]:
            for fn, whys in r["funciones"].items():
                changed_fns.setdefault(fn, set()).update(whys)
        sueltos = [p for r in by_back[back] for p in r["sin_funcion"]]
        for suite in run.suites():
            triggers = run.unit_sections(suite)
            secs, avisos = unit_plan(suite, run.suites(), triggers, changed_fns, sueltos,
                                     solo_triggers=(back == "sanic"))
            for msg in avisos:
                step(f"unit {tag}{suite}", "aviso", msg)
            if secs is None:
                secs = sorted(s for s, t in triggers.items() if t is not None)
            if not secs:
                step(f"unit {tag}{suite}", "omitido", "ninguna seccion tocada")
                continue
            code, summary, out = run.pytest(
                back, suite, "-m", "unit", "-rA", *[f"{s}/unit/{TRIGGERS_FILE}" for s in secs])
            secciones = unit_by_section(out)
            if code not in (0, 5) and not secciones:
                step(f"unit {tag}{suite}", "rojo", summary)
                print(out[-3000:])
                return finish(1)
            for sec, counts in sorted(secciones.items()):
                detail = ", ".join(f"{n} {k}" for k, n in counts.items())
                state = "rojo" if counts.get("failed") or counts.get("error") else "ok"
                step(f"unit {tag}{suite}/{sec}", state, detail)
            faltan = sorted(set(FALTA_SANIC.findall(out)))
            if faltan:
                step(f"unit {tag}{suite}", "aviso", "falta en sanic (tests saltados): " + ", ".join(faltan))
            no_aplica = [s for s, t in triggers.items() if t is not None and s not in secs]
            if no_aplica:
                step(f"unit {tag}{suite}", "omitido", "no aplica: " + ", ".join(no_aplica))
            if code not in (0, 5):
                print(out.split("short test summary info")[0][-3000:])
                return finish(1)

    # 5. target (integration / prod_test), cada back con sus funciones
    if not targets:
        step("target", "omitido", "sin funciones cambiadas")
        return finish(3 if pending else 0)

    def covered(out):
        for line in out.splitlines():
            if line.startswith("LKF_TARGETS_CUBIERTOS="):
                return {t for t in line.split("=", 1)[1].split(",") if t}
        return set()

    account = None
    for back in backs:
        tag = "" if back == "addons" else "sanic "
        fns = sorted({fn for r in by_back[back] for fn in r["funciones"]})
        if not fns:
            continue
        all_covered, plan = set(), {}
        for suite in run.suites():
            _, _, out = run.pytest(back, suite, "--collect-only", f"--target={','.join(fns)}")
            all_covered |= covered(out)
            code, _, out = run.pytest(back, suite, "--collect-only", f"--target={','.join(fns)}", "-m", "not unit")
            plan[suite] = code
        no_tests = [fn for fn in fns if fn not in all_covered]
        if no_tests:
            step(f"sin tests {tag}".strip(), "aviso", ", ".join(no_tests))
        for suite in run.suites():
            if plan[suite] == 5:
                step(f"target {tag}{suite}", "omitido", "sin integration/prod_test para estas funciones")
                continue
            if account is None:
                account = run.active_account()
            if account != TEST_ACCOUNT:
                step(f"target {tag}{suite}", "pendiente",
                     f"cuenta activa {account}, se requiere {TEST_ACCOUNT}: ./lkf workwith seguridad")
                pending = True
                continue
            code, summary, out = run.pytest(
                back, suite, f"--target={','.join(fns)}", "-m", "not unit", "--allow-prod-integration")
            if code not in (0, 5):
                step(f"target {tag}{suite}", "rojo", summary)
                print(out[-3000:])
                return finish(1)
            step(f"target {tag}{suite}", "ok", summary)
    return finish(3 if pending else 0)


if __name__ == "__main__":
    sys.exit(main())
