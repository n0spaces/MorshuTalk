# cx_freeze does a bad job at determining what files it needs to keep, so this script does that manually after building.
# This saves 150+ MB.
# I'm using windirstat to search for large files to remove. This can probably be improved.

import os
import shutil
from glob import glob

if not os.path.exists('build'):
    print("could not find build path")
    exit(1)

win_amd64_pyside6_keep = [
    r'build\exe.win-amd64-3.9\lib\PySide6\plugins\platforms\qwindows.dll',
    r'build\exe.win-amd64-3.9\lib\PySide6\plugins\styles\qwindowsvistastyle.dll',
    r'build\exe.win-amd64-3.9\lib\PySide6\pyside6.abi3.dll',
    r'build\exe.win-amd64-3.9\lib\PySide6\Qt6Core.dll',
    r'build\exe.win-amd64-3.9\lib\PySide6\Qt6Gui.dll',
    r'build\exe.win-amd64-3.9\lib\PySide6\Qt6Network.dll',
    r'build\exe.win-amd64-3.9\lib\PySide6\Qt6OpenGL.dll',
    r'build\exe.win-amd64-3.9\lib\PySide6\Qt6Qml.dll',
    r'build\exe.win-amd64-3.9\lib\PySide6\Qt6Widgets.dll',
    r'build\exe.win-amd64-3.9\lib\PySide6\QtCore.pyd',
    r'build\exe.win-amd64-3.9\lib\PySide6\QtGui.pyd',
    r'build\exe.win-amd64-3.9\lib\PySide6\QtWidgets.pyd',
    r'build\exe.win-amd64-3.9\lib\PySide6\__init__.pyc'
]

win_amd64_paths_delete = [
    r'build\exe.win-amd64-3.9\lib\morshutalkgui\res',
    r'build\exe.win-amd64-3.9\lib\morshutalkgui\ui',
    r'build\exe.win-amd64-3.9\lib\numpy\core\include',
    r'build\exe.win-amd64-3.9\lib\numpy\core\lib',
]
win_amd64_paths_delete.extend(glob(r'build\exe.win-amd64-3.9\lib\**\tests', recursive=True))
win_amd64_paths_delete.extend(glob(r'build\exe.win-amd64-3.9\lib\**\test', recursive=True))

win_amd64_files_delete = [
    r'build\exe.win-amd64-3.9\lib\numpy\core\python39.dll'
]
win_amd64_files_delete.extend(glob(r'build\exe.win-amd64-3.9\lib\**\python??.dll', recursive=True))
win_amd64_files_delete.extend(glob(r'build\exe.win-amd64-3.9\lib\**\*.c', recursive=True))
win_amd64_files_delete.extend(glob(r'build\exe.win-amd64-3.9\lib\**\*.h', recursive=True))

for path in win_amd64_paths_delete:
    shutil.rmtree(path, True)

for file in win_amd64_files_delete:
    if os.path.exists(file):
        os.remove(file)

for subdir, dirs, files in os.walk('build/exe.win-amd64-3.9/lib/PySide6'):
    for file in files:
        path = os.path.normpath(os.path.join(subdir, file))
        if not any(path == os.path.normpath(p) for p in win_amd64_pyside6_keep):
            os.remove(path)
