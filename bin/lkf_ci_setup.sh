#!/usr/bin/env bash
# Arma en GitHub Actions el mismo arbol que clave10-sdk para que bin/lkf_test.py
# corra igual que en local. Lo llama .github/workflows/lkf-test.yml despues de
# clonar addons en <ws>/addons.
#
#   <ws>/addons                      (ya clonado por el workflow)
#   <ws>/addons/modules
#   <ws>/addons/test/sdk_testing
#   <ws>/linkaform_api
#   <ws>/lkf-sanic-apps
#   <ws>/lkf-sanic-apps/app/modules  (sdk-modules-sanic)
#
# Cada repo queda en la rama del PR si existe con ese nombre (el repo del PR,
# en el commit exacto del PR); si no, en master. Despues escribe la config de
# preprod (secrets/accounts.ini, current_domain, current_env y local_settings.py
# de addons y de Sanic) con PREPROD_USERNAME / PREPROD_APIKEY.
#
# Variables: PR_REPO, PR_BRANCH, PR_NUMBER, PREPROD_USERNAME, PREPROD_APIKEY.
set -euo pipefail

WS=${1:?uso: lkf_ci_setup.sh <workspace>}
ADDONS="$WS/addons"

# clone <repo> <destino>: misma regla que el clon de addons del workflow.
clone() {
  local repo=$1 dest=$2
  rm -rf "$dest"
  git clone -q --filter=blob:none --no-checkout "https://github.com/linkaform/$repo.git" "$dest"
  if [ "$repo" = "$PR_REPO" ]; then
    git -C "$dest" fetch -q origin "refs/pull/$PR_NUMBER/head"
    git -C "$dest" checkout -q -B "$PR_BRANCH" FETCH_HEAD
  elif git -C "$dest" rev-parse -q --verify "refs/remotes/origin/$PR_BRANCH" >/dev/null; then
    git -C "$dest" checkout -q -B "$PR_BRANCH" "origin/$PR_BRANCH"
  else
    git -C "$dest" checkout -q master
  fi
  echo "$repo: $(git -C "$dest" rev-parse --abbrev-ref HEAD) $(git -C "$dest" rev-parse --short HEAD)"
}

clone modules            "$ADDONS/modules"
clone sdk_testing        "$ADDONS/test/sdk_testing"
clone linkaform_api      "$WS/linkaform_api"
clone lkf-sanic-apps     "$WS/lkf-sanic-apps"
clone sdk-modules-sanic  "$WS/lkf-sanic-apps/app/modules"

if [ -z "${PREPROD_USERNAME:-}" ] || [ -z "${PREPROD_APIKEY:-}" ]; then
  echo "::error::Faltan los secrets PREPROD_USERNAME / PREPROD_APIKEY (cuenta de pruebas en preprod)"
  exit 1
fi

# Catalogo con una sola cuenta, "ci", en preprod. Sin clave10 = true: el prefijo
# /api/clave10 solo esta confirmado en prod.
for secrets in "$ADDONS/secrets" "$WS/lkf-sanic-apps/secrets"; do
  mkdir -p "$secrets"
  rm -f "$secrets/accounts.ini"
  umask 077
  printf '[ci]\nusername = %s\napikey = %s\n' "$PREPROD_USERNAME" "$PREPROD_APIKEY" > "$secrets/accounts.ini"
  echo ci > "$secrets/current_domain"
  echo preprod > "$secrets/current_env"
done
cp "$ADDONS/test/ci/local_settings_addons.py" "$ADDONS/config/local_settings.py"
cp "$ADDONS/test/ci/local_settings_sanic.py" "$WS/lkf-sanic-apps/app/config/local_settings.py"
echo "config de preprod lista (cuenta ci)"
