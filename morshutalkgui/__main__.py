print("Loading MorshuTalk...")

import sys
from PySide6.QtWidgets import QApplication

from morshutalkgui.mainwindow import MainWindow

import nltk


def main():
    nltk.download("averaged_perceptron_tagger_eng")

    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
