# MorshuTalk

A [Morshu](https://knowyourmeme.com/memes/morshu) text-to-speech program.

![](screenshot.png)

This program works by converting the given text into phonemes with [g2p_en](https://pypi.org/project/g2p-en/), then
concatenates the segments of Morshu's audio where he speaks those phonemes.

## Requirements
Python 3.7+ (tested on Windows, should also work on Linux and macOS)

Python is not required if you're just using the MorshuTalk executable.

## Installation
### Windows Executable
If you're on Windows and you don't want to install Python, you can download an executable from the
[latest release on GitHub](https://github.com/n0spaces/MorshuTalk/releases/latest). Simply download the 7z or ZIP
archive (they're both identical) and extract it.

### Python Package
If you have Python installed, you can install this with `pip`:

    pip install morshutalk

Or you can clone this repo and run the setup script:

    python setup.py install

This installs all the packages necessary for running MorshuTalk from the command-line. If you want to use the GUI, you
will also need to install PySide6. (It's not included by default because it's a slightly larger download.)

    pip install PySide6

## Running
### Windows Executable
Just run `MorshuTalk.exe` to start the GUI.

### Python Package
Installing the package will add the commands `morshutalk` and `morshutalkgui` to your command-line. If those commands
don't work, you can run the modules with `python -m morshutalk` or `python -m morshutalkgui`.

#### Python package quickstart 
```
from morshutalk.morshu import Morshu
morshu = morshu()
text = "Hello world"
audio = morshu.load_text(text)
audio.export("output.mp3", format="mp3") # to save as a file

from sounddevice import play
play(audio.get_array_of_samples(), audio.frame_rate) # to play audio
```

#### Command-Line
Run `morshutalk` to load the interactive command-line app. Simply type whatever lines you want Morshu to speak, then he
will talk. To exit, leave the line blank and hit enter.

#### GUI
Run `morshutalkgui` to load the GUI app. Remember that PySide6 is required.

Type text into the textbox, then click Load to load the audio. Click Play to hear the audio. The Morshu sprite will
animate as he speaks. You can toggle the sprite visibility from the View menu.

## Building
1. Clone this repo.
2. Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and activate it.
3. Install the required packages with `pip install -r requirements.txt`
4. If you make changes to `mainwindow.ui`, update `ui_mainwindow.py` with:
```commandline
pyside6-uic morshutalkgui/ui/mainwindow.ui -o morshutalkgui/ui_mainwindow.py --from-imports
```
5. If you make changes to `res.qrc`, update `res_rc.py` with:
```commandline
pyside6-rcc morshutalkgui/res/res.qrc -o morshutalkgui/res_rc.py
```
6. Use `build` to create a distributable package:
    1. Install it with `pip install build`
    2. Run `python -m build`. A tar.gz and wheel package should be located in the `dist` folder.
7. Use cx_freeze to build an executable for Windows:
    1. Install it with `pip install cx_freeze`
    2. Run `python freeze_setup.py build`. The executable and many other files should be located in the `build` folder.
    3. Run `python clean_cx_freeze_build.py` to remove unnecessary files. (cx_freeze does a bad job at choosing what
       packages are necessary. This script removes 150+ MB of unused files.)

## License
[MIT License](LICENSE.txt)

This uses the following libraries:
* [g2p_en](https://pypi.org/project/g2p-en/)
* [NumPy](https://numpy.org/)
* [Pydub](http://pydub.com/)
* [sounddevice](https://pypi.org/project/sounddevice/)
* [PySide 6 (Qt for Python)](https://wiki.qt.io/Qt_for_Python)
