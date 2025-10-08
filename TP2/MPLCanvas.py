import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import ModelIntegration
import sympy as sp

class MPLCanvas(FigureCanvas):

    __model_integration:ModelIntegration

    def __init__(self, model_integration):
        self.__fig, self.__axe = plt.subplots()
        self.__model_integration = model_integration
        super().__init__(self.__fig)
        plt.draw()  # makes blank plot with axes visible

    def plot(self):
        self.__axe.clear()
        x = sp.symbols('x')
        f = sp.lambdify(x,self.__model_integration.get_fonction(), 'numpy')
        x = np.linspace(self.__model_integration.borne_inf,self.__model_integration.borne_inf,100)
        self.line, = self.__axe.plot(x, f(x))

        plt.draw()