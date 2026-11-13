#!/usr/bin/env python3
"""Detecta que funciones cambiaron en addons, modules y Sanic contra origin/master.

Es la primera pieza de `./lkf test`: de aqui salen los `--target=` de pytest y
el resumen que se publica en cada PR. Corre en el HOST (necesita git real de
los dos repos; dentro del contenedor el .git de modules no esta montado).

Por repo:
  - Base = merge-base(origin/master, HEAD), igual que un PR: lo que entro a
    master despues de abrir tu rama no cuenta como cambio tuyo.
  - Se compara HEAD (lo commiteado), no el arbol de trabajo: el status se
    publica sobre un SHA, asi que lo no commiteado no puede contar. Si hay
    cambios sin commit se avisa.
  - Solo ramas de trabajo (con "/": fix/..., feat/...) o master. Las ramas de
    cuenta (account_126, seguridad, chubb...) no llevan "/" y se rechazan: ahi
    el diff contra master trae todo lo propio de la cuenta, no tu cambio.

Que cuenta como funcion cambiada:
  - Cualquier .py: los def (funciones o metodos) que tocan lineas cambiadas.
    Se reporta el nombre del metodo, que es lo que lleva el marker target.
  - Scripts de modules (no *_utils.py): ademas, todos los metodos que el
    script llama sobre un objeto (`algo.metodo(...)`) y que existen en la
    clase del modulo (app.py de addons + *_utils.py de modules).
  - Lo que no es .py (XML de formas, catalogos, reportes) va a `sin_tests`.

Sanic (mismas reglas, sus clases son otras):
  - lkf-sanic-apps: solo addons/<modulo>/ (service.py, models.py...). En
    routes.py no cuenta el handler sino los metodos de la clase que llama.
  - sdk-modules-sanic: *_service.py como los *_utils.py. Los *_sdk.py y
    *_routes.py son pegamento: cuentan los metodos que llaman y, para cada
    `dispatch("endpoint")`, los que llama el handler de @route("/endpoint").

Uso:
  bin/lkf_changes.py                       # addons = este repo, modules = ./modules
  bin/lkf_changes.py --modules RUTA --json
"""
import argparse
import ast
import json
import os
import py_compile
import re
import subprocess
import sys
import tempfile

BASE_REF = "origin/master"


def git(repo, *args, check=True):
    res = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} ({repo}): {res.stderr.strip()}")
    return res.stdout if res.returncode == 0 else None


def show(repo, rev, path):
    """Contenido de path en rev, o None si no existe ahi."""
    return git(repo, "show", f"{rev}:{path}", check=False)


def changed_lines(repo, base, head):
    """{path: {"new": set(lineas nuevas), "old": set(lineas viejas), "status": X}}"""
    files = {}
    for line in git(repo, "diff", "--name-status", "--no-renames", base, head).splitlines():
        status, path = line.split("\t", 1)
        files[path] = {"new": set(), "old": set(), "status": status[0]}
    current = None
    for line in git(repo, "diff", "-U0", "--no-renames", base, head).splitlines():
        if line.startswith("+++ "):
            current = None if line[4:] == "/dev/null" else line[6:]
        elif line.startswith("--- ") and line[4:] != "/dev/null":
            current = line[6:]
        elif line.startswith("@@") and current in files:
            m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
            o, oc, n, nc = int(m[1]), int(m[2] or 1), int(m[3]), int(m[4] or 1)
            files[current]["old"].update(range(o, o + oc))
            files[current]["new"].update(range(n, n + nc))
            # Borrado puro (nc == 0): marca la linea vecina en el lado nuevo
            # para que el def que lo contenia cuente como cambiado.
            if nc == 0:
                files[current]["new"].add(n)
    return files


def defs(source):
    """[(nombre, linea_ini, linea_fin)] de funciones y metodos (sin anidadas)."""
    tree = ast.parse(source)
    out = []

    def add(node):
        start = min([node.lineno] + [d.lineno for d in node.decorator_list])
        out.append((node.name, start, node.end_lineno))

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add(node)
        elif isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add(sub)
    return out


def touched_defs(source, lines):
    return {name for name, a, b in defs(source) if any(a <= l <= b for l in lines)}


COMPOUND = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try,
            ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def _calls(nodes):
    return {
        n.func.attr
        for node in nodes
        for n in ast.walk(node)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
    }


def method_calls(source, lines):
    """`x.metodo(...)` de las sentencias que tocan las lineas cambiadas.

    Sentencia simple tocada -> sus llamadas. Cabecera de un if/elif/for/while
    tocada (p.ej. `elif option == 'load_shift':`) -> tambien las de su bloque,
    porque cambiar la condicion cambia cuando corre ese bloque.
    """
    hit = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.stmt):
            continue
        if not isinstance(node, COMPOUND):
            if any(node.lineno <= l <= node.end_lineno for l in lines):
                hit |= _calls([node])
        elif isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            head = node.test if isinstance(node, (ast.If, ast.While)) else node.iter
            if any(node.lineno <= l <= head.end_lineno for l in lines):
                hit |= _calls([head, *node.body])
    return hit


def compiles(source, path):
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write(source)
    try:
        py_compile.compile(fh.name, doraise=True)
        return None
    except py_compile.PyCompileError as exc:
        msg = str(exc.exc_value).replace(fh.name, path)
        return msg.replace(os.path.basename(fh.name), os.path.basename(path))
    finally:
        os.unlink(fh.name)


# repo -> como encontrar la clase de cada modulo: (repo de donde sale, prefijo, sufijo o None)
CLASS_SOURCES = {
    "addons": (("addons", "lkf_addons/addons/{m}/", None), ("modules", "{m}/", "_utils.py")),
    "sanic": (("lkf-sanic-apps", "addons/{m}/", None), ("sdk-modules-sanic", "{m}/", "_service.py")),
}
BACK = {"addons": "addons", "modules": "addons", "lkf-sanic-apps": "sanic", "sdk-modules-sanic": "sanic"}


def _sources(back, module, paths, heads, suffix_in=None):
    """[(repo, rev, path)] de los .py de la clase del modulo en ese back."""
    out = []
    for repo, prefix, suffix in CLASS_SOURCES[back]:
        if not paths.get(repo) or not heads.get(repo):
            continue
        listed = git(paths[repo], "ls-tree", "-r", "--name-only", heads[repo], prefix.format(m=module))
        for path in (listed or "").splitlines():
            want = suffix_in or suffix
            if path.endswith(".py") and (not want or path.endswith(want)):
                out.append((repo, heads[repo], path))
    return out


def module_methods(back, module, paths, heads):
    """Metodos de la clase del modulo. addons: app.py de addons + *_utils.py de
    modules. sanic: addons/<m>/ de lkf-sanic-apps + *_service.py de sdk-modules-sanic."""
    names = set()
    for repo, rev, path in _sources(back, module, paths, heads):
        try:
            names.update(n for n, _, _ in defs(show(paths[repo], rev, path)))
        except SyntaxError:
            pass
    return names


def route_calls(module, paths, heads):
    """{endpoint: metodos llamados en su handler} de los routes.py (lkf-sanic-apps)
    y *_routes.py (sdk-modules-sanic) del modulo."""
    out = {}
    files = [(r, rev, p) for r, rev, p in _sources("sanic", module, paths, heads, suffix_in="routes.py")]
    for repo, rev, path in files:
        try:
            tree = ast.parse(show(paths[repo], rev, path))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in node.decorator_list:
                if (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute)
                        and dec.func.attr in ROUTE_DECORATORS and dec.args
                        and isinstance(dec.args[0], ast.Constant) and isinstance(dec.args[0].value, str)):
                    ep = dec.args[0].value.strip("/").split("/")[-1]
                    out.setdefault(ep, set()).update(_calls(node.body))
    return out


DISPATCH = ("dispatch", "dispatch_with_api_key")
ROUTE_DECORATORS = ("route", "get", "post", "put", "patch", "delete")


def dispatched(source, lines, default_module):
    """{(modulo, endpoint)} de los dispatch("endpoint", module=...) en las
    sentencias que tocan las lineas cambiadas (misma regla que method_calls)."""
    hit = set()

    def grab(nodes):
        for node in nodes:
            for n in ast.walk(node):
                if not isinstance(n, ast.Call):
                    continue
                name = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", None)
                if name not in DISPATCH or not n.args or not isinstance(n.args[0], ast.Constant):
                    continue
                mod = next((k.value.value for k in n.keywords
                            if k.arg == "module" and isinstance(k.value, ast.Constant)), default_module)
                hit.add((mod, str(n.args[0].value)))

    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.stmt):
            continue
        if not isinstance(node, COMPOUND):
            if any(node.lineno <= l <= node.end_lineno for l in lines):
                grab([node])
        elif isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            head = node.test if isinstance(node, (ast.If, ast.While)) else node.iter
            if any(node.lineno <= l <= head.end_lineno for l in lines):
                grab([head, *node.body])
    return hit


def glue(name, path):
    """Archivos que solo pasan la llamada a la clase: cuenta lo que llaman, no sus def."""
    if name == "lkf-sanic-apps":
        return path.endswith("/routes.py")
    if name == "sdk-modules-sanic":
        return path.endswith(("_sdk.py", "_routes.py"))
    return False


def analyze(repo, name, paths, heads):
    res = {"repo": name, "ruta": repo, "ok": True}
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    res["rama"] = branch
    res["sha"] = git(repo, "rev-parse", "HEAD").strip()
    if "/" not in branch and branch != "master":
        res["ok"] = False
        res["error"] = f"esta en '{branch}', una rama de cuenta: ahi no se puede probar un cambio"
        where = {"modules": "modules", "sdk-modules-sanic": "lkf-sanic-apps/app/modules"}.get(name, ".")
        res["ayuda"] = (
            f"Crea primero una rama nueva para tu cambio, desde master:\n"
            f"    git -C {where} checkout -b fix/<folio> origin/master\n"
            f"Formato: fix/<folio> o feat/<folio> (ej. fix/1520), siempre con '/'.\n"
            f"Si tu cambio toca varios repos (addons, modules, Sanic), usa el mismo nombre de rama en todos.\n"
            f"Si no tocaste {name}, basta con dejarlo en master:\n"
            f"    git -C {where} checkout master"
        )
        return res
    if git(repo, "rev-parse", "--verify", "-q", BASE_REF, check=False) is None:
        res["ok"] = False
        res["error"] = f"no existe {BASE_REF}; corre git fetch"
        return res

    base = git(repo, "merge-base", BASE_REF, "HEAD").strip()
    res["base"] = base
    # --ignore-submodules: en addons, workwith deja " M modules" (puntero que no se
    # commitea) y sdk_testing puede ir distinto; las pruebas montan esos repos
    # directo, asi que su puntero no cambia lo que se prueba.
    res["sin_commit"] = bool(git(repo, "status", "--porcelain", "--untracked-files=no",
                                 "--ignore-submodules=all").strip())
    funciones, sin_tests, rotos, eliminados, sin_funcion = {}, [], [], [], []

    def add(fn, why):
        funciones.setdefault(fn, set()).add(why)

    for path, info in sorted(changed_lines(repo, base, "HEAD").items()):
        if not path.endswith(".py"):
            sin_tests.append(path)
            continue
        if name == "addons" and not path.startswith("lkf_addons/"):
            continue  # bin/, miniback/, config/... no son funciones probadas por sdk_testing
        if name == "lkf-sanic-apps" and not path.startswith("addons/"):
            continue  # app/ (main, loader, middleware), bin/, docker/: no los prueba sdk_testing
        if info["status"] == "D":
            eliminados.append(path)
            continue
        new = show(repo, "HEAD", path)
        err = compiles(new, path)
        if err:
            rotos.append({"archivo": path, "error": err})
            continue
        is_glue = glue(name, path)
        hit = set() if is_glue else touched_defs(new, info["new"])
        old = show(repo, base, path)
        if old and not is_glue:
            try:
                gone = touched_defs(old, info["old"]) - {n for n, _, _ in defs(new)}
                hit |= gone
                for fn in gone:
                    add(fn, f"{path} (eliminada)")
            except SyntaxError:
                pass
        for fn in hit:
            add(fn, path)
        called = set()
        if name == "modules" and "/items/scripts/" in path and not path.endswith("_utils.py"):
            module = path.split("/", 1)[0]
            known = module_methods("addons", module, paths, heads)
            called = method_calls(new, info["new"]) & known
            for fn in called:
                add(fn, f"{path} (lo llama)")
        elif is_glue:
            module = path.split("/")[1] if name == "lkf-sanic-apps" else path.split("/", 1)[0]
            known = module_methods("sanic", module, paths, heads)
            called = method_calls(new, info["new"]) & known
            for fn in called:
                add(fn, f"{path} (lo llama)")
            for mod, ep in sorted(dispatched(new, info["new"], module)):
                via = route_calls(mod, paths, heads).get(ep, set()) & module_methods("sanic", mod, paths, heads)
                for fn in via:
                    add(fn, f"{path} (dispatch {ep})")
                called |= via
        if not hit and not called:
            sin_funcion.append(path)

    res.update(
        funciones={k: sorted(v) for k, v in sorted(funciones.items())},
        sin_tests=sin_tests,
        rotos=rotos,
        eliminados=eliminados,
        sin_funcion=sin_funcion,
    )
    return res


def print_human(results):
    for r in results:
        print(f"\n== {r['repo']}  ({r.get('rama')} @ {r.get('sha', '')[:8]})")
        if not r["ok"]:
            print(f"   x {r['error']}")
            continue
        if r["sin_commit"]:
            print("   ! hay cambios sin commit: no cuentan (se evalua HEAD)")
        if not any(r[k] for k in ("funciones", "sin_tests", "rotos", "eliminados", "sin_funcion")):
            print("   sin cambios contra master")
        for fn, why in r["funciones"].items():
            print(f"   + {fn:40s} <- {', '.join(why)}")
        for x in r["rotos"]:
            print(f"   x no compila: {x['archivo']}: {x['error']}")
        for p in r["sin_funcion"]:
            print(f"   ~ cambio fuera de funciones: {p}")
        for p in r["eliminados"]:
            print(f"   - archivo eliminado: {p}")
        for p in r["sin_tests"]:
            print(f"   ? sin tests, revisar a mano: {p}")
    targets = sorted({fn for r in results if r["ok"] for fn in r["funciones"]})
    print(f"\ntargets: {' '.join(targets) or '(ninguno)'}")


def main():
    here = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sanic = os.path.join(os.path.dirname(here), "lkf-sanic-apps")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--addons", default=here)
    ap.add_argument("--modules", default=os.path.join(here, "modules"))
    ap.add_argument("--sanic", default=sanic, help="repo lkf-sanic-apps (si no existe se omite)")
    ap.add_argument("--sanic-modules", default=os.path.join(sanic, "app", "modules"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    paths = {"addons": args.addons, "modules": args.modules,
             "lkf-sanic-apps": args.sanic, "sdk-modules-sanic": args.sanic_modules}
    paths = {k: v for k, v in paths.items() if v and os.path.exists(os.path.join(v, ".git"))}
    heads = {k: "HEAD" for k in paths}
    results = [analyze(p, name, paths, heads) for name, p in paths.items()]
    targets = sorted({fn for r in results if r["ok"] for fn in r["funciones"]})
    if args.json:
        print(json.dumps({"repos": results, "targets": targets}, indent=2, ensure_ascii=False))
    else:
        print_human(results)
    # 1 = algun archivo no compila (eso ya es rojo); el resto lo decide ./lkf test
    sys.exit(1 if any(r.get("rotos") for r in results) else 0)


if __name__ == "__main__":
    main()
