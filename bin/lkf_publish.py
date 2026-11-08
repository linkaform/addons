"""Publica el resultado de ./lkf test en GitHub.

Por cada repo (addons, modules) que tenga cambios y PR abierto:
  - commit status `lkf-test` sobre su SHA (verde / rojo / pendiente). Es el
    check que exige el ruleset de master. Atado al SHA: un push nuevo lo deja
    sin status hasta volver a correr ./lkf test.
  - un comentario en el PR (uno solo; se edita en cada corrida) con las
    funciones detectadas, los pasos y el link al PR hermano del otro repo.

Requisitos: `gh` autenticado con permiso de escritura, y el SHA ya pusheado
(si no, ./lkf test guarda el resultado y luego `./lkf test --publicar`).
"""
import json
import re
import subprocess

MARKER = "<!-- lkf-test -->"
STATE = {"verde": "success", "rojo": "failure", "pendiente": "pending"}
ICON = {"ok": "✅", "rojo": "❌", "pendiente": "⏳", "aviso": "⚠️", "omitido": "➖"}


def run(*cmd, input=None):
    res = subprocess.run(cmd, capture_output=True, text=True, input=input)
    if res.returncode:
        raise RuntimeError(f"{' '.join(cmd[:4])}...: {res.stderr.strip()[:300]}")
    return res.stdout


def slug(repo_path):
    url = run("git", "-C", repo_path, "remote", "get-url", "origin").strip()
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    return m[1]


def pushed(repo_path, branch, sha):
    """El SHA ya esta en origin/<rama> (si no, GitHub no lo conoce)."""
    subprocess.run(["git", "-C", repo_path, "fetch", "-q", "origin", branch], capture_output=True)
    res = subprocess.run(
        ["git", "-C", repo_path, "rev-parse", "-q", "--verify", f"origin/{branch}"],
        capture_output=True, text=True,
    )
    return res.returncode == 0 and res.stdout.strip() == sha


def find_pr(gh_repo, branch):
    prs = json.loads(run("gh", "pr", "list", "-R", gh_repo, "--head", branch, "--state", "open",
                         "--json", "number,url"))
    return prs[0] if prs else None


def has_changes(r):
    return any(r[k] for k in ("funciones", "sin_tests", "rotos", "eliminados", "sin_funcion"))


def description(result):
    v = result["veredicto"]
    bad = [p for p in result["pasos"] if p["estado"] in ("rojo", "pendiente")]
    if bad:
        txt = f"{v}: {bad[0]['paso']} - {bad[0]['detalle']}"
    else:
        n = len(result["targets"])
        txt = f"{v}: {n} funcion(es) probadas" if n else f"{v}: sin funciones cambiadas"
    return txt[:139]


def body(result, me, brothers):
    v = result["veredicto"]
    head = {"verde": "✅ **lkf-test: verde**", "rojo": "❌ **lkf-test: rojo**",
            "pendiente": "⏳ **lkf-test: pendiente**"}[v]
    lines = [MARKER, f"{head} · {result['segundos']} s", ""]
    if brothers:
        lines.append("**Va junto con:** " + ", ".join(f"{b['gh']}#{b['pr']['number']}" for b in brothers))
        lines.append("Corrida conjunta: el código local de los dos repos se probó junto.")
        lines.append("")
    lines.append("| Repo | Rama | SHA | Funciones detectadas |")
    lines.append("|---|---|---|---|")
    for r in result["repos"]:
        fns = ", ".join(f"`{f}`" for f in r["funciones"]) or "—"
        lines.append(f"| {r['repo']} | `{r['rama']}` | `{r['sha'][:8]}` | {fns} |")
    lines += ["", "| Paso | | Detalle |", "|---|---|---|"]
    for p in result["pasos"]:
        det = p["detalle"].replace("|", "\\|").replace("\n", " ")[:300]
        lines.append(f"| {p['paso']} | {ICON[p['estado']]} | {det} |")
    extra = [f"`{x}`" for r in result["repos"] for x in r["sin_tests"]]
    if extra:
        lines += ["", "**Sin tests, revisar a mano:** " + ", ".join(extra)]
    lines += ["", f"<sub>Generado por `./lkf test` en local. Status atado a `{me['sha'][:8]}`: "
              "un push nuevo pide volver a correrlo.</sub>"]
    return "\n".join(lines)


def upsert_comment(gh_repo, number, text):
    comments = json.loads(run("gh", "api", f"repos/{gh_repo}/issues/{number}/comments", "--paginate"))
    mine = [c for c in comments if MARKER in (c.get("body") or "")]
    payload = json.dumps({"body": text})
    if mine:
        run("gh", "api", "-X", "PATCH", f"repos/{gh_repo}/issues/comments/{mine[-1]['id']}",
            "--input", "-", input=payload)
        return "editado"
    run("gh", "api", "-X", "POST", f"repos/{gh_repo}/issues/{number}/comments", "--input", "-", input=payload)
    return "nuevo"


def publish(result):
    """Regresa (publicado: bool, mensajes: [str])."""
    msgs = []
    if not result.get("publicable"):
        return False, ["no se publica: habia cambios sin commit (lo probado no es lo commiteado)"]
    targets = []
    for r in result["repos"]:
        if r["rama"] == "master" or not has_changes(r):
            continue
        gh = slug(r["ruta"])
        if not pushed(r["ruta"], r["rama"], r["sha"]):
            msgs.append(f"{r['repo']}: {r['sha'][:8]} no esta en origin/{r['rama']}; "
                        "haz push y corre ./lkf test --publicar")
            continue
        pr = find_pr(gh, r["rama"])
        targets.append({"repo": r, "gh": gh, "pr": pr})
        if not pr:
            msgs.append(f"{r['repo']}: sin PR abierto para {r['rama']}; solo se publica el status")
    if not targets:
        return False, msgs or ["nada que publicar (sin cambios fuera de master)"]
    for t in targets:
        r, gh = t["repo"], t["gh"]
        state = STATE[result["veredicto"]]
        run("gh", "api", "-X", "POST", f"repos/{gh}/statuses/{r['sha']}",
            "-f", f"state={state}", "-f", "context=lkf-test", "-f", f"description={description(result)}")
        line = f"{r['repo']}: status lkf-test={state} en {r['sha'][:8]}"
        if t["pr"]:
            brothers = [b for b in targets if b is not t and b["pr"]]
            how = upsert_comment(gh, t["pr"]["number"], body(result, r, brothers))
            line += f", comentario {how} en {t['pr']['url']}"
        msgs.append(line)
    return True, msgs
