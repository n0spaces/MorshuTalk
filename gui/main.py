import sys
import sounddevice as sd
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMainWindow

from morshu import Morshu
from gui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.morshu = Morshu()

        self.playing = False

        self._audio_buff_pos = 0
        self._audio_buff_end = 0

        self.audio_current_time = 0

        # start audio stream
        self.audio_stream = sd.RawOutputStream(samplerate=18900,
                                               channels=1,
                                               dtype='int16',
                                               callback=self.stream_callback)

        self.ui.btn_load.clicked.connect(self.load_audio)
        self.ui.btn_play.clicked.connect(self.toggle_play)
        self.ui.slider.sliderMoved.connect(self.slider_moved)

    @property
    def audio_buff_pos(self) -> int:
        """The current index position in the raw audio buffer"""
        return self._audio_buff_pos

    @audio_buff_pos.setter
    def audio_buff_pos(self, value):
        """
        Sets the index in the raw audio buffer.
        This also updates elements in the gui, like the slider (unless it's currently clicked on.)
        """
        self._audio_buff_pos = value
        self.audio_current_time = (self.audio_buff_pos / self.morshu.out_audio.frame_rate /
                                   self.morshu.out_audio.sample_width)
        self.ui.lbl_time.setText("{:.2f}".format(self.audio_current_time))
        if not self.ui.slider.isSliderDown():
            self.ui.slider.setValue(
                self.audio_buff_pos // (self.morshu.out_audio.channels * self.morshu.out_audio.sample_width)
            )

    def load_audio(self) -> None:
        """Load the morshu tts with the text and update the audio fields"""
        self.playing = False
        self.morshu.load_text(self.ui.textedit.toPlainText())

        # set audio slider length
        self.ui.slider.setMaximum(
            len(self.morshu.out_audio.raw_data) // (self.morshu.out_audio.channels * self.morshu.out_audio.sample_width)
        )
        self.audio_buff_pos = 0

        self.ui.lbl_time_end.setText(
            "{:.2f}".format(len(self.morshu.out_audio.raw_data) / self.morshu.out_audio.frame_rate /
                            self.morshu.out_audio.sample_width))

    def slider_moved(self) -> None:
        """
        Set the audio buffer position to the value set by the user with the slider.
        The audio position will be equal to the value of the slider times the number of channels and the sample width of
        the audio segment.
        """
        # TODO: sometimes impossible to set slider to min or max, need to fix that somehow
        self.audio_buff_pos = (self.ui.slider.value() * self.morshu.out_audio.channels *
                               self.morshu.out_audio.sample_width)

    def toggle_play(self) -> None:
        """Toggle the current playback"""
        if self.playing:
            self.stop_audio()
        else:
            self.play_audio()

    def play_audio(self) -> None:
        """
        Start playing the audio. Starts the audio stream and sets the audio position to the beginning if necessary.
        """
        if len(self.morshu.out_audio.raw_data) > 0:
            self.ui.btn_play.setText("Stop")
            if self.audio_buff_pos >= len(self.morshu.out_audio.raw_data):
                self.audio_buff_pos = 0
            self.playing = True
            if self.audio_stream.stopped:
                self.audio_stream.start()

    def stop_audio(self) -> None:
        """Stop playing the audio."""
        self.ui.btn_play.setText("Play")
        self.playing = False

    def stream_callback(self, outdata: bytes, frames: int, _time, _status) -> None:
        """
        The sounddevice audio stream callback. This runs constantly while the stream is running.

        outdata should be set to the raw audio that we want to output. Its length of the audio slice must be equal to
        frames * channels * sample_width. If we don't want to output anything, then outdata should be set to all zeros.

        Assigning the buffer data to the outdata variable won't work; use indexing instead (outdata[:] = data).
        """
        slice_len = (frames * self.morshu.out_audio.channels * self.morshu.out_audio.sample_width)

        # not playing
        if not self.playing:
            outdata[:] = b'\x00' * slice_len
            return

        # end of audio was already reached, stop playing
        if self.audio_buff_pos >= len(self.morshu.out_audio.raw_data):
            outdata[:] = b'\x00' * slice_len
            self.audio_buff_pos = len(self.morshu.out_audio.raw_data)
            self.stop_audio()
            return

        # slider is pressed, play silence and don't advance audio position but don't stop playback
        if self.ui.slider.isSliderDown():
            outdata[:] = b'\x00' * slice_len
            return

        start = self.audio_buff_pos
        end = start + slice_len
        if end > len(self.morshu.out_audio.raw_data):
            outdata[:] = self.morshu.out_audio.raw_data[start:] + b'\x00' * (end - len(self.morshu.out_audio.raw_data))
        else:
            outdata[:] = self.morshu.out_audio.raw_data[start:end]
        self.audio_buff_pos = end

    def closeEvent(self, event: QCloseEvent) -> None:
        """Safely stop and close the audio stream before closing the window"""
        self.audio_stream.stop()
        self.audio_stream.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
