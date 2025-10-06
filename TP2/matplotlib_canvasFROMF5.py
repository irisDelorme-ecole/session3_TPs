import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import sympy as sp
from fonction_model import FonctionModel


class MPLCanvas(FigureCanvas):

#makes a mpl plot.
    __fonction_model:FonctionModel

    def __init__(self, fonction_model):
        self.__fig, self.__axe = plt.subplots()
        self.__fonction_model = fonction_model
        super().__init__(self.__fig)
        plt.draw()#makes blank plot with axes visible



        self.__fonction_model.has_updated.connect(self.plot)


    def set_colour(self):
        self.line.set_color(self.__fonction_model.get_colour())

    def set_function(self):
        self.function=self.__fonction_model.get_fonction()

    def plot(self):
        self.__axe.clear()
        f = self.__fonction_model.get_fonction()
        self.set_function()
        x = np.linspace(0,10,100)
        self.line, = self.__axe.plot(x, self.function(x))
        self.set_colour()
        self.__axe.grid(self.__fonction_model.get_has_grille())
        plt.title(self.__fonction_model.get_titre())
        plt.draw()



