#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import sys
import platform

from PyInstaller.utils.hooks import collect_submodules
import PyInstaller.__main__

arch = platform.architecture()[0][:2]
assert arch in ('32', '64')
_x86 = '_x86' if arch == '32' else ''

# Compatability with older arguments
opts = sys.argv[1:]
if opts[0:1] in (['32'], ['64']):
    if arch != opts[0]:
        raise Exception(f'{opts[0]}bit executable cannot be built on a {arch}bit system')
    opts = opts[1:]
opts = opts or ['--onefile']

print(f'Building {arch}bit version with options {opts}')

exec(compile(open('yt_dlp/version.py').read(), 'yt_dlp/version.py', 'exec'))
VERSION = locals()['__version__']

VERSION_LIST = VERSION.split('.')
VERSION_LIST = list(map(int, VERSION_LIST)) + [0] * (4 - len(VERSION_LIST))

print('Version: %s%s' % (VERSION, _x86))
print('Remember to update the version using devscipts/update-version.py')

def pycryptodome_module():
    try:
        import Cryptodome  # noqa: F401
    except ImportError:
        try:
            import Crypto  # noqa: F401
            print('WARNING: Using Crypto since Cryptodome is not available. '
                  'Install with: pip install pycryptodomex', file=sys.stderr)
            return 'Crypto'
        except ImportError:
            pass
    return 'Cryptodome'


dependancies = [pycryptodome_module(), 'mutagen', 'certifi'] + collect_submodules('websockets')
excluded_modules = ['test', 'ytdlp_plugins', 'youtube-dl', 'youtube-dlc']

PyInstaller.__main__.run([
    '--name=yt-dlp%s' % _x86,
    '--icon=devscripts/logo.ico',
    *[f'--exclude-module={module}' for module in excluded_modules],
    *[f'--hidden-import={module}' for module in dependancies],
    '--noconfirm',
    *opts,
    'yt_dlp/__main__.py',
])
