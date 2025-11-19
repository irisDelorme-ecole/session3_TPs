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
            if self.__controller.selected_node():
                graphe_sel = graphe.copy()
                graphe.remove_node(int(self.__controller.selected_node()[0]))

                pos_main = {name: pos for name, pos in self._pos.items() if
                            name != int(self.__controller.selected_node()[0])}

                nx.draw(graphe, pos_main, with_labels=True, node_color='skyblue', node_size=800)
                graphe_sel.remove_nodes_from(graphe)

                nx.draw(graphe_sel, {int(self.__controller.selected_node()[0]): self.__controller.selected_node()[1]},
                        with_labels=True, node_color='red', node_size=800)

                # fill in with edges
                nx.draw_networkx_edges(self.__controller.graphe(), self._pos)
                labels = nx.get_edge_attributes(self.__controller.graphe(), "weight")
                nx.draw_networkx_edge_labels(self.__controller.graphe(), self._pos, edge_labels=labels)
            elif self.__controller.selected_edge():
                print('in draw edge')
                graphe_sel = graphe.copy()
                print(self.__controller.selected_edge()[0], self.__controller.selected_edge()[1])
                graphe.remove_edge(self.__controller.selected_edge()[0], self.__controller.selected_edge()[1])

                nx.draw(self.__controller.graphe(), self._pos, with_labels=True, node_color='skyblue', node_size=800)

                labels = nx.get_edge_attributes(self.__controller.graphe(), "weight")
                print('huh')
                nx.draw_networkx_edges(graphe, self._pos,graphe.edges)
                graphe_sel.remove_edges_from(graphe.edges)
                print(labels)
                nx.draw_networkx_edges(graphe_sel, self._pos, graphe_sel.edges, edge_color='red')
                nx.draw_networkx_edge_labels(self.__controller.graphe(), self._pos, labels)
                nx.draw_networkx_nodes(graphe_sel, self._pos, node_color='skyblue', node_size=800)
            else:
                # Dessiner le graphe dans l'axe du canvas
                nx.draw(self.__controller.graphe(), self._pos, with_labels=True, node_color='skyblue', node_size=800)
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
                self.__dragging = True
                self.__drag_start_pos = pos
            else:
                self.__dragging = False
                self.signal.emit(pos)


        except Exception as e:
            print(e)

    def mouseReleaseEvent(self, event):
        if self.__dragging:
            pos_end = self.__convert_pos(event)
            self.signal_create_edge.emit(self.__drag_start_pos, pos_end)
            self.signal.emit(pos_end)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.signal_delete.emit("del pressed")

    def on_graph_changed(self, position):
        self._pos = position
        self.draw_graphe()
