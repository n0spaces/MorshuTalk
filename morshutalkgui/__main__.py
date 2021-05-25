import sys
try:
    from PySide6.QtWidgets import QApplication
except ImportError:
    raise ImportError("The GUI requires PySide6 to run. Install it with 'pip install PySide6'")

try:
    from mainwindow import MainWindow
except ImportError:
    from .mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
