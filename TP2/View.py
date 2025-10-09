from PyQt6.QtGui import QColor, QAction
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QWidget, \
    QColorDialog, QMenu
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIntValidator
import sympy as sp
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from ModelIntegration import IntegrationModel
from MPLCanvas import MPLCanvas
import sys
from PyQt6.QtWidgets import QApplication




class View(QMainWindow):

    __calculerPushButton:QPushButton
    __borneInfLineEdit:QLineEdit
    __borneSupLineEdit:QLineEdit


    fonction:IntegrationModel

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


        #fonctionnement
        self.validatorInf = QIntValidator(self)

        self.borneInfLineEdit.setValidator(self.validatorInf)

        self.validatorSup = QIntValidator(self)

        self.borneSupLineEdit.setValidator(self.validatorSup)

        

      #  self.__borneSupLineEdit.textChanged.connect(self.validate_sup)
        self.borneInfLineEdit.textEdited.connect(self.validate_inf)


    def validate_inf(self, texte):
        state, _, _ = self.validatorInf.validate(texte, 0)

        if state == QIntValidator.State.Acceptable:
            self.borneInfLineEdit.setStyleSheet("background-color: white;")
            self.fonction.borne_inf = self.borneInfLineEdit.text()
            print(self.fonction.borne_inf)
        else:
            self.borneInfLineEdit.setStyleSheet("background-color: lightcoral;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex3 = View()
    ex3.show()
    sys.exit(app.exec())