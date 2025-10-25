from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal
from ModelIntegration import IntegrationModel
from PyQt6.QtWidgets import QMessageBox
import json

class ModelListFonctions(QAbstractListModel):

    updatedSignal = pyqtSignal(bool)

    def __init__(self):

        super().__init__()


        self.__fonctions = []
        self.from_dict()

    def to_dict(self):
        dict = {}
        for i in range(len(self.__fonctions)):
            dict[str(i)] = self.__fonctions[i].__str__()
        return dict


    def from_dict(self):
        with open('data\listefonctions.json') as json_file:
            data = json.load(json_file)
        if data.__len__() == 0:
            pass
        else:
            for i in range(data.__len__()):
                self.addItem(IntegrationModel(data[str(i)]))

    def export(self):
        with open("data\listeFonctions.json", 'w') as file:
                json.dump(self.to_dict(), file)
                file.close()
        QMessageBox.information(QMessageBox(), "Message", "Liste de fonctions sauvegardée")


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
        if index < self.__fonctions.__len__():
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            item = self.__fonctions[index]
            self.__fonctions.remove(item)
            (self.endInsertRows())
