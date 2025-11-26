import time
import networkx as nx
from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar


class PlusCourtChemin(QThread):
    chemin = pyqtSignal(list)
    fini_chemin = pyqtSignal(str)

    def __init__(self, debut, fin, graphe:nx.Graph):
        super().__init__()

        self._debut = debut
        self._fin = fin
        self._graphe = graphe

    def run(self):
        chemin = []
        progress = 0
        try:
            chemin_temp = nx.shortest_path(self._graphe, self._debut, self._fin)

            while progress < len(chemin_temp):
                chemin.append(chemin_temp[progress])
                progress += 1

                time.sleep(1)
                self.chemin.emit(chemin)
            time.sleep(1)
            self.fini_chemin.emit("")

        except Exception as e:
            self.chemin.emit([])


class Parcourir(QThread):
    progress_parcours = pyqtSignal(int, int)
    signal_fini = pyqtSignal(str)

    def __init__(self, graphe:nx.Graph):
        super().__init__()
        self._graphe = graphe

    def run(self):
        progress = 0
        for node in self._graphe.nodes:
            progress += 1
            time.sleep(1)
            self.progress_parcours.emit(node, progress)
        time.sleep(2)
        self.signal_fini.emit('fin')


class PopupWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("Progress")
        self.setGeometry(100, 600, 250, 75)

        layout = QVBoxLayout()
        label = QLabel(text)
        self.progress = QProgressBar()
        layout.addWidget(label)
        layout.addWidget(self.progress)
        self.setLayout(layout)