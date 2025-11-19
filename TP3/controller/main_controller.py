import time

from PyQt6.QtCore import QThread, pyqtSignal

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
        self.__canvas.signal.connect(self.canvas_clicked)
        self.__canvas.signal_delete.connect(self.delete_node)
        self.__canvas.signal_create_edge.connect(self.create_edge)

    def create_edge(self,pos1, pos2):

        self.__model.selected_edge = self.__model.create_edge(pos1, pos2)

    def delete_node(self):
        self.__model.delete_node()

    def canvas_clicked(self,pos):
        possible_node = self.__model.get_node_at(pos)
        possible_edge = self.__model.get_edge_at(pos)
        if self.__model.graphe.has_node(possible_node):
            self.__model.selected_node = possible_node #priority one: s'il y a une node
        elif possible_edge is not None:

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
