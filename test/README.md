# Linkaform/Python:Develeop

Contenedro base para correr pruebas de LinkaFrom

Para hacer build de la imagen correr

'''
docker-compose build --no-cache lkf-test
docker-compose build lkf-test
'''

Para subir imagen

'''
docker push linkaform/lkf-test:develop
docker tag linkaform/lkf-test:develop linkaform/lkf-test:latest
docker push linkaform/lkf-test:latest

'''

Para probar imagen

'''
docker run  -i -t linkaform/lkf-test:develop bash

docker run   -w /srv/scripts/ -v `pwd`:/srv/scripts -v /home/josepato/lkf/linkaform_api/linkaform_api:/usr/local/lib/python3.7/site-packages/linkaform_api/ --name lkf_test -d linkaform/lkf_test:develop sleep infinity


docker exec -it lkf_test bash

'''


'''
docker-compose build lkf-test
'''

## Para subir la imagene a producion, de momento ser hara con un tag
'''
docker tag linkaform/lkf-test:develop linkaform/lkf-test:latest
docker push linkaform/lkf-test:latest
'''