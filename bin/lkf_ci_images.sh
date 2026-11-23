#!/usr/bin/env bash
# Tags de las imagenes de pruebas publicadas en GHCR, uno por imagen: el hash
# de los archivos con que se construye. Lo usan los dos workflows de CI:
#   lkf-test-images.yml  las construye y las sube con ese tag (y develop / test)
#   lkf-test.yml         baja la del tag; si no existe (el PR cambio el
#                        Dockerfile o requires.txt), la construye como antes
#
#   bin/lkf_ci_images.sh <ws>      (<ws>/addons y <ws>/lkf-sanic-apps)
#
# Imprime "lkf_test=<hash>" y "sanic=<hash>"; en Actions tambien van a
# $GITHUB_OUTPUT. sanic-app:test parte de sanic-app:develop, que cambia por su
# lado: el hash no lo ve, por eso lkf-test-images.yml reconstruye cada semana.
set -euo pipefail

WS=${1:?uso: lkf_ci_images.sh <workspace>}

tag() { cat "$@" | sha256sum | cut -c1-12; }

out="lkf_test=$(tag "$WS/addons/test/docker/Dockerfile" "$WS/addons/test/docker/requires.txt")
sanic=$(tag "$WS/lkf-sanic-apps/docker/Dockerfile.test")"
echo "$out"
if [ -n "${GITHUB_OUTPUT:-}" ]; then
  echo "$out" >> "$GITHUB_OUTPUT"
fi
