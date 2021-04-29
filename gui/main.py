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
        self.audio_raw = self.audio_segment.raw_data
        self.samplerate = 18900

        self.audio_buff_pos = 0

        # start audio stream
        self.audio_stream = sd.RawOutputStream(samplerate=self.samplerate,
                                               channels=1,
                                               dtype='int16',
                                               callback=self.stream_callback)

        self.ui.btn_load.clicked.connect(self.btn_load_clicked)
        self.ui.btn_play.clicked.connect(self.btn_play_clicked)

    def btn_load_clicked(self):
        self.audio_segment = morshu_tts(self.ui.textedit.toPlainText())
        self.audio_raw = self.audio_segment.raw_data
        self.samplerate = self.audio_segment.frame_rate

    def btn_play_clicked(self):
        if self.audio_stream.stopped:
            self.audio_stream.start()
        else:
            self.audio_stream.stop()
            self.audio_buff_pos = 0

    def stream_callback(self, outdata: bytes, frames: int, _time, _status):
        self.ui.lbl_time.setText(str(self.audio_buff_pos / self.samplerate / self.audio_segment.sample_width))
        slice_len = (frames * self.audio_segment.channels * self.audio_segment.sample_width)

        if self.audio_buff_pos > len(self.audio_raw):
            outdata[:] = b'\x00' * slice_len
            # stopping is slow
            self.audio_stream.stop()
            self.audio_buff_pos = 0
            return

        start = self.audio_buff_pos
        end = start + slice_len
        if end > len(self.audio_raw):
            outdata[:] = self.audio_raw[start:] + b'\x00' * (end - len(self.audio_raw))
        else:
            outdata[:] = self.audio_raw[start:end]
        self.audio_buff_pos = end


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
