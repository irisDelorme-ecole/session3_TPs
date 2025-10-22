from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QAction, QTextDocument, QPainter, QPixmap
import matplotlib.pyplot as plt
import io
from PyQt6.QtWidgets import QDockWidget, QListView, QLineEdit, QPushButton, QStyledItemDelegate
from PyQt6.uic import loadUi
from PyQt6.QtGui import QIntValidator
import sympy as sp
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from ModelIntegration import IntegrationModel
from MPLCanvas import MPLCanvas
import sys
from PyQt6.QtWidgets import QApplication

# Custom Delegate to render the pixmap
class PlotDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        pixmap = index.data(Qt.ItemDataRole.DecorationRole)
        if pixmap:
            painter.drawPixmap(option.rect, pixmap)

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

        self.setFloating(True)
        #fonctionnement
        self.fonctionLineEdit.textEdited.connect(self.setAjouter)

        self.ajouterPushButton.clicked.connect(self.addFonction)



    # def updateModel(self, boolean):
    #     print("got into update")
    #     self.fonctionsListView.update()

    def setAjouter(self):
        self.ajouterPushButton.setEnabled(True)

    def addFonction(self):
        self.model.addItem(IntegrationModel(str(self.fonctionLineEdit.text())))


