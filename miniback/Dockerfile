# Mini-back local. Solo necesita Sanic, httpx y el CLI de docker: la
# ejecucion de los scripts ocurre en el contenedor de addons, no aqui.
FROM python:3.10-slim

# CLI de docker (binario estatico, sin el demonio). Habla con el docker.sock
# del host, que se monta en docker-compose.miniback.yml.
ARG DOCKER_CLI_VERSION=27.3.1
ADD https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_CLI_VERSION}.tgz /tmp/docker.tgz
RUN tar -xzf /tmp/docker.tgz -C /usr/local/bin --strip-components=1 docker/docker \
    && rm /tmp/docker.tgz \
    && docker --version

RUN pip install --no-cache-dir sanic==23.12.1 httpx==0.27.2

WORKDIR /srv/miniback
COPY . /srv/miniback

EXPOSE 8000

# -u: stdout sin buffer, para que los logs de cada corrida salgan en vivo
# en `docker compose logs -f miniback`.
CMD ["python", "-u", "app.py"]
