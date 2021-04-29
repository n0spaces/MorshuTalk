import sys
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
from PySide6.QtWidgets import QApplication, QMainWindow

from morshu import morshu_tts
from ui_mainwindow import Ui_MainWindow


"""
current_pos = 0
def callback(in_data, frame_count, time_info, status):
    global current_pos
    start = current_pos
    end = start + (frame_count * morshu_wav.channels * morshu_wav.sample_width)
    data = raw[start:end]
    current_pos = end
    return data, pyaudio.paContinue
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.audio_segment = AudioSegment.empty()
        self.audio_arr = np.array([])
        self.samplerate = 18900

        self.ui.btn_load.clicked.connect(self.btn_load_clicked)
        self.ui.btn_play.clicked.connect(self.btn_play_clicked)

    def btn_load_clicked(self):
        self.audio_segment = morshu_tts(self.ui.textedit.toPlainText())
        self.audio_arr = np.array(self.audio_segment.get_array_of_samples())
        self.samplerate = self.audio_segment.frame_rate

    def btn_play_clicked(self):
        active = False
        try:
            active = sd.get_stream().active
        except RuntimeError:
            pass

        if active:
            sd.stop()
        else:
            sd.play(self.audio_arr, self.samplerate)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
