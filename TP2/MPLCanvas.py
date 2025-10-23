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
        a = 0
        b = 5
        N = 10
        n = 10

        x = np.linspace(a, b, N + 1)
        y = f(x)

        X = np.linspace(a, b, n * N + 1)
        Y = f(X)

        plt.plot(X, Y, 'b')
        x_left = x[:-1]  # Left endpoints
        y_left = y[:-1]
        plt.plot(x_left, y_left, 'b.', markersize=10)
        plt.bar(x_left, y_left, width=(b - a) / N, alpha=0.2, align='edge', edgecolor='b')


    def plot(self):
        self.__axe.clear()
        y = np.linspace(self.model_integration.borne_inf, self.model_integration.borne_sup, 100)
        x = sp.symbols('x')
        f = sp.lambdify(x,self.model_integration.fonction, 'numpy')

        self.__axe.plot(y, f(y))
        self.show_sum()
        plt.draw()
