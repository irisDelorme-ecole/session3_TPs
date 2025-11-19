import random
import threading

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtCore import pyqtSignal, QObject
from networkx import Graph


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

    # signal qui envoie le graphe complet
    grapheChanged = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._pos = nx.spring_layout(self._graphe, seed=42)

    def create_edge(self, pos1, pos2):
        #TODO : fix avec nouvelle structure
        node1 =self.get_node_at(pos1)
        node2 =self.get_node_at(pos2)
        if self._graphe.has_node(node1[0]) and self._graphe.has_node(node2[0]):
            if self._graphe.has_edge(node1[0], node2[0]):
                self._graphe[node1[0]][node2[0]]['weight'] += 1
            else:
                self._graphe.add_edge(node1[0], node2[0], weight=1)

            self.grapheChanged.emit(self._pos)
        return [node1[0], node2[0]]

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

        # stocke le nouveau layout
        self._pos = nx.spring_layout(self._graphe, seed=42)


        # Notif des vues
        self.grapheChanged.emit(self._pos)

    def get_number_nodes(self):
        return len(self._pos)

    @property
    def selected_edge(self):
        return self.__selected_edge

    @selected_edge.setter
    def selected_edge(self, value):
        self.__selected_edge = [value[0], value[1]]
        self.__selected_node = []
        self.grapheChanged.emit(self._pos)

    @property
    def selected_node(self):
        return self.__selected_node

    @selected_node.setter
    def selected_node(self, value):
        self.__selected_node = value

        if not self._graphe.has_node(int(value[0])):
            self._graphe.add_node(int(value[0]), pos=value[1])
            self._pos[int(value[0])] = value[1]

        self.__selected_edge = []
        self.grapheChanged.emit(self._pos)

    def delete_node(self):
        if self.__selected_node:
            self._graphe.remove_node(self.__selected_node[0])
            del self._pos[self.__selected_node[0]]
            self.__selected_node = []
            self.grapheChanged.emit(self._pos)

    def dist_edge(self, edge, position):
        #TODO: make work

        x_click = position[0]
        y_click = position[1]
        x_pt1 = self._pos[edge[0]][0]
        y_pt1 = self._pos[edge[0]][1]
        x_pt2 = self._pos[edge[1]][0]
        y_pt2 = self._pos[edge[1]][1]


        x_pc = x_click - x_pt1
        y_pc = y_click - y_pt1


        x_edge   =  x_pt2 - x_pt1
        y_edge  =  y_pt2 - y_pt1

        x_dist = x_click - (x_pt1 + ((x_pc*x_edge + y_pc*y_edge)/(x_edge**2 + y_edge**2) * x_edge))
        y_dist =  y_click - (y_pt1 + ((x_pc*x_edge + y_pc*y_edge)/(x_edge**2 + y_edge**2) * y_edge))
        if (x_dist**2) + (y_dist**2)**(1/2) < 2:
            print(round((x_dist**2) + (y_dist**2)**(1/2), 4), position, edge)
        return round((x_dist**2) + (y_dist**2)**(1/2), 4)




    def get_node_at(self, position):

        for pos in self._pos.values():

            if ((position[0] - pos[0]) ** 2 + (position[1] - pos[1]) ** 2) ** (1 / 2) <= 0.06:
                print(pos)

                selected_node = [key for key, val in self._pos.items() if list(self._pos[key]) == list(pos)]


                selected_node.append(pos)

                return selected_node
        return [self.get_number_nodes() , position]


    def get_edge_at(self, position):
        for edge in self._graphe.edges:
            if self.dist_edge(edge, position) <= 0.004:
                return edge
        return None


    def delete_graph(self):
        # Effacer les references au graphe
        self._graphe = nx.empty_graph()
        # stocke le nouveau layout
        self._pos = nx.spring_layout(self._graphe, seed=42)

        self.__selected_node = []

        # Notif des vues
        self.grapheChanged.emit(self._pos)
