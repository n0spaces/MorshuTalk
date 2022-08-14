# cx_freeze does a bad job at determining what files it needs to keep, so this script does that manually after building.
# This saves 150+ MB.
# I'm using windirstat to search for large files to remove. This can probably be improved.

import os
import shutil
from glob import glob

if not os.path.exists('build'):
    print("could not find build path")
    exit(1)

win_amd64_pyside6_keep = (
    glob(r'build\exe.win*\lib\PySide6\plugins\platforms\qwindows.dll') +
    glob(r'build\exe.win*\lib\PySide6\plugins\styles\qwindowsvistastyle.dll') +
    glob(r'build\exe.win*\lib\PySide6\pyside6.abi3.dll') +
    glob(r'build\exe.win*\lib\PySide6\Qt6Core.dll') +
    glob(r'build\exe.win*\lib\PySide6\Qt6Gui.dll') +
    glob(r'build\exe.win*\lib\PySide6\Qt6Network.dll') +
    glob(r'build\exe.win*\lib\PySide6\Qt6OpenGL.dll') +
    glob(r'build\exe.win*\lib\PySide6\Qt6Qml.dll') +
    glob(r'build\exe.win*\lib\PySide6\Qt6Widgets.dll') +
    glob(r'build\exe.win*\lib\PySide6\QtCore.pyd') +
    glob(r'build\exe.win*\lib\PySide6\QtGui.pyd') +
    glob(r'build\exe.win*\lib\PySide6\QtWidgets.pyd') +
    glob(r'build\exe.win*\lib\PySide6\__init__.pyc')
)

win_amd64_paths_delete = (
    glob(r'build\exe.win*\lib\morshutalkgui\res') +
    glob(r'build\exe.win*\lib\morshutalkgui\ui') +
    glob(r'build\exe.win*\lib\numpy\core\include') +
    glob(r'build\exe.win*\lib\numpy\core\lib')
)
win_amd64_paths_delete.extend(glob(r'build\exe.win*\lib\**\tests', recursive=True))
win_amd64_paths_delete.extend(glob(r'build\exe.win*\lib\**\test', recursive=True))

win_amd64_files_delete = (
    glob(r'build\exe.win-amd64-3.9\lib\numpy\core\python39.dll') +
    glob(r'build\exe.win-amd64-3.9\lib\**\python??.dll', recursive=True) +
    glob(r'build\exe.win-amd64-3.9\lib\**\*.c', recursive=True) +
    glob(r'build\exe.win-amd64-3.9\lib\**\*.h', recursive=True)
)

for path in win_amd64_paths_delete:
    shutil.rmtree(path, True)

for file in win_amd64_files_delete:
    if os.path.exists(file):
        print("deleting " + file)
        os.remove(file)

for subdir, dirs, files in os.walk(glob('build/exe.win*/lib/PySide6')[0]):
    for file in files:
        path = os.path.normpath(os.path.join(subdir, file))
        if not any(path == os.path.normpath(p) for p in win_amd64_pyside6_keep):
            print("deleting " + path)
            os.remove(path)
