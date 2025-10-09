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

    def plot(self):
        self.__axe.clear()
        y = np.linspace(self.model_integration.borne_inf, self.model_integration.borne_sup, 100)
        x = sp.symbols('x')
        f = sp.lambdify(x,self.model_integration.fonction, 'numpy')

        self.__axe.plot(y, f(y))
        plt.draw()
