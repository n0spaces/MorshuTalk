import cx_Freeze

# no idea why cx_freeze includes soooo many unneeded packages
# i'd exclude more but shiboken (pyside6) needs them for some reason
exclude_packages = [
    'asyncio',
    'certifi',
    'cffi',
    'chardet',
    'concurrent',
    'curses',
    'distutils',
    'idna',
    'joblib',
    'lib2to3',
    'msilib',
    'multiprocessing',
    'networkx',
    'pycparser',
    'pydoc_data',
    'pyreadline',
    'pytz',
    'requrests',
    'scipy',
    'setuptools',
    'test',
    'tkinter',
    'tqdm',
    'unittest',
    'urllib3',
    'xmlrpc',
    'yaml',
]

include_packages = [
    'secrets',
]

build_options = {
    'excludes': exclude_packages,
    'includes': include_packages,
    'include_files': [('thirdparty.txt', ''), ('LICENSE.txt', '')]
}

base = None
# base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    cx_Freeze.Executable('morshutalkgui\\__main__.py', base=base, target_name='MorshuTalk')
]

cx_Freeze.setup(name='MorshuTalk',
                version='0.0.2',
                description='Morshu TTS',
                options={'build_exe': build_options},
                executables=executables)
