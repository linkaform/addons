#!/usr/local/bin/python
# coding: utf-8
"""
One-time backfill: stamps a 'version: <epoch>' marker into the <description>
tag of every form XML of a module that doesn't have one yet.

Without this marker lkfaddons has no reliable way to tell if a form changed
(updated_at gets rewritten by Linkaform on install, so it can't be diffed),
so install always re-uploads every form. Once every form XML carries a
version marker, install can skip the ones that didn't change.

Usage:
    python backfill_form_versions.py -m <module_name>
"""
import argparse
import os
import re
import time
import xml.etree.ElementTree as ET

# Kept in sync with download_module.py. Defined locally (instead of imported)
# so this script doesn't need linkaform_api/settings/uts installed just to
# resolve two path constants.
MODULES_PATH = '/srv/scripts/addons/modules'
ADDONS_PATH = '/usr/local/lib/python3.10/site-packages/lkf_addons/addons'

VERSION_RE = re.compile(r'version:\s*\d+')
SKIP_SUFFIXES = ('_rules.xml', '_workflow.xml', '_data.xml', '_demo.xml')


def find_forms_path(module):
    repo_addons = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'addons'))
    repo_modules = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'modules'))
    candidates = (ADDONS_PATH, MODULES_PATH, repo_addons, repo_modules)
    for base_path in candidates:
        candidate = os.path.join(base_path, module, 'items', 'forms')
        if os.path.isdir(candidate):
            return candidate
    raise SystemExit(
        f'No forms folder found for module "{module}" under any of: {candidates}'
    )


def iter_form_files(forms_path):
    for root, _dirs, files in os.walk(forms_path):
        for file_name in files:
            if not file_name.endswith('.xml'):
                continue
            if file_name.endswith(SKIP_SUFFIXES):
                continue
            yield os.path.join(root, file_name)


def stamp_version(file_path, epoch):
    with open(file_path, 'rb') as f:
        f.seek(-1, os.SEEK_END)
        had_trailing_newline = f.read(1) == b'\n'
    tree = ET.parse(file_path)
    root = tree.getroot()
    description = root.find('description')
    if description is None:
        print(f'  [skip] no <description> tag: {file_path}')
        return False
    current_text = (description.text or '').strip()
    if VERSION_RE.search(current_text):
        print(f'  [skip] already has version: {file_path}')
        return False
    new_version = f'version: {epoch}'
    description.text = f'{new_version} | {current_text}' if current_text else new_version
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    # ET.write() always drops the trailing newline; match the file's original
    # state so the diff is a clean single-line change instead of a spurious
    # "no newline at end of file" delta.
    if had_trailing_newline:
        with open(file_path, 'ab') as f:
            f.write(b'\n')
    print(f'  [stamped] {file_path} -> {description.text}')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Backfill version marker on form XML files for a module'
    )
    parser.add_argument(
        '-m', '--module', required=True,
        help='Module name (as it appears under addons/ or modules/)'
    )
    args = parser.parse_args()

    forms_path = find_forms_path(args.module)
    epoch = int(time.time())
    print(f'Backfilling form versions for module "{args.module}" ({forms_path}) with epoch {epoch}')

    stamped = 0
    total = 0
    for file_path in iter_form_files(forms_path):
        total += 1
        if stamp_version(file_path, epoch):
            stamped += 1
    print(f'Done. Stamped {stamped}/{total} file(s).')
