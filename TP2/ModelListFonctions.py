from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex
from ModelIntegration import IntegrationModel

class ModelListFonctions(QAbstractListModel):

    def __init__(self):

        super().__init__()

        self.__fonctions = [IntegrationModel("x"), IntegrationModel("x**2"), IntegrationModel("x**3")]


    def data(self, index, role = ...):

        if not index.isValid():
            return None
        fonction = self.__fonctions[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return fonction.__str__()
        elif role == Qt.ItemDataRole.UserRole:
            return fonction
        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self.__fonctions)

    def addItem(self, item):
        self.__fonctions.append(item)