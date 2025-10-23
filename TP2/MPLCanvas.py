import numpy as np
from PyQt6.QtWidgets import QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import ModelIntegration
import sympy as sp

class MPLCanvas(FigureCanvas):

    model_integration:ModelIntegration

    def __init__(self, model_integration):
        self.__fig, self.__axe = plt.subplots()
        self.model_integration = model_integration
        super().__init__(self.__fig)
        plt.draw()  # makes blank plot with axes visible



    def exporter(self):
        file_path, _ = QFileDialog.getSaveFileName(self,
                                                   "Save File", "", "PNG files(*.png);;All Files(*)")

        if file_path:
            plt.savefig(file_path, format='png')
            print(f"Plot saved as: {file_path}")
        else:
            print("Save operation canceled.")

    def show_sum(self):
        x = sp.symbols('x')
        f = sp.lambdify(x,self.model_integration.fonction, 'numpy')
        a = self.model_integration.borne_inf
        b = self.model_integration.borne_sup
        N = self.model_integration.nb_boites


        x = np.linspace(a, b, N + 1) #evaluation
        y = f(x)

        X = np.linspace(a, b, N * N + 1) #rectangles
        Y = f(X)


        if self.model_integration.is_gauche:
            side = -1
            x_toside = x[:-1]  # Left endpoints
            y_toside = y[:-1]
        else:
            side = 1
            x_toside = x[1:]  # Left endpoints
            y_toside = y[1:]

        plt.plot(X, Y, 'b')


        plt.bar(x_toside, y_toside, width=-side*(b - a) / N, alpha=1, align='edge', facecolor="None", edgecolor="orange" )

        #code pour la visualisation d'une somme de riemman par patrick walls sur github :
        #https://patrickwalls.github.io/mathematicalpython/integration/riemann-sums/
        #bien sur avec changements pour integrer avec mon propre code.


    def plot(self):
        self.__axe.clear()
        y = np.linspace(self.model_integration.borne_inf, self.model_integration.borne_sup, 100)
        x = sp.symbols('x')
        f = sp.lambdify(x,self.model_integration.fonction, 'numpy')

        self.__axe.plot(y, f(y))
        self.show_sum()
        plt.draw()
