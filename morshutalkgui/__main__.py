print("Loading MorshuTalk...")

import sys

import nltk
from PySide6.QtWidgets import QApplication, QStyleFactory

from morshutalkgui.mainwindow import MainWindow


def main():
    nltk.download("averaged_perceptron_tagger_eng")

    app = QApplication(sys.argv)
    if "windowsvista" in QStyleFactory:
        app.setStyle("windowsvista")

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
