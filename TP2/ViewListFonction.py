from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QDockWidget, QListView, QLineEdit, QPushButton, QMessageBox
from PyQt6.uic import loadUi
import sympy as sp
from ModelIntegration import IntegrationModel
from TP2.ModelListFonctions import LatexDelegate


# Custom Delegate to render the pixmap
# class PlotDelegate(QStyledItemDelegate):
#     def paint(self, painter, option, index):
#         pixmap = index.data(Qt.ItemDataRole.DecorationRole)
#         if pixmap:
#             painter.drawPixmap(option.rect, pixmap)

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

        # Delegate: tune desired_height to control rendered size
        self.delegate = LatexDelegate(self, pixmap_fontsize=18, desired_height=50, padding=4)

        self.fonctionsListView.setItemDelegate(self.delegate)
        self.fonctionsListView.setSpacing(6)
        #fonctionnement
        self.fonctionLineEdit.textEdited.connect(self.setAjouter)

        self.enregistrerPushButton.setEnabled(True)
        self.enregistrerPushButton.clicked.connect(self.model.export)

        self.fonctionsListView.clicked.connect(self.activateSupprimer)

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

    def setAjouter(self):
        self.ajouterPushButton.setEnabled(True)

    def activateSupprimer(self):
        self.supprimerPushButton.setEnabled(True)

    def addFonction(self):
        x = sp.symbols('x')
        if sp.sympify(str(self.fonctionLineEdit.text())).free_symbols <= {x}:
            self.model.addItem(IntegrationModel(str(self.fonctionLineEdit.text())))
        else:
            QMessageBox.critical(QMessageBox(),"Invalid Function", "la fonction ne respecte pas le format d'une expression sympy.")



    def removeFonction(self):
        self.model.removeItem((QModelIndex(self.fonctionsListView.selectedIndexes()[0]).row()))

