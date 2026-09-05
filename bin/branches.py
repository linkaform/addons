#!/usr/bin/env python3
# coding: utf-8
"""branches: le da a cada cuenta una rama de modules/ que se llama como su dominio.

Historicamente las ramas de modules/ se llaman account_<account_id> (account_29954) y la
cuenta se identifica por su dominio -- la seccion de secrets/accounts.ini (gfh). Esa doble
identidad obliga a cargar la llave branch_name en cada seccion, y hace imposible deducir
la rama a partir del nombre de la cuenta.

Esto NO renombra ni borra nada: copia cada rama account_<id> a una rama nueva con el
nombre del dominio, apuntando al mismo commit. Las viejas siguen vivas para que el equipo
migre a su ritmo. Retirarlas es una decision posterior, y este script no la implementa.

Corre en el HOST, no dentro del contenedor: modules/ es un submodulo cuyo .git real vive
en ../.git/modules/modules, que no esta montado.

    ./lkf branches plan       # que copiaria, y por que se brinca lo que se brinca
    ./lkf branches create     # crea las ramas en origin y limpia branch_name del ini
    ./lkf branches status     # divergencia entre cada par (vieja, nueva)

Si un dominio no tiene rama de origen no se le inventa una, y si a proposito su rama no
debe llamarse como la seccion, se excluye. Las dos excepciones se piden a mano:

    ./lkf branches create --desde-master soter --brincar linkaform
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time

# workwith ya resuelve catalogo, dominios y rama por dominio; aqui se reusa tal cual.
import workwith as w
from workwith import Error

RE_SECCION = re.compile(r'^\s*\[(?P<nombre>[^\]]+)\]')
RE_BRANCH_NAME = re.compile(r'^\s*branch_name\s*=')

# Motivos por los que un dominio no entra a la copia. Se imprimen tal cual en `plan`.
SIN_ID = 'sin account_id en el catalogo'
YA_ES_DOMINIO = 'su rama ya se llama como el dominio'


class Par(object):
    """Una copia por hacer: de la rama `origen` a una rama nueva llamada `dominio`."""

    def __init__(self, dominio, origen, account_id):
        self.dominio = dominio
        self.origen = origen
        self.account_id = account_id


def remotas():
    """{nombre_de_rama: sha} de origin, segun los refs que tengamos fetcheados."""
    salida = w.git('branch', '-r', '--format=%(refname:short) %(objectname)')
    res = {}
    for linea in salida.splitlines():
        partes = linea.split()
        if len(partes) != 2:
            continue
        nombre, sha = partes
        if not nombre.startswith('origin/'):
            continue
        nombre = nombre.split('origin/', 1)[1]
        if nombre == 'HEAD':   # el symref origin/HEAD -> origin/master, no es una rama
            continue
        res[nombre] = sha
    return res


def clasificar(cat, rem, desde_master=(), excluidos=()):
    """Parte los dominios del catalogo en (copias por hacer, brincados con su motivo)."""
    copiar, brincar = [], []
    for dominio in sorted(w.dominios(cat)):
        account_id = cat[dominio].get('account_id', '').strip()
        origen = w.rama_de(cat, dominio)
        if dominio in excluidos:
            # Excluido a mano: ni se copia, ni se le toca su branch_name.
            brincar.append((dominio, 'excluido con --brincar (branch_name = %s)' % origen))
        elif dominio in rem:
            brincar.append((dominio, YA_ES_DOMINIO))
        elif dominio in desde_master:
            # Excepcion pedida a mano: la cuenta no tiene rama propia todavia.
            copiar.append(Par(dominio, 'master', account_id))
        elif not account_id:
            brincar.append((dominio, SIN_ID))
        elif origen in rem:
            copiar.append(Par(dominio, origen, account_id))
        else:
            brincar.append((dominio, 'no existe origin/%s' % origen))
    return copiar, brincar


def fetch():
    print('fetch origin...')
    w.git('fetch', 'origin', '--prune', '--quiet')


def push(refspec):
    """Empuja un refspec. Devuelve (ok, salida) en vez de lanzar: un fallo no aborta el lote."""
    res = subprocess.run(['git', '-C', w.MODULES, 'push', 'origin', refspec],
                         capture_output=True, text=True)
    return res.returncode == 0, (res.stderr or res.stdout).strip()


def quitar_branch_name(dominios_):
    """Borra la linea branch_name de las secciones dadas, conservando comentarios.

    A proposito no se usa configparser.write(): reescribiria el archivo entero y se
    llevaria todos los comentarios, que es donde vive la mitad de la documentacion del
    catalogo. Aqui se filtra linea por linea, acotado a la seccion.
    """
    objetivo = set(dominios_)
    if not objetivo:
        return []

    with open(w.ACCOUNTS, encoding='utf-8') as fh:
        lineas = fh.readlines()

    modo = os.stat(w.ACCOUNTS).st_mode
    respaldo = '%s.bak-%s' % (w.ACCOUNTS, time.strftime('%Y%m%d-%H%M%S'))
    shutil.copy2(w.ACCOUNTS, respaldo)
    os.chmod(respaldo, 0o600)

    seccion, salida, quitadas = None, [], []
    for linea in lineas:
        m = RE_SECCION.match(linea)
        if m:
            seccion = m.group('nombre').strip()
        elif seccion in objetivo and RE_BRANCH_NAME.match(linea):
            quitadas.append(seccion)
            continue
        salida.append(linea)

    with open(w.ACCOUNTS, 'w', encoding='utf-8') as fh:
        fh.writelines(salida)
    os.chmod(w.ACCOUNTS, modo & 0o777)

    print('\ncatalogo: %d linea(s) branch_name quitadas de %s'
          % (len(quitadas), os.path.basename(w.ACCOUNTS)))
    print('          respaldo en %s' % os.path.basename(respaldo))
    for d in quitadas:
        print('  - %s' % d)
    return quitadas


def divergencia(nueva, vieja):
    """(commits en la vieja que faltan en la nueva, y al reves)."""
    atras = w.git('rev-list', '--count', 'origin/%s..origin/%s' % (nueva, vieja))
    adelante = w.git('rev-list', '--count', 'origin/%s..origin/%s' % (vieja, nueva))
    return int(atras or 0), int(adelante or 0)


def cmd_plan(cat, rem, args):
    copiar, brincar = clasificar(cat, rem, args.desde_master, args.brincar)
    print('\n=== a copiar (%d) ===' % len(copiar))
    for p in copiar:
        ya = rem.get(p.dominio)
        nota = ''
        if ya:
            nota = '  [ya existe%s]' % ('' if ya == rem.get(p.origen) else ', OTRO COMMIT')
        print('  %-22s -> %-22s (id %s)%s' % (p.origen, p.dominio, p.account_id or '?', nota))
    print('\n=== se brincan (%d) ===' % len(brincar))
    for dominio, motivo in brincar:
        print('  %-22s %s' % (dominio, motivo))
    print('\nNada de esto se ejecuto. Para hacerlo:  ./lkf branches create')
    return 0


def cmd_create(cat, rem, args):
    copiar, brincar = clasificar(cat, rem, args.desde_master, args.brincar)
    if not copiar:
        print('No hay nada que copiar.')
        return 0

    print('\n=== creando %d rama(s) en origin ===' % len(copiar))
    listas = []
    for p in copiar:
        sha_origen = rem.get(p.origen)
        sha_destino = rem.get(p.dominio)
        if sha_destino and sha_destino == sha_origen:
            print('  = %-22s ya existe y apunta al mismo commit' % p.dominio)
            listas.append(p.dominio)
            continue
        if sha_destino:
            # Nunca --force: si alguien ya la creo y divergio, es su trabajo, no basura.
            print('  ! %-22s YA EXISTE con otro commit, se salta' % p.dominio)
            print('      origin/%s = %s' % (p.dominio, sha_destino[:9]))
            print('      origin/%s = %s' % (p.origen, (sha_origen or '?')[:9]))
            continue
        ok, salida = push('origin/%s:refs/heads/%s' % (p.origen, p.dominio))
        if ok:
            print('  + %-22s <- %s (%s)' % (p.dominio, p.origen, (sha_origen or '?')[:9]))
            listas.append(p.dominio)
        else:
            print('  x %-22s FALLO: %s' % (p.dominio, salida.replace('\n', ' | ')))

    if args.no_ini:
        print('\n--no-ini: el catalogo se queda como esta.')
    else:
        # Solo se limpia branch_name de las ramas que se confirmo que ya existen: si un
        # push fallo, la seccion conserva su branch_name y workwith sigue funcionando.
        quitar_branch_name(listas)

    print('\n%d de %d rama(s) listas. Ninguna rama vieja se toco.' % (len(listas), len(copiar)))
    return 0 if len(listas) == len(copiar) else 1


def cmd_status(cat, rem, args):
    """Vigila la divergencia mientras las dos ramas del par siguen vivas."""
    filas = []
    for dominio in sorted(w.dominios(cat)):
        account_id = cat[dominio].get('account_id', '').strip()
        if dominio not in rem or not account_id:
            continue
        vieja = 'account_%s' % account_id
        if vieja not in rem:
            continue
        atras, adelante = divergencia(dominio, vieja)
        filas.append((dominio, vieja, atras, adelante))

    if not filas:
        print('No hay pares vivos: ningun dominio con rama propia conserva su account_<id>.')
        return 0

    print('\n%-22s %-20s %-12s %s' % ('dominio', 'rama vieja', 'solo vieja', 'solo nueva'))
    print('-' * 70)
    sucios = 0
    for dominio, vieja, atras, adelante in filas:
        marca = '' if not atras else '  <-- revisar'
        if atras:
            sucios += 1
        print('%-22s %-20s %-12s %s%s' % (dominio, vieja, atras, adelante, marca))

    print('\n%d par(es); %d con commits en la rama vieja que no estan en la nueva.'
          % (len(filas), sucios))
    if sucios:
        print('Traelos con:  cd modules && git checkout <dominio> && git merge origin/account_<id>')
    return 0


COMANDOS = {'plan': cmd_plan, 'create': cmd_create, 'status': cmd_status}


def main(argv):
    par = argparse.ArgumentParser(
        prog='./lkf branches',
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__)
    par.add_argument('comando', nargs='?', default='plan', choices=sorted(COMANDOS),
                     help='plan (default): que copiaria. create: lo hace. status: divergencia.')
    par.add_argument('--desde-master', metavar='DOMINIO', action='append', default=[],
                     help='Dominio sin rama de origen al que SI se le crea una, desde master. '
                          'Repetible. Sin esto, un dominio sin rama simplemente se brinca.')
    par.add_argument('--brincar', metavar='DOMINIO', action='append', default=[],
                     help='Dominio que se deja intacto: no se le crea rama ni se le quita '
                          'branch_name. Repetible. Para cuentas cuya rama a proposito no se '
                          'llama como la seccion.')
    par.add_argument('--no-ini', action='store_true',
                     help='No quitar las llaves branch_name de accounts.ini (solo create).')
    par.add_argument('--no-fetch', action='store_true',
                     help='No hacer fetch antes; usa los refs de origin que ya tengas.')
    args = par.parse_args(argv[1:])
    args.desde_master = set(args.desde_master)
    args.brincar = set(args.brincar)

    cat = w.cargar_catalogo()
    conocidos = set(w.dominios(cat))
    for flag, pedidos in (('--desde-master', args.desde_master), ('--brincar', args.brincar)):
        faltantes = pedidos - conocidos
        if faltantes:
            raise Error('%s: estos dominios no estan en %s: %s'
                        % (flag, w.ACCOUNTS, ', '.join(sorted(faltantes))))
    choque = args.desde_master & args.brincar
    if choque:
        raise Error('%s esta en --desde-master y en --brincar a la vez.' % ', '.join(sorted(choque)))

    if not args.no_fetch:
        fetch()
    return COMANDOS[args.comando](cat, remotas(), args)


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except Error as e:
        print('\n%s\n%s\n%s' % ('=' * 60, e, '=' * 60), file=sys.stderr)
        sys.exit(1)
