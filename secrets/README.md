

# Configurar llave publica dentro de servidor local.

### Como configurar en tu servidor local.


1. Rehacer la imagen de tu contenedor.

En la primera etapa de la compliacion del contenedor ``` FROM python:3.10.14-bullseye as addons-base``` se hace la copia del certificado a la ubicacion defautl del contenedor. 

para ello correr:
```
bash

# cd ~/lkf/addons
~/lkf/addons# ./lkf build base
~/lkf/addons# ./lkf build dev
~/lkf/addons# ./lkf build local

```

este comando corre un compiacion de base de la imagen con el comando `docker compose build lkf-addons-base`



### Te marca : No Such file or directory : '/etc/ssl/certs/lkf_jwt_key.pub'

Ver como configurar tu servidor local.