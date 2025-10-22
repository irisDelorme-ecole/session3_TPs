import numpy as np
from PyQt6.QtWidgets import QFileDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
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
        #calc etendu
        e = (self.model_integration.borne_sup-self.model_integration.borne_inf)/self.model_integration.nb_boites
        x = sp.symbols('x')
        lines = [x+1 for x in range(0,self.model_integration.nb_boites)]#[(self.model_integration.fonction.subs(x, self.model_integration.borne_inf + (i * e)) for i in range(0, self.model_integration.nb_boites + 1))]


        self.__axe.vlines(x=[x+1 for x in range(0,self.model_integration.nb_boites)],ymin=0,ymax=lines)

    def plot(self):
        self.__axe.clear()
        y = np.linspace(self.model_integration.borne_inf, self.model_integration.borne_sup, 100)
        x = sp.symbols('x')
        f = sp.lambdify(x,self.model_integration.fonction, 'numpy')

        self.__axe.plot(y, f(y))
        self.show_sum()
        plt.draw()
