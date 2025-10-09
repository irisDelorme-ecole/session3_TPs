from PyQt6 import QtWidgets
from PyQt6.QtGui import QColor, QAction
from PyQt6.QtWidgets import  QDockWidget, QListView
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

    def __init__(self, model, parent):
        super().__init__(parent)

        loadUi("ui/listeFonctions.ui",self)

        self.fonctionsListView.setModel(model)




