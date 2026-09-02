# coding: utf-8
"""Renombra el par forma+catalogo `definicion_de_permisos` a `definicion_de_requerimientos`.

Motivo: el catalogo dejo de describir solo permisos. Su campo principal
(662962bb203407ab90c886e5) se llama "Requerimientos" y agrupa vigencia, examen,
comprobante fotografico, comprobante documental e inspeccion visual. El nombre viejo ya
no describia lo que el item modela.

Son dos items distintos de LKFModules que comparten slug: la forma (121743) y el
catalogo (121726) al que el workflow la sincroniza. Se renombran los dos en sitio: es un
UPDATE del doc existente, asi que ambos conservan su item_id y todos sus registros.

`definicion_de_permisos_rules.xml` y `_workflow.xml` no aparecen aqui porque no son items
de LKFModules: se suben con upload_rules/upload_workflows contra el form_id que llevan
dentro (lkf_addons/items/form_resource.py). Basta con renombrar los archivos para que
form_resource los siga asociando a la forma por prefijo.
"""

name = '0001_rename_definicion_de_permisos'

operations = [
    {
        'op': 'rename',
        'item_type': 'catalog',
        'from': {'module': 'accesos', 'item_name': 'definicion_de_permisos'},
        'to': {'module': 'accesos',
               'item_name': 'definicion_de_requerimientos',
               'item_full_name': 'Definicion de Requerimientos'},
    },
    {
        'op': 'rename',
        'item_type': 'form',
        'from': {'module': 'accesos', 'item_name': 'definicion_de_permisos'},
        'to': {'module': 'accesos',
               'item_name': 'definicion_de_requerimientos',
               'item_full_name': 'Definicion de Requerimientos'},
    },
]
