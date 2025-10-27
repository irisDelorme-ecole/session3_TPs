from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QDockWidget, QListView, QLineEdit, QPushButton, QMessageBox, QSizePolicy
from PyQt6.uic import loadUi
import sympy as sp
from PyQt6.uic.properties import QtCore

from ModelIntegration import IntegrationModel
from ModelListFonctions import LatexDelegate


class ViewListFonction(QDockWidget):
    fonctionsListView: QListView
    fonctionLineEdit: QLineEdit
    ajouterPushButton: QPushButton
    supprimerPushButton: QPushButton
    enregistrerPushButton: QPushButton

    def __init__(self, model, parent):
        super().__init__(parent)

        loadUi("ui/listeFonctions.ui", self)

        #make cute
        self.fonctionsListView.setStyleSheet("background-color : #99afd7")
        self.fonctionLineEdit.setStyleSheet("color : #233c67")
        self.setStyleSheet("background-color : #ccdbee")

        self.fonctionsListView.setModel(model)

        self.model = model

        self.setFloating(True)

        # Delegate: tune desired_height to control rendered size (j'ai choisi 18, 50 et 4 parce qu'après plusieurs test ce semblait comme les meilleurs.)
        self.delegate = LatexDelegate(self, pixmap_fontsize=18, desired_height=50, padding=4)


        #assigne le delegate latex à mon listview
        self.fonctionsListView.setItemDelegate(self.delegate)
        self.fonctionsListView.setSpacing(6)
        # fonctionnement
        self.update_button_state()
        self.fonctionLineEdit.textEdited.connect(self.update_button_state)


        self.enregistrerPushButton.clicked.connect(self.model.export)

        self.fonctionsListView.clicked.connect(self.update_button_state)

        self.ajouterPushButton.clicked.connect(self.addFonction)

        self.supprimerPushButton.clicked.connect(self.removeFonction)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.addFonction()
        elif event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self.removeFonction()
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_S:
            self.model.export()
        else:
            pass

    def update_button_state(self):
        self.ajouterPushButton.setEnabled(self.fonctionLineEdit.text() != "")
        self.supprimerPushButton.setEnabled(self.fonctionsListView.selectionModel().hasSelection())
        self.enregistrerPushButton.setEnabled(self.model.rowCount()>0)

    def addFonction(self):
        x = sp.symbols('x')
        if sp.sympify(str(self.fonctionLineEdit.text())).free_symbols <= {x}:
            self.model.addItem(IntegrationModel(str(self.fonctionLineEdit.text())))
        else:
            QMessageBox.critical(QMessageBox(), "Invalid Function",
                                 "la fonction ne respecte pas le format d'une expression sympy en fonction de x.")

        self.update_button_state()

    def removeFonction(self):
        self.model.removeItem((QModelIndex(self.fonctionsListView.selectedIndexes()[0]).row()))
        self.update_button_state()
