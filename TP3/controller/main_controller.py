import time
from model.graphe_model import GrapheModel
from view.GrapheCanvas import GraphCanvas
from view.MainWindow import MainWindow
from model.threads import Parcourir, PopupWindow, PlusCourtChemin


class MainController:
    __view: MainWindow
    __model: GrapheModel
    __canvas: GraphCanvas

    def __init__(self, view, model, canvas):
        self.__view = view
        self.__model = model
        self.__canvas = canvas

        self.progressBar_chemin = PopupWindow("Recherche du chemin ...")
        self.progressBar_parcour = PopupWindow("Avancement du parcour ...")

        #signaux du view
        self.__view.createButton.clicked.connect(self.generate_graph)
        self.__view.deleteButton.clicked.connect(self.delete_graph)
        self.__view.debutSpinBox.valueChanged.connect(self.set_debut)
        self.__view.finSpinBox.valueChanged.connect(self.set_fin)
        self.__view.tracerPushButton.clicked.connect(self.lancer_thread_chemin)
        self.__view.nbrNodes.valueChanged.connect(self.__model.set_nbr_nodes)
        self.__view.signal_parcourir.connect(self.lancer_thread_parcours)


        #signaux du canvas
        self.__canvas.signal.connect(self.canvas_clicked)
        self.__canvas.signal_delete.connect(self.delete_node_or_edge)
        self.__canvas.signal_create_edge.connect(self.create_edge)
        self.__canvas.signal_move.connect(self.move_node)
        self.__canvas.signal_parcourir.connect(self.lancer_thread_parcours)
        self.__canvas.edge_weight_signal.connect(self.change_edge_weight)


    def set_debut(self, value):
        self.__model.debut = value

    def set_fin(self, value):
        self.__model.fin = value

    def change_edge_weight(self, pos):
        edge = self.__model.get_edge_at(pos)
        if edge:
            self.__model.change_edge_weight(edge)
            self.__model.selected_edge = edge

    def lancer_thread_parcours(self):
        self.thread_parcours = Parcourir(self.__model.graphe)

        self.thread_parcours.start()

        self.thread_parcours.progress_parcours.connect(self.set_parcourir)
        self.thread_parcours.signal_fini.connect(self.finir_parcours)

    def finir_parcours(self):
        self.__model.remove_selecteds()
        self.progressBar_parcour.hide()

    def set_parcourir(self, node, progress):
        self.progressBar_parcour.show()
        self.progressBar_parcour.progress.setValue(int((progress / self.__model.graphe.number_of_nodes()) * 100))

        self.__model.set_parcourir(node)

    def lancer_thread_chemin(self):
        self.thread_chemin = PlusCourtChemin(self.__model.debut, self.__model.fin, self.__model.graphe)

        self.thread_chemin.start()

        self.progressBar_chemin.show()
        self.progressBar_chemin.progress.setRange(0,0)

        self.thread_chemin.chemin.connect(self.__model.set_chemin)
        self.thread_chemin.fini_chemin.connect(self.finir_chemin)


    def finir_chemin(self):
        time.sleep(1)
        self.progressBar_chemin.hide()
        self.__model.remove_selecteds()

    def move_node(self, pos_start, pos_end):
        possible_node = self.__model.get_node_at(pos_start)
        if self.__model.graphe.has_node(possible_node[0]):
            self.__model.move_node(possible_node[0], pos_end)

    def chemin(self):
        return self.__model.chemin

    def node_colours(self):
        return self.__model.node_colours

    def create_edge(self, pos1, pos2):
        self.__model.create_edge(pos1, pos2)

    def delete_node_or_edge(self):
        if self.__model.selected_node:
            self.__model.delete_node()
        elif self.__model.selected_edge:
            self.__model.delete_edge()
        else:
            pass

    def canvas_clicked(self, pos):
        possible_node = self.__model.get_node_at(pos)
        possible_edge = self.__model.get_edge_at(pos)


        if self.__model.graphe.has_node(possible_node[0]):
            self.__model.selected_node = possible_node  # priority one: s'il y a une node
        elif possible_edge:
            self.__model.selected_edge = possible_edge  # priority 2: s'il y  a une edge
        else:
            self.__model.selected_node = possible_node  # sinon, add node

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
        self.__view.nbrNodes.setEnabled(False)

    def delete_graph(self, n):
        self.__model.delete_graph()
        self.__view.nbrNodes.setEnabled(True)
