# coding: utf-8
"""Motor de migraciones de items instalados.

En este framework el nombre del archivo XML es la clave primaria de facto: se guarda
como `item_name` en la coleccion Mongo `LKFModules` y el instalador identifica cada
item con la tripleta `(module, item_type, item_name)` (`serach_module_item`). Por eso
renombrar un archivo -o moverlo de modulo- sin mas hace que el instalador NO encuentre
el item y cree uno nuevo, dejando huerfano el anterior con todos sus registros.

Una migracion declara ese cambio de identidad para que el instalador siga apuntando al
mismo item. Se escribe un archivo numerado por migracion, al estilo de Django/Alembic:

    lkf_addons/addons/<modulo>/migrations/0001_lo_que_sea.py

        name = '0001_lo_que_sea'
        operations = [
            {
                'op': 'rename',
                'item_type': 'catalog',          # catalog | form | script | report
                'from': {'module': 'accesos', 'item_name': 'nombre_viejo'},
                'to':   {'module': 'accesos',
                         'item_name': 'nombre_nuevo',
                         'item_full_name': 'Nombre Visible Nuevo'},
            },
        ]

Un cambio de modulo se expresa poniendo un `module` distinto en `to`; no hace falta
otra operacion.

Las migraciones se aplican solas al inicio de cada install, y son idempotentes porque
cada operacion reevalua el estado real de `LKFModules` en vez de confiar en un registro
de lo ya aplicado (mismo patron de reconciliacion que `install_script`).

OJO: solo se buscan migraciones en `lkf_addons/addons/<modulo>/migrations/`, nunca en
`/srv/scripts/addons/modules`. Cada cuenta tiene su propia rama del submodulo `modules/`
y `bin/workwith.py:merge_master()` mergea master con `-X ours`, asi que una migracion
puesta ahi puede descartarse en silencio al cambiar de cuenta.
"""

import glob
import importlib.util
import os
import time

from lkf_addons import items


class MigrationResource(items.Items):

    def find_migrations_path(self):
        """Devuelve el directorio de migraciones del modulo, o None si no tiene.

        Mismo fallback contenedor/host que usa bin/backfill_form_versions.py, para que
        el motor tambien sirva corriendo desde el repo.
        """
        repo_addons = os.path.normpath(
            os.path.join(os.path.dirname(__file__), '..', 'addons'))
        for base_path in (items.ADDONS_PATH, repo_addons):
            candidate = os.path.join(base_path, self.module, 'migrations')
            if os.path.isdir(candidate):
                return candidate
        return None

    def load_migrations(self):
        """Carga los modulos de migracion del modulo actual, ordenados por nombre."""
        migrations_path = self.find_migrations_path()
        if not migrations_path:
            return []
        migrations = []
        for file_path in sorted(glob.glob(os.path.join(migrations_path, '[0-9]*.py'))):
            # spec_from_file_location y no importlib.import_module: la mayoria de los
            # directorios de modulo no tienen __init__.py (son namespace packages).
            module_name = os.path.basename(file_path)[:-3]
            spec = importlib.util.spec_from_file_location(
                'lkf_migrations.{}.{}'.format(self.module, module_name), file_path)
            migration = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(migration)
            if not getattr(migration, 'name', None):
                migration.name = module_name
            migrations.append(migration)
        return migrations

    def applied_by(self):
        """Quien corre la migracion, tolerando las dos formas de config['USER'].

        No se usa lkf.get_user_data(): asume que el usuario viene anidado bajo
        USER['user'], pero con local_settings los campos llegan planos en USER y
        devuelve un dict de puros None. Aqui se aceptan ambas y se omite lo vacio.
        """
        user = getattr(self.lkf, 'config', {}).get('USER') or {}
        user = user.get('user', user) if isinstance(user, dict) else {}
        who = {k: user.get(k) for k in ('email', 'username', 'id') if user.get(k)}
        return who or None

    def run_migrations(self):
        migrations = self.load_migrations()
        if not migrations:
            return []
        print('******************** Running Migrations ****************************')
        applied = []
        for migration in migrations:
            for operation in getattr(migration, 'operations', []):
                op = operation.get('op')
                if op != 'rename':
                    raise self.LKFException(
                        'Migration {}: unknown op "{}". Supported ops: rename.'.format(
                            migration.name, op))
                if self.apply_rename(migration, operation):
                    applied.append((migration.name, operation))
        return applied

    def apply_rename(self, migration, operation):
        """Reapunta el doc de LKFModules al nuevo (module, item_name).

        Devuelve True solo si realmente se escribio algo.
        """
        item_type = operation['item_type']
        frm, to = operation['from'], operation['to']
        old = self.lkf.serach_module_item({
            'module': frm['module'],
            'item_type': item_type,
            'item_name': frm['item_name'],
        })
        new = self.lkf.serach_module_item({
            'module': to['module'],
            'item_type': item_type,
            'item_name': to['item_name'],
        })
        label = '{} {}/{} -> {}/{}'.format(
            item_type, frm['module'], frm['item_name'], to['module'], to['item_name'])

        if old and new:
            raise self.LKFException(
                'Migration {}: no se puede migrar {}. Existen los dos items a la vez: '
                'el viejo (item_id {}) y el nuevo (item_id {}). Alguien instalo el '
                'rename sin migrar y se duplico. Hay que decidir a mano cual conservar '
                'antes de volver a instalar.'.format(
                    migration.name, label, old.get('item_id'), new.get('item_id')))
        if new:
            print('  [ok] {} ya migrado (item_id {})'.format(label, new.get('item_id')))
            return False
        if not old:
            print('  [skip] {}: no instalado en esta cuenta'.format(label))
            return False

        record = {
            'name': migration.name,
            'applied_at': int(time.time()),
            'from': {'module': frm['module'], 'item_name': frm['item_name']},
        }
        applied_by = self.applied_by()
        if applied_by:
            record['applied_by'] = applied_by

        # El _id es obligatorio como query: update() hace update_many con upsert=True,
        # cualquier otro filtro podria insertar un doc espurio.
        changes = {
            'module': to['module'],
            'item_name': to['item_name'],
            'migrations': old.get('migrations', []) + [record],
        }
        if to.get('item_full_name'):
            changes['item_full_name'] = to['item_full_name']
        self.lkf.update({'_id': old['_id']}, changes)
        print('  [migrated] {} (item_id {})'.format(label, old.get('item_id')))
        return True
