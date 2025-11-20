import time

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QProgressBar

from model.graphe_model import GrapheModel
from view.GrapheCanvas import GraphCanvas
from view.MainWindow import MainWindow


class MainController :
    __view:MainWindow
    __model:GrapheModel
    __canvas:GraphCanvas

    def __init__(self,view,model,canvas):
        self.__view = view
        self.__model = model
        self.__canvas = canvas

        # Connecter le bouton de creation de graphe
        self.__view.createButton.clicked.connect(self.generate_graph)
        self.__view.deleteButton.clicked.connect(self.delete_graph)
        self.__view.debutSpinBox.valueChanged.connect(self.__model.set_debut)
        self.__view.finSpinBox.valueChanged.connect(self.__model.set_fin)
        self.__view.tracerPushButton.clicked.connect(self.lancer_thread)

        self.__canvas.signal.connect(self.canvas_clicked)
        self.__canvas.signal_delete.connect(self.delete_node_or_edge)
        self.__canvas.signal_create_edge.connect(self.create_edge)
        self.__canvas.signal_move.connect(self.move_node)

    def lancer_thread(self):
        progress = QProgressBar()

        progress.setRange(0,0)
        progress.show()

        self.__model.lancer_thread()
        time.sleep(1)
        progress.hide()

    def move_node(self, pos_start, pos_end):
        possible_node = self.__model.get_node_at(pos_start)
        if self.__model.graphe.has_node(possible_node[0]):
            self.__model.move_node(possible_node[0], pos_end)

    def chemin(self):
        return self.__model.chemin

    def create_edge(self,pos1, pos2):
        self.__model.create_edge(pos1, pos2)

    def delete_node_or_edge(self):
        if self.__model.selected_node:
            self.__model.delete_node()
        elif self.__model.selected_edge:
            self.__model.delete_edge()
        else:
            pass


    def canvas_clicked(self,pos):
        possible_node = self.__model.get_node_at(pos)
        possible_edge = self.__model.get_edge_at(pos)

        if self.__model.graphe.has_node(possible_node[0]):
            self.__model.selected_node = possible_node #priority one: s'il y a une node
        elif possible_edge:
            self.__model.selected_edge = possible_edge #priority 2: s'il y  a une edge
        else:
            self.__model.selected_node = possible_node #sinon, add node

    def post_init(self):
        self.__model.grapheChanged.connect(self.__canvas.on_graph_changed)
        self.__model.grapheChanged.emit(self.__model.pos)

    def graphe(self):
        return self.__model.graphe

    def selected_node(self):
        return self.__model.selected_node

    def selected_edge(self):
        return self.__model.selected_edge

    def generate_graph(self, pos):
        self.__model.generate_graph()


    def delete_graph(self, n):
        self.__model.delete_graph()
