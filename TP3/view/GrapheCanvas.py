import networkx as nx
import numpy as np
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.uic.properties import QtCore

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from networkx import NetworkXError
from typing import TYPE_CHECKING

from sympy.categories import Object

if TYPE_CHECKING:
    from controller.main_controller import MainController  # uniquement pour


class GraphCanvas(FigureCanvasQTAgg):
    _pos = None

    signal = pyqtSignal(np.ndarray)
    signal_delete = pyqtSignal(str)
    signal_create_edge = pyqtSignal(np.ndarray, np.ndarray)
    signal_move = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self):
        # Crée une figure matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        super().__init__(self.fig)
        # self.draw_graphe()
        if TYPE_CHECKING:
            self.__controller: MainController | None = None
        # Permet de faire fonctionner l'ecoute des touches dans un canvas
        self.setFocus()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.__dragging = False

    def set_controller(self, controller):
        self.__controller = controller

    def __convert_pos(self, event):
        """ Cette methode permet de transformer les coordonnées d'un mouseEvenyt
         (coordonnées QT) en coordonnées figure matplotlib """
        # coordonnées de l’événement en pixels figure
        x_fig, y_fig = self.mouseEventCoords(event)

        # transformation : des pixels figure → data coords
        return self.ax.transData.inverted().transform((x_fig, y_fig))

    def draw_graphe(self):
        # Effacer le contenu précédent
        self.ax.clear()
        self.__draw_graphe()
        self.draw()

    def __draw_graphe(self):
        if self.__controller.graphe() is None:
            return

        graphe = self.__controller.graphe().copy()

        try:
            node_colours = [self.__controller.node_colours()[node] for node in self.__controller.graphe()]

            edge_colours = [nx.get_edge_attributes(self.__controller.graphe(), "couleur")[edge] for edge in self.__controller.graphe().edges]

            nx.draw(self.__controller.graphe(), self._pos, with_labels=True, node_color=node_colours, node_size=800)

            nx.draw_networkx_edges(self.__controller.graphe(), self._pos, self.__controller.graphe().edges, edge_color=edge_colours)

            labels = nx.get_edge_attributes(self.__controller.graphe(), "weight")
            nx.draw_networkx_edge_labels(self.__controller.graphe(), self._pos, edge_labels=labels)

        except NetworkXError as nxe:
            print("__draw_graphe, Erreur inatendue:", nxe)
        except Exception as e:
            print("__draw_graphe, Erreur inatendue:", e)

    def mousePressEvent(self, event):
        try:
            pos = self.__convert_pos(event)

            if event.button() == Qt.MouseButton.RightButton:
                # TODO: make so i cant just drag from nowhere
                self.__dragging_right = True
                self.__drag_start_pos = pos
            else:
                self.__dragging_right = False
                self.__drag_start_pos = pos



        except Exception as e:
            print(e)

    def mouseReleaseEvent(self, event):
        pos_end = self.__convert_pos(event)
        if self.__dragging_right:
            pos_end = self.__convert_pos(event)
            self.signal_create_edge.emit(self.__drag_start_pos, pos_end)
        elif ((self.__drag_start_pos[0]-pos_end[0])**2 + (self.__drag_start_pos[1]-pos_end[1])**2)**(1/2) > 0.06:
            self.signal_move.emit(self.__drag_start_pos, pos_end)
        else:
            self.signal.emit(self.__drag_start_pos)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.signal_delete.emit("del pressed")


    def on_graph_changed(self, position):
        self._pos = position
        self.draw_graphe()
