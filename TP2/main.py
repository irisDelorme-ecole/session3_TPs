import sys
import traceback

from PyQt6.QtWidgets import QApplication

from View import View


def qt_exception_hook(exctype, value, tb):
    traceback.print_exception(exctype, value, tb)

sys.excepthook = qt_exception_hook
app = QApplication(sys.argv)
ex3 = View()
ex3.show()
sys.exit(app.exec())