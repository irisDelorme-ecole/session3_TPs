from PyQt6.QtGui import QColor, QAction
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QWidget, \
    QColorDialog, QMenu
from PyQt6.uic import loadUi
import sympy as sp
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from ModelIntegration import IntegrationModel
from MPLCanvas import MPLCanvas
import sys
from PyQt6.QtWidgets import QApplication




class View(QMainWindow):



    __model_integration:IntegrationModel

    def __init__(self):
        super().__init__()

        loadUi("ui/TP2MainWindow.ui", self)

        # setup de base
        self.fonction = IntegrationModel()
        canvas = MPLCanvas(self.fonction)
        self.toolbar = NavigationToolbar(canvas)
        layout = QVBoxLayout(self.plotWidget)
        layout.addWidget(self.toolbar)
        self.plotWidget.layout().addWidget(canvas)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex3 = View()
    ex3.show()
    sys.exit(app.exec())