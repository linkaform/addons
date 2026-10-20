# coding: utf-8
"""Renombra el catalogo `catalogo_de_formas` a `catalogo_de_items`.

Motivo: el catalogo ahora alimenta el formulario "Catalogo de Items"
(`catalogo_de_items.xml`), y el nombre viejo ya no describia lo que lista.

Se renombra en sitio: es un UPDATE del doc existente en LKFModules, asi que el catalogo
conserva su item_id (y con el su catalog id / obj_id) y todos sus registros. Sin esta
migracion el instalador no encontraria `catalogo_de_items` y crearia un catalogo nuevo,
dejando huerfano el viejo y a los forms ya ligados (carga_universal_module,
programar_tareas, bitacora_rondines, ...) apuntando a el.

Solo el catalogo: la forma `catalogo_de_items` es un item de tipo `form` aparte y ya se
instala con ese nombre.
"""

name = '0001_rename_catalogo_de_formas'

operations = [
    {
        'op': 'rename',
        'item_type': 'catalog',
        'from': {'module': 'base', 'item_name': 'catalogo_de_formas'},
        'to': {'module': 'base',
               'item_name': 'catalogo_de_items',
               'item_full_name': 'Catalogo de Items'},
    },
]
