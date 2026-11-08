#!/usr/bin/env python3
"""`./lkf test`: corre las pruebas del cambio actual en addons + modules.

Corre en el HOST y lanza pytest en la imagen linkaform/lkf_test:develop con el
codigo local de los dos repos montado (el cambio completo, aunque nada este
mergeado).

Pasos (se detiene en el primero que falla en rojo):
  1. Detectar (bin/lkf_changes.py): funciones cambiadas en addons y modules.
     Un repo en rama de cuenta -> se detiene (cambia a fix/... o master).
  2. Compilar los .py cambiados.                                    bloquea
  3. ruff --select E9,F63,F7,F82 en los .py cambiados.              bloquea
  4. pytest -m unit (todos los unit de sdk_testing).                bloquea
  5. pytest --target=<funciones> -m "not unit" (integration/prod_test de las
     funciones cambiadas) contra la cuenta activa, que debe ser la 10
     (./lkf workwith seguridad). Si no es la 10 queda PENDIENTE.     bloquea
  Funciones cambiadas sin ningun test con su target -> aviso.

El resultado se guarda en .lkf-test/<sha_addons>_<sha_modules>.json y se
publica (bin/lkf_publish.py): status lkf-test + comentario en el PR de cada
repo con cambios. Si algun SHA no esta pusheado, haz push y luego
`./lkf test --publicar`, que sube el resultado guardado sin volver a correr.
`--no-publicar` corre sin tocar GitHub.
"""
import argparse
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import lkf_changes  # noqa: E402
import lkf_publish  # noqa: E402

IMAGE = "linkaform/lkf_test:develop"
SP = "/usr/local/lib/python3.12/site-packages"
TEST_ACCOUNT = 10
RUFF_RULES = "E9,F63,F7,F82"


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


class Runner:
    def __init__(self, a):
        self.addons, self.modules, self.sdk, self.env = a.addons, a.modules, a.sdk, a.env_from
        api = os.path.join(os.path.dirname(self.env), "linkaform_api", "linkaform_api")
        self.mounts = [
            (os.path.join(self.env, "secrets/lkf_jwt_key.pub"), "/etc/ssl/certs/lkf_jwt_key.pub"),
            (api, f"{SP}/linkaform_api"),
            (os.path.join(self.addons, "lkf_addons"), f"{SP}/lkf_addons"),
            (self.modules, f"{SP}/lkf_modules"),
            (self.sdk, "/srv/lkf_test/sdk_testing"),
            (os.path.join(self.env, "config"), "/srv/scripts/addons/config"),
            (os.path.join(self.env, "secrets"), "/srv/scripts/addons/secrets"),
            (self.addons, "/srv/repo/addons"),
            (self.modules, "/srv/repo/modules"),
        ]

    def docker(self, workdir, *cmd):
        args = ["docker", "run", "--rm", "-w", workdir]
        for src, dst in self.mounts:
            args += ["-v", f"{os.path.realpath(src)}:{dst}"]
        return sh(args + [IMAGE, *cmd])

    def suites(self):
        """Carpetas de sdk_testing con pytest.ini propio (accesos, ...)."""
        return sorted(
            d for d in os.listdir(self.sdk)
            if not d.startswith(("_", ".")) and os.path.isfile(os.path.join(self.sdk, d, "pytest.ini"))
        )

    def pytest(self, suite, *args):
        res = self.docker(
            f"/srv/lkf_test/sdk_testing/{suite}",
            "pytest", "-p", "no:cacheprovider", "-p", "no:warnings", "-q", "-o", "log_cli=false", *args,
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


def sdk_behind(sdk):
    sh(["git", "-C", sdk, "fetch", "-q", "origin", "master"])
    out = sh(["git", "-C", sdk, "rev-list", "--count", "HEAD..origin/master"]).stdout.strip()
    return int(out or 0)


def result_path(addons, sha_a, sha_m):
    return os.path.join(addons, ".lkf-test", f"{sha_a[:8]}_{sha_m[:8]}.json")


def do_publish(out):
    try:
        _, msgs = lkf_publish.publish(out)
    except RuntimeError as exc:
        msgs = [f"x fallo al publicar: {exc}"]
    print("\npublicacion:")
    for m in msgs:
        print(f"  {m}")


def publish_saved(a):
    shas = [sh(["git", "-C", r, "rev-parse", "HEAD"]).stdout.strip() for r in (a.addons, a.modules)]
    path = result_path(a.addons, *shas)
    if not os.path.exists(path):
        print(f"x no hay resultado para {shas[0][:8]} / {shas[1][:8]}: corre ./lkf test primero")
        return 2
    with open(path) as fh:
        out = json.load(fh)
    print(f"publicando {os.path.relpath(path, a.addons)} ({out['veredicto']})")
    do_publish(out)
    return 0


def main():
    here = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    ap = argparse.ArgumentParser(description="Pruebas del cambio actual (addons + modules)")
    ap.add_argument("--addons", default=here)
    ap.add_argument("--modules", default=os.path.join(here, "modules"))
    ap.add_argument("--sdk", default=os.path.join(here, "test", "sdk_testing"))
    ap.add_argument("--env-from", default=here, help="addons de donde salen config/ y secrets/")
    ap.add_argument("--publicar", action="store_true", help="solo publica el resultado guardado de los SHAs actuales")
    ap.add_argument("--no-publicar", action="store_true", help="corre sin publicar en GitHub")
    a = ap.parse_args()
    if a.publicar:
        return publish_saved(a)
    run = Runner(a)
    steps, t0 = [], time.time()

    def step(name, state, detail=""):
        icon = {"ok": "✓", "rojo": "✗", "pendiente": "…", "aviso": "!", "omitido": "-"}[state]
        print(f"  {icon} {name:28s} {detail}")
        steps.append({"paso": name, "estado": state, "detalle": detail})

    # 1. detectar
    for r in (a.addons, a.modules):
        sh(["git", "-C", r, "fetch", "-q", "origin", "master"])
    heads = {"addons": "HEAD", "modules": "HEAD"}
    repos = [
        lkf_changes.analyze(a.addons, "addons", a.addons, a.modules, heads),
        lkf_changes.analyze(a.modules, "modules", a.addons, a.modules, heads),
    ]
    lkf_changes.print_human(repos)
    print()
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
        path = result_path(a.addons, repos[0]["sha"], repos[1]["sha"])
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

    # 3. ruff
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

    # 4. unit
    for suite in run.suites():
        code, summary, out = run.pytest(suite, "-m", "unit")
        if code not in (0, 5):
            step(f"unit {suite}", "rojo", summary)
            print(out[-3000:])
            return finish(1)
        step(f"unit {suite}", "ok", summary)

    # 5. target (integration / prod_test)
    if not targets:
        step("target", "omitido", "sin funciones cambiadas")
        return finish(0)
    def covered(out):
        for line in out.splitlines():
            if line.startswith("LKF_TARGETS_CUBIERTOS="):
                return {t for t in line.split("=", 1)[1].split(",") if t}
        return set()

    pending, all_covered, plan = False, set(), {}
    for suite in run.suites():
        _, _, out = run.pytest(suite, "--collect-only", f"--target={','.join(targets)}")
        all_covered |= covered(out)
        code, _, out = run.pytest(suite, "--collect-only", f"--target={','.join(targets)}", "-m", "not unit")
        plan[suite] = code
    no_tests = [fn for fn in targets if fn not in all_covered]
    if no_tests:
        step("sin tests", "aviso", ", ".join(no_tests))

    account = run.active_account()
    for suite in run.suites():
        if plan[suite] == 5:
            step(f"target {suite}", "omitido", "sin integration/prod_test para estas funciones")
            continue
        if account != TEST_ACCOUNT:
            step(f"target {suite}", "pendiente",
                 f"cuenta activa {account}, se requiere {TEST_ACCOUNT}: ./lkf workwith seguridad")
            pending = True
            continue
        code, summary, out = run.pytest(
            suite, f"--target={','.join(targets)}", "-m", "not unit", "--allow-prod-integration")
        if code not in (0, 5):
            step(f"target {suite}", "rojo", summary)
            print(out[-3000:])
            return finish(1)
        step(f"target {suite}", "ok", summary)
    return finish(3 if pending else 0)


if __name__ == "__main__":
    sys.exit(main())
