from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QPushButton, QMainWindow, QVBoxLayout, QSpinBox, QProgressBar, QComboBox, QLineEdit
from PyQt6.uic import loadUi
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controller.main_controller import MainController  # uniquement pour

class MainWindow(QMainWindow):
    grapheLayout:QVBoxLayout

    createButton: QPushButton
    deleteButton: QPushButton
    nbrNodes:QSpinBox

    edgesComboBox:QComboBox
    weightSpinBox:QSpinBox
    deleteEdgeButton:QPushButton

    debutSpinBox:QSpinBox
    finSpinBox:QSpinBox
    tracerPushButton:QPushButton

    signal_parcourir = pyqtSignal(str)



    def __init__(self):
        super().__init__()

        loadUi("view/ui/main_window.ui", self)
        self.resize(1000,800)
        #self.draw_graphe()
        if TYPE_CHECKING:
            self.__controller: MainController | None = None

        self.finSpinBox.setValue(9)
        self.nbrNodes.setValue(10)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_P:
            self.signal_parcourir.emit("parcourir")

    def add_canvas(self, canvas):
        #  insérer le canvas dans le layout
        self.grapheLayout.addWidget(canvas)

    def set_controller(self,controller):
        self.__controller = controller