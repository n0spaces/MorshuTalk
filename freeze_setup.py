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

    'PySide6.QtPrintSupport',
    'PySide6.QtSql',
    'PySide6.QtNetwork',
    'PySide6.QtTest',
    'PySide6.QtConcurrent',
    'PySide6.QtXml',
    'PySide6.QtHelp',
    'PySide6.QtOpenGL',
    'PySide6.QtOpenGLFunctions',
    'PySide6.QtOpenGLWidgets',
    'PySide6.QtQml',
    'PySide6.QtQuick',
    'PySide6.QtQuickControls2',
    'PySide6.QtQuickWidgets',
    'PySide6.QtSvg',
    'PySide6.QtSvgWidgets',
    'PySide6.QtUiTools',
    'PySide6.Qt3DCore',
    'PySide6.Qt3DRender',
    'PySide6.Qt3DInput',
    'PySide6.Qt3DLogic',
    'PySide6.Qt3DAnimation',
    'PySide6.Qt3DExtras'
]

build_options = {'packages': [], 'excludes': exclude_packages}

base = None
# base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    cx_Freeze.Executable('morshutalkgui\\__main__.py', base=base, target_name='MorshuTalk')
]

cx_Freeze.setup(name='MorshuTalk',
                version='0.0.1',
                description='Morshu TTS',
                options={'build_exe': build_options},
                executables=executables)