import sys
import sounddevice as sd
from PySide6.QtGui import QCloseEvent
from pydub import AudioSegment
from PySide6.QtWidgets import QApplication, QMainWindow

from morshu import Morshu
from gui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.morshu = Morshu()

        self.audio_segment = AudioSegment.empty()
        self.audio_raw = self.audio_segment.raw_data
        self.samplerate = 18900

        self.playing = False

        self._audio_buff_pos = 0
        self._audio_buff_end = 0

        self.audio_current_time = 0

        # start audio stream
        self.audio_stream = sd.RawOutputStream(samplerate=self.samplerate,
                                               channels=1,
                                               dtype='int16',
                                               callback=self.stream_callback)

        self.ui.btn_load.clicked.connect(self.load_audio)
        self.ui.btn_play.clicked.connect(self.toggle_play)
        self.ui.slider.sliderMoved.connect(self.slider_moved)

    """The current index position in the raw audio buffer"""
    @property
    def audio_buff_pos(self) -> int:
        return self._audio_buff_pos

    """
    Sets the index in the raw audio buffer.
    This also updates elements in the gui, like the slider (unless it's currently clicked on.)
    """
    @audio_buff_pos.setter
    def audio_buff_pos(self, value):
        self._audio_buff_pos = value
        self.audio_current_time = self.audio_buff_pos / self.audio_segment.frame_rate / self.audio_segment.sample_width
        self.ui.lbl_time.setText("{:.2f}".format(self.audio_current_time))
        if not self.ui.slider.isSliderDown():
            self.ui.slider.setValue(
                self.audio_buff_pos // (self.audio_segment.channels * self.audio_segment.sample_width)
            )

    """Load the morshu tts with the text and update the audio fields"""
    def load_audio(self) -> None:
        self.playing = False
        self.audio_segment = self.morshu.load_text(self.ui.textedit.toPlainText())
        self.audio_raw = self.audio_segment.raw_data

        # set audio slider length
        self.ui.slider.setMaximum(
            len(self.audio_raw) // (self.audio_segment.channels * self.audio_segment.sample_width)
        )
        self.audio_buff_pos = 0

        self.ui.lbl_time_end.setText(
            "{:.2f}".format(len(self.audio_raw) / self.audio_segment.frame_rate / self.audio_segment.sample_width))

    """
    Set the audio buffer position to the value set by the user with the slider.
    The audio position will be equal to the value of the slider times the number of channels and the sample width of the
    audio segment.
    """
    def slider_moved(self) -> None:
        # TODO: sometimes impossible to set slider to min or max, need to fix that somehow
        self.audio_buff_pos = self.ui.slider.value() * self.audio_segment.channels * self.audio_segment.sample_width

    """Toggle the current playback"""
    def toggle_play(self) -> None:
        if self.playing:
            self.stop_audio()
        else:
            self.play_audio()

    """Start playing the audio. Starts the audio stream and sets the audio position to the beginning if necessary."""
    def play_audio(self) -> None:
        if len(self.audio_raw) > 0:
            self.ui.btn_play.setText("Stop")
            if self.audio_buff_pos >= len(self.audio_raw):
                self.audio_buff_pos = 0
            self.playing = True
            if self.audio_stream.stopped:
                self.audio_stream.start()

    """Stop playing the audio."""
    def stop_audio(self) -> None:
        self.ui.btn_play.setText("Play")
        self.playing = False

    """
    The sounddevice audio stream callback. This runs constantly while the stream is running.
    
    outdata should be set to the raw audio that we want to output. Its length of the audio slice must be equal to
    frames * channels * sample_width. If we don't want to output anything, then outdata should be set to all zeros.
    
    Assigning the buffer data to the outdata variable won't work; use indexing instead (outdata[:] = data). 
    """
    def stream_callback(self, outdata: bytes, frames: int, _time, _status) -> None:
        slice_len = (frames * self.audio_segment.channels * self.audio_segment.sample_width)

        # not playing
        if not self.playing:
            outdata[:] = b'\x00' * slice_len
            return

        # end of audio was already reached, stop playing
        if self.audio_buff_pos >= len(self.audio_raw):
            outdata[:] = b'\x00' * slice_len
            self.audio_buff_pos = len(self.audio_raw)
            self.stop_audio()
            return

        # slider is pressed, play silence and don't advance audio position but don't stop playback
        if self.ui.slider.isSliderDown():
            outdata[:] = b'\x00' * slice_len
            return

        start = self.audio_buff_pos
        end = start + slice_len
        if end > len(self.audio_raw):
            outdata[:] = self.audio_raw[start:] + b'\x00' * (end - len(self.audio_raw))
        else:
            outdata[:] = self.audio_raw[start:end]
        self.audio_buff_pos = end

    """Safely stop and close the audio stream before closing the window"""
    def closeEvent(self, event: QCloseEvent) -> None:
        self.audio_stream.stop()
        self.audio_stream.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
