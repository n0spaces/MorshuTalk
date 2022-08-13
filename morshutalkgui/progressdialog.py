from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QProgressDialog


class ProgressDialog(QProgressDialog):
    def __init__(self, parent):
        super().__init__("Loading text...", "Cancel", 0, 1, parent)
        self.setWindowTitle("Loading...")
        self.setWindowModality(Qt.WindowModal)
        self.setMinimumDuration(1000)
        super().reset()

        self.update_text_timer = QTimer(self)
        self.update_text_timer.setInterval(100)

        self.canceled.connect(lambda: self.update_text_timer.stop())
        self.update_text_timer.timeout.connect(self.update_text)

        self.overall_step = 1

    def reset(self) -> None:
        super().reset()
        self.overall_step = 1
        self.update_text_timer.start()

    def update_text(self):
        if self.overall_step == 1:
            text = "Converting text... (Step 1 of 2)\n"
        elif self.overall_step == 2:
            text = "Loading audio... (Step 1 of 2)\n"
        else:
            text = "Loading..."
        text += "{} out of {}".format(self.value(), self.maximum())
        self.setLabelText(text)
