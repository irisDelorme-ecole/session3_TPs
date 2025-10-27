import sys
import traceback

from PyQt6.QtWidgets import QApplication

from View import View

if __name__ == "__main__":
    def qt_exception_hook(exctype, value, tb):
        traceback.print_exception(exctype, value, tb)


    sys.excepthook = qt_exception_hook
    app = QApplication(sys.argv)

    with open('ui/style.qss', 'r') as file:
        style = file.read()
    app.setStyleSheet(style)


    ex3 = View()
    ex3.show()
    sys.exit(app.exec())
