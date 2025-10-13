from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QAction
from PyQt6.QtWidgets import QDockWidget, QListView, QLineEdit, QPushButton
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIntValidator
import sympy as sp
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from ModelIntegration import IntegrationModel
from MPLCanvas import MPLCanvas
import sys
from PyQt6.QtWidgets import QApplication

class ViewListFonction(QDockWidget):

    fonctionsListView: QListView
    fonctionLineEdit: QLineEdit
    ajouterPushButton:QPushButton
    supprimerPushButton:QPushButton
    enregistrerPushButton:QPushButton

    def __init__(self, model, parent):
        super().__init__(parent)

        loadUi("ui/listeFonctions.ui",self)

        self.fonctionsListView.setModel(model)

        self.model = model

        #fonctionnement
        self.fonctionLineEdit.textEdited.connect(self.setAjouter)

        self.ajouterPushButton.clicked.connect(self.addFonction)


    # def updateModel(self, boolean):
    #     print("got into update")
    #     self.fonctionsListView.update()

    def setAjouter(self):
        self.ajouterPushButton.setEnabled(True)

    def addFonction(self):
        self.model.addItem(str(self.fonctionLineEdit.text()))


