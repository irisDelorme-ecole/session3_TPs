import numpy as np
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import ModelIntegration
import sympy as sp


class MPLCanvas(FigureCanvas):
    model_integration: ModelIntegration.IntegrationModel

    def __init__(self, model_integration):
        self.__fig, self.__axe = plt.subplots()
        self.model_integration = model_integration
        super().__init__(self.__fig)
        plt.draw()  # makes blank plot with axes visible

    def exporter(self):
        msg = QMessageBox()
        msg.setStyleSheet("background-color : #99afd7")

        #basic filedialog pour sauvegarder le canvas.
        file_path, _ = QFileDialog.getSaveFileName(self,
                                                   "Save File", "", "PNG files(*.png);;All Files(*)")

        if file_path:
            plt.savefig(file_path, format='png')
            msg.setText(f"Plot saved as: {file_path}")
            msg.setWindowTitle("Succès!")
            msg.setIcon(QMessageBox.Icon.Information)
        else:
            msg.setText("Ça n'a pas marché.....")
            msg.setWindowTitle("Oops....")
            msg.setIcon(QMessageBox.Icon.Warning)

        msg.exec()

    def show_sum(self):
        x = sp.symbols('x')
        f = sp.lambdify(x, self.model_integration.fonction, 'numpy')
        a = self.model_integration.borne_inf
        b = self.model_integration.borne_sup
        n = self.model_integration.nb_boites

        x = np.linspace(a, b, n + 1)
        y = f(x)                     # evaluation de chaque ieme point avec pas égal à (borne sup - borne inf)/nb boites(+1 pour gèrer droite ou gauche)

        if self.model_integration.is_gauche:
            side = -1
            x_toside = x[:-1]  # Left endpoints(tous les points sauf le dernier)
            y_toside = y[:-1]
        else:
            side = 1
            x_toside = x[1:]  # right endpoints(tous les points sauf le premier)
            y_toside = y[1:]

        # rectangles avec un bar graph
        # mpl utilise des "artist" qui ont chacun une patch de type Rectangle
        # pour dessiner ses bar graphs, donc le "bar graph" ici est plus un dessin de n rectangles allant de
        # zero a f(x)
        #ça compute plus rapidement que de faire les "artists" a la main
        #puis c'est franchement plus élégant
        plt.bar(x_toside, y_toside, width=-side * (b - a) / n, alpha=1, align='edge', facecolor="None",
                edgecolor="orange", linewidth=1.5)

    def set_fonction(self, fonction):
        self.model_integration = fonction

    def plot(self):
        self.__axe.clear()
        y = np.linspace(self.model_integration.borne_inf, self.model_integration.borne_sup, 100)
        x = sp.symbols('x')
        f = sp.lambdify(x, self.model_integration.fonction.__str__(), 'numpy')

        self.__axe.plot(y, f(y))
        self.show_sum()
        plt.draw()
