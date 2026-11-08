#!/usr/bin/env python3
"""Detecta que funciones cambiaron en addons y modules contra origin/master.

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


def module_methods(addons, modules, module, head_addons, head_modules):
    """Metodos de la clase del modulo: app.py (y archivos) de addons + *_utils.py de modules."""
    names = set()
    for repo, rev, prefix, only_utils in (
        (addons, head_addons, f"lkf_addons/addons/{module}/", False),
        (modules, head_modules, f"{module}/", True),
    ):
        if not repo:
            continue
        for path in git(repo, "ls-tree", "-r", "--name-only", rev, prefix).splitlines():
            if not path.endswith(".py") or (only_utils and not path.endswith("_utils.py")):
                continue
            src = show(repo, rev, path)
            try:
                names.update(n for n, _, _ in defs(src))
            except SyntaxError:
                pass
    return names


def analyze(repo, name, addons, modules, heads):
    res = {"repo": name, "ruta": repo, "ok": True}
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    res["rama"] = branch
    res["sha"] = git(repo, "rev-parse", "HEAD").strip()
    if "/" not in branch and branch != "master":
        res["ok"] = False
        res["error"] = (
            f"rama '{branch}' es de cuenta (sin '/'); cambia a tu fix/... o feat/... "
            "(o a master si no tocaste este repo)"
        )
        return res
    if git(repo, "rev-parse", "--verify", "-q", BASE_REF, check=False) is None:
        res["ok"] = False
        res["error"] = f"no existe {BASE_REF}; corre git fetch"
        return res

    base = git(repo, "merge-base", BASE_REF, "HEAD").strip()
    res["base"] = base
    res["sin_commit"] = bool(git(repo, "status", "--porcelain", "--untracked-files=no").strip())
    funciones, sin_tests, rotos, eliminados, sin_funcion = {}, [], [], [], []

    def add(fn, why):
        funciones.setdefault(fn, set()).add(why)

    for path, info in sorted(changed_lines(repo, base, "HEAD").items()):
        if not path.endswith(".py"):
            sin_tests.append(path)
            continue
        if name == "addons" and not path.startswith("lkf_addons/"):
            continue  # bin/, miniback/, config/... no son funciones probadas por sdk_testing
        if info["status"] == "D":
            eliminados.append(path)
            continue
        new = show(repo, "HEAD", path)
        err = compiles(new, path)
        if err:
            rotos.append({"archivo": path, "error": err})
            continue
        hit = touched_defs(new, info["new"])
        old = show(repo, base, path)
        if old:
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
            known = module_methods(addons, modules, module, heads["addons"], heads["modules"])
            called = method_calls(new, info["new"]) & known
            for fn in called:
                add(fn, f"{path} (lo llama)")
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
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--addons", default=here)
    ap.add_argument("--modules", default=os.path.join(here, "modules"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    heads = {}
    for key in ("addons", "modules"):
        path = getattr(args, key)
        heads[key] = "HEAD" if path and os.path.exists(os.path.join(path, ".git")) else None
    results = [
        analyze(args.addons, "addons", args.addons, args.modules, heads),
        analyze(args.modules, "modules", args.addons, args.modules, heads),
    ]
    targets = sorted({fn for r in results if r["ok"] for fn in r["funciones"]})
    if args.json:
        print(json.dumps({"repos": results, "targets": targets}, indent=2, ensure_ascii=False))
    else:
        print_human(results)
    # 1 = algun archivo no compila (eso ya es rojo); el resto lo decide ./lkf test
    sys.exit(1 if any(r.get("rotos") for r in results) else 0)


if __name__ == "__main__":
    main()
