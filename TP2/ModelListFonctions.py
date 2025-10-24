from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal
from ModelIntegration import IntegrationModel
from PyQt6.QtWidgets import QFileDialog
import json

class ModelListFonctions(QAbstractListModel):

    updatedSignal = pyqtSignal(bool)

    def __init__(self, data=None):

        super().__init__()
        if data is None:
            data = [IntegrationModel("x"), IntegrationModel("x**2"), IntegrationModel("x**3")] #default list
        self.__fonctions = data

    def to_dict(self):
        return {f"fonction {fonction.__str__()}": fonction.__str__() for fonction in self.__fonctions}

    def export(self):
        file_path, _ = QFileDialog.getSaveFileName(None,
            "Save File", "", "JSON files(*.json);;All Files(*)")

        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.to_dict(), file)
                file.close()
            print(f"List saved to {file_path}")
        else:
            print("Save operation canceled.")
        return json.dumps(self.__fonctions)

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
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.__fonctions.append(item)
        (self.endInsertRows())

    def removeItem(self, index):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        item = (self.__fonctions)[index]
        self.__fonctions.remove(item)
        (self.endInsertRows())
