# mini-back

Simula la parte del backend de LinkaForm que corre scripts de addons, para
poder probar `modules/` desde un front local **sin tener el repo
`infosync-api`**.

Cuando el back real recibe una peticion a `/api/infosync/scripts/run/`, busca
el contenedor de la cuenta (`account_10_linkaform.addons..latest`) y adentro
corre `python <script>.py '<record>' '<script_args>' 'False'`. El mini-back
hace exactamente eso, pero contra el contenedor `lkf-addons` que ya usas para
desarrollar.

```
front (localhost:3000)
   |  POST /api/infosync/scripts/run/
   v
mini-back (localhost:8000)          <- este servicio
   |  docker exec lkf-addons python /srv/.../script.py '{}' '{...}' 'False'
   v
contenedor lkf-addons               <- tu codigo de modules/, en vivo
```

## Arrancarlo

```bash
cd ~/lkf/addons
docker compose -f docker/docker-compose.miniback.yml up -d --build
curl localhost:8000/api/health
```

```json
{"ok": true, "container": "lkf-addons", "account_id": 10, "scripts": 163}
```

Necesitas el contenedor `lkf-addons` corriendo (`./lkf start addons`): el
mini-back no lo levanta, solo le habla.

Para tirarlo:

```bash
docker compose -f docker/docker-compose.miniback.yml down
```

Los logs son la herramienta principal de depuracion:

```bash
docker compose -f docker/docker-compose.miniback.yml logs -f
```

## Apuntar el front

En `clave10`, en `docker/docker-compose.yml`:

```yaml
environment:
  NEXT_PUBLIC_API_BASE_URL: http://localhost:8000/api
```

## Probarlo con curl

```bash
curl -s -X POST localhost:8000/api/infosync/scripts/run/ \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $JWT" \
  -d '{"script_name": "script_turnos.py", "option": "get_user_menu"}'
```

```json
{"response": {"data": {...}}, "log": "Loding: local_settings\n...", "success": true}
```

`GET` tambien funciona, util para probar desde el navegador:

```
localhost:8000/api/infosync/scripts/run/?script_name=script_turnos.py&option=get_user_menu
```

Cada corrida deja en el log el `docker exec` exacto. Copialo y pegalo en una
terminal para reproducirla a mano:

```
miniback: >>> docker exec lkf-addons python /srv/scripts/addons/modules/accesos/items/scripts/Accesos/script_turnos.py '{}' '{"data": {...}}' 'False'
miniback: <<< returncode=0
```

## Variables de entorno

| Variable               | Default                       | Para que                                                        |
| ---------------------- | ----------------------------- | --------------------------------------------------------------- |
| `MINIBACK_PORT`        | `8000`                        | Puerto publicado en el host.                                     |
| `LKF_ADDONS_CONTAINER` | `lkf-addons`                  | Contenedor destino del `docker exec`.                            |
| `LKF_MODULES_PATH`     | `/srv/scripts/addons/modules` | Raiz del indice, dentro del contenedor destino.                  |
| `LKF_ACCOUNT_ID`       | vacio                         | `account_id` por default. Vacio = se resuelve de `secrets/`.      |
| `LKF_SECRETS_PATH`     | `/srv/scripts/addons/secrets` | Donde busca `current_domain` y `accounts.ini`.                   |
| `LKF_UPSTREAM`         | `https://app.linkaform.com`   | Destino del proxy de login.                                      |
| `MINIBACK_TIMEOUT`     | `120`                         | Segundos maximos por script.                                     |
| `MINIBACK_INDEX_TTL`   | `30`                          | Segundos de vida del indice de scripts.                          |
| `MINIBACK_MAX_CONCURRENT` | `0`                        | Tope de scripts a la vez. 0 = sin tope.                          |

### Peticiones en paralelo

Las corridas no se hacen en fila: el `docker exec` se lanza como subproceso de
asyncio, asi que 10 llamadas del front tardan lo que la mas lenta, no la suma
de las 10.

Cada corrida es un proceso de python cargando `linkaform_api`, asi que muchas
a la vez cuestan memoria. Si la maquina sufre, se puede poner un tope:

```bash
MINIBACK_MAX_CONCURRENT=8 docker compose -f docker/docker-compose.miniback.yml up -d
```

Lo que pase del tope espera turno; no se rechaza.

### Probar un worktree

```bash
LKF_ADDONS_CONTAINER=lkf-addons-<worktree> \
  docker compose -f docker/docker-compose.miniback.yml up -d
```

Levanta antes ese contenedor con `docker/docker-compose.worktree.yml`. El
indice se construye dentro del contenedor destino, asi que no hay que montar
nada mas.

### Si el 8000 esta ocupado

Si tienes el `infosync-api` real corriendo, ya tiene el 8000. Levanta el
mini-back en otro puerto y apunta el front ahi:

```bash
MINIBACK_PORT=8010 docker compose -f docker/docker-compose.miniback.yml up -d
```

### Cuenta activa

Sin `LKF_ACCOUNT_ID`, el `account_id` sale de `secrets/current_domain` +
`secrets/accounts.ini`, igual que `config/local_settings.py`. Es decir: se
mueve cuando corres `./lkf workwith <cuenta>`. `/api/health` siempre dice cual
esta usando. Para clavarlo:

```bash
LKF_ACCOUNT_ID=10 docker compose -f docker/docker-compose.miniback.yml up -d
```

## Endpoints

| Ruta                                | Que hace                                                  |
| ----------------------------------- | ---------------------------------------------------------- |
| `POST/GET /api/infosync/scripts/run/` | Corre el script. Mismo contrato que el back real.         |
| `POST /api/infosync/user_admin/login/` | Proxy transparente a `LKF_UPSTREAM`. El JWT es real.     |
| `GET /api/health`                     | Estado, contenedor, cuenta y numero de scripts indexados. |

Todo lo demas que usa el front (`cloud_upload`, `renew_jwt`,
`profile_picture`, `pwd_reset`) ya apunta a `app.linkaform.com` directo, por
eso no se simula.

### Codigos de error

| HTTP | `code` | Cuando                                                        |
| ---- | ------ | ------------------------------------------------------------- |
| 404  | 11     | El `script_name` no existe en ningun modulo.                  |
| 400  | 12     | El script fallo, el contenedor no responde, o se agoto el timeout. |
| 400  | 20     | El mismo nombre de archivo esta en dos modulos (ver `matches`). |
| 400  | —      | Falta `script_name`, o el body no es JSON valido.             |
| 502  | —      | No se pudo contactar `LKF_UPSTREAM` en el login.              |

Los codigos 11 y 12 son los mismos del back real. El 20 es propio: en
produccion los scripts de una cuenta viven planos en una sola carpeta y un
nombre repetido no puede pasar; aqui viven en arbol por modulo, asi que la
ambiguedad se reporta con las rutas candidatas en vez de elegir al azar.

## Que NO simula

- **Permisos.** No hay `can_view_item`, ni dueno del script, ni scripts
  publicos. Cualquiera que alcance el puerto corre cualquier script con el
  JWT que quiera.
- **Un contenedor por cuenta.** Siempre apunta a uno solo. No replica
  `account_{id}_{imagen}`.
- **Levantar el contenedor.** Si `lkf-addons` esta apagado, responde con un
  error que lo dice; no lo arranca.
- **Ejecucion diferida.** `is_workflow` y `runtime` se ignoran: cada peticion
  espera a que su script termine. No hay huey ni cola. (Las peticiones si
  corren en paralelo entre si, ver arriba.)
- **`ScriptLog` / `WorkflowLog`.** Los logs van a stdout y no se guardan.
- **Records grandes.** No se corta el `record` por `MAX_ARG_STRLEN` ni se
  sube a B2. El tercer argumento siempre va como `'False'`.
- **Scripts en Java o JavaScript.** Solo Python.
- **Validacion del JWT.** Se pasa tal cual al script. Si esta vencido, el
  error lo tira la API real desde adentro, igual que en produccion.

Una diferencia deliberada: el back real devuelve 400 ante **cualquier** stderr,
aun con `returncode 0` (`script_resource.py:763`). Aqui el 400 sale cuando el
`returncode` no es 0 o cuando el stderr trae una excepcion, para que un
warning no se vea como un fallo.

## Seguridad

Esto es una herramienta de desarrollo local. Dos razones para no exponerla:

- Monta `/var/run/docker.sock`, lo que equivale a **acceso root al host**.
- El log imprime el JWT completo de cada peticion.

No la publiques ni la corras en un ambiente compartido.

## Archivos

| Archivo       | Que tiene                                                       |
| ------------- | --------------------------------------------------------------- |
| `app.py`      | Rutas de Sanic, CORS y proxy de login.                          |
| `index.py`    | Indice `script_name` -> ruta, por `find` dentro del contenedor.  |
| `runner.py`   | Argumentos, `docker exec`, y traduccion del stdout.              |
| `settings.py` | Variables de entorno y resolucion de la cuenta.                  |
| `errors.py`   | Errores con mensaje presentable.                                 |
