from PySide6.QtCore import QThread, Signal

from morshutalk import Morshu


class MorshuWorker(QThread):
    """Background thread for loading Morshu audio to avoid UI blocking"""

    done = Signal(bool)
    """Emitted when audio is done loading. True if successful, False if an exception occured."""

    step = Signal(int, int)

    def __init__(self, morshu: Morshu):
        super().__init__()
        self.morshu = morshu
        self.exception: Exception | None = None

    # noinspection PyUnresolvedReferences
    # the PySide type stubs don't understand Signals for some reason
    def run(self) -> None:
        """
        Start loading the text. morshu.input_str must be set first.

        Don't use this method. Use start() instead so it runs in a background thread.
        """
        try:
            self.morshu.load_text(progress_callback=lambda x, y: self.step.emit(x, y))
        except Exception as e:
            print(e)
            self.exception = e
            self.done.emit(False)

        self.done.emit(True)
