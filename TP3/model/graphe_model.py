import random
import threading
from logging import CRITICAL

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtCore import pyqtSignal, QObject, QThread, Qt
from PyQt6.QtWidgets import QInputDialog, QProgressBar, QDialog, QVBoxLayout, QWidget, QLabel, QMessageBox
from networkx import Graph
import time

class PlusCourtChemin(QThread):
    chemin = pyqtSignal(list)
    progress_chemin = pyqtSignal(int, int)

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
                self.progress_chemin.emit(len(chemin), len(chemin_temp))
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
        self.setWindowTitle("")
        self.setGeometry(100, 600, 250, 75)

        layout = QVBoxLayout()
        label = QLabel(text)
        self.progress = QProgressBar()
        layout.addWidget(label)
        layout.addWidget(self.progress)
        self.setLayout(layout)

class GrapheModel(QObject):
    # Le graphe 0 à afficher
    _graphe: Graph = nx.Graph()
    # _pos contient le layout, soit le mapping noeud -> position pour l'Affichage
    _pos = None

    # probabilité qu'une arête existe entre deux nœuds pour la generation
    __proba = 0.5
    # Le nombre de noeuds par défaut pour la generation
    __default_graphe_order = 10
    # le poids min d'une arete pour la generation
    __poids_min = 1
    # le poids max d'une arete pour la generation
    __poids_max = 10

    __selected_node = []

    __selected_edge = []

    __debut = 0

    __fin = __default_graphe_order-1

    __chemin = []

    __parcours = []

    # signal qui envoie le graphe complet
    grapheChanged = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self._pos = nx.spring_layout(self._graphe, seed=42)


    @property
    def debut(self):
        return self.__debut

    @debut.setter
    def debut(self, value):
        self.__debut = value

    @property
    def fin(self):
        return self.__fin

    @fin.setter
    def fin(self, value):
        self.__fin = value

    def set_parcourir(self, node):

        self.__parcours.append(node)

        self.__node_colours[node] = 'red'

        self.grapheChanged.emit(self._pos)



    def set_nbr_nodes(self, value):
        if 0 < value < 101:
            self.__default_graphe_order = value

    @property
    def chemin(self):
        return self.__chemin

    def set_chemin(self, chemin):

        if chemin:
            self.remove_selecteds()

            self.__chemin = chemin

            for i in range(len(self.__chemin)):
                self.__node_colours[self.__chemin[i]] = 'orange'
                if i < len(self.__chemin)-1:
                    self._graphe.edges[(self.__chemin[i],self.__chemin[i+1])]['couleur'] = 'orange'

            self.grapheChanged.emit(self._pos)
        else:
            error = QMessageBox(None)
            error.critical(None,"Aucun chemin possible !!!", "")



    def create_edge(self, pos1, pos2):
        # TODO : fix avec nouvelle structure
        self.remove_selecteds()
        node1 = self.get_node_at(pos1)
        node2 = self.get_node_at(pos2)

        value, is_valid_weight = QInputDialog.getInt(None, "Selection du poids", "Entrez un entier:", value=1, min=1, max=100, step=1)  # Step size

        if self._graphe.has_node(node1[0]) and self._graphe.has_node(node2[0]):

            if not self._graphe.has_edge(node1[0], node2[0]):
                self._graphe.add_edge(node1[0], node2[0])

            self.__selected_edge = [node1[0], node2[0]]
            self._graphe.edges[self.__selected_edge]['couleur'] = 'red'
            if is_valid_weight:
                self._graphe.edges[self.__selected_edge]['weight'] = value
            else:
                self._graphe.edges[self.__selected_edge]['weight'] = 1

            self.grapheChanged.emit(self._pos)

    def move_node(self, node, pos):
        self.remove_selecteds()
        self._pos[node] = pos
        self.__selected_node = [node, pos]
        self.__node_colours[node] = 'red'

        self.grapheChanged.emit(self._pos)

    def graphe_order(self):
        return self._graphe.number_of_nodes()

    @property
    def default_graphe_order(self):
        return self.__default_graphe_order

    @default_graphe_order.setter
    def default_graphe_order(self, value):
        self.__default_graphe_order = value

    @property
    def graphe(self):
        return self._graphe

    @property
    def pos(self):
        return self._pos

    def edge_weight(self, edge):
        return self._graphe[edge[0]][edge[1]]['weight']

    def generate_graph(self):
        self.delete_graph()
        # Générer un graphe aléatoire non orienté avec une probabilité d'Arete donnée
        self._graphe = nx.gnp_random_graph(self.default_graphe_order, self.__proba, directed=False)

        # Ajouter un poids aléatoire à chaque arête
        for u, v in self._graphe.edges():
            self._graphe[u][v]['weight'] = random.randint(self.__poids_min, self.__poids_max)

        for u, v in self._graphe.edges():
            self._graphe[u][v]['couleur'] = 'black'

        # stocke le nouveau layout
        self._pos = nx.spring_layout(self._graphe, seed=42)

        self.__node_colours = {}
        for node in self._graphe.nodes:
            self.__node_colours[node] = 'skyblue'

        # Notif des vues
        self.grapheChanged.emit(self._pos)

    @property
    def node_colours(self):
        return self.__node_colours

    def get_number_nodes(self):
        return len(self._pos)

    @property
    def selected_edge(self):
        return self.__selected_edge

    @selected_edge.setter
    def selected_edge(self, value):
        self.remove_selecteds()

        self.__selected_edge = value
        self._graphe.edges[value]['couleur'] = 'red'

        self.grapheChanged.emit(self._pos)

    def remove_selecteds(self):
        if self.__selected_edge:
            self._graphe.edges[self.__selected_edge]['couleur'] = 'black'
            self.__selected_edge = []
        if self.__selected_node:
            self.__node_colours[self.__selected_node[0]] = 'skyblue'
            self.__selected_node = []

        if self.__chemin:
            for i in range(len(self.__chemin)):
                self.__node_colours[self.__chemin[i]] = 'skyblue'
                if i < len(self.__chemin)-1:
                    self._graphe.edges[(self.__chemin[i],self.__chemin[i+1])]['couleur'] = 'black'
            self.__chemin = []

        if self.__parcours:
            for node in self.__parcours:
                self.__node_colours[node] = 'skyblue'
            self.__parcours = []
        self.grapheChanged.emit(self._pos)


    @property
    def selected_node(self):
        return self.__selected_node

    @selected_node.setter
    def selected_node(self, value):
        self.remove_selecteds()
        self.__selected_node = value

        if not self._graphe.has_node(int(value[0])):
            self._graphe.add_node(int(value[0]), pos=value[1])
            self._pos[int(value[0])] = value[1]

        self.__node_colours[value[0]] = 'red'

        self.grapheChanged.emit(self._pos)

    def delete_node(self):
        self._graphe.remove_node(self.__selected_node[0])
        del self._pos[self.__selected_node[0]]

        self.remove_selecteds()

        self.grapheChanged.emit(self._pos)

    def delete_edge(self):
        self._graphe.remove_edge(self.__selected_edge[0], self.__selected_edge[1])
        self.__selected_edge = []
        self.remove_selecteds()
        self.grapheChanged.emit(self._pos)

    def dist_edge(self, edge, position):
        # TODO: make work

        x_click = position[0]
        y_click = position[1]
        x_pt1 = self._pos[edge[0]][0]
        y_pt1 = self._pos[edge[0]][1]
        x_pt2 = self._pos[edge[1]][0]
        y_pt2 = self._pos[edge[1]][1]

        x_pc = x_click - x_pt1
        y_pc = y_click - y_pt1

        x_edge = x_pt2 - x_pt1
        y_edge = y_pt2 - y_pt1

        x_dist = x_click - (x_pt1 + ((x_pc * x_edge + y_pc * y_edge) / (x_edge ** 2 + y_edge ** 2) * x_edge))
        y_dist = y_click - (y_pt1 + ((x_pc * x_edge + y_pc * y_edge) / (x_edge ** 2 + y_edge ** 2) * y_edge))

        return round((x_dist ** 2) + (y_dist ** 2) ** (1 / 2), 4)

    def get_node_at(self, position):

        for pos in self._pos.values():

            if ((position[0] - pos[0]) ** 2 + (position[1] - pos[1]) ** 2) ** (1 / 2) <= 0.1:


                selected_node = [key for key, val in self._pos.items() if list(self._pos[key]) == list(pos)]

                selected_node.append(pos)

                return selected_node
        return [self.get_number_nodes(), position]

    def get_edge_at(self, position):
        for edge in self._graphe.edges:
            if self.dist_edge(edge, position) <= 0.01:
                return edge
        return None

    def delete_graph(self):
        self.remove_selecteds()
        # Effacer les references au graphe
        self._graphe = nx.empty_graph()
        # stocke le nouveau layout
        self._pos = nx.spring_layout(self._graphe, seed=42)


        # Notif des vues
        self.grapheChanged.emit(self._pos)
