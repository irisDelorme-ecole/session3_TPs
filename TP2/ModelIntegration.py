import sympy as sp
import numpy as np


class IntegrationModel():
    __fonction: sp.Basic
    __borne_inf: int = 0
    __borne_sup: int = 5
    __nb_boites: int = 1
    __is_gauche: bool = True

    def __init__(self, fonction):
        super().__init__()
        x = sp.symbols('x')

        self.fonction = fonction

    def integrate(self):
        x = sp.symbols('x')
        return sp.integrate(self.__fonction, (x, self.borne_inf, self.borne_sup))

    def sum(self):
        x, i, n = sp.symbols('x i n')
        n = self.nb_boites

        # set width
        delta_x = (self.borne_sup - self.borne_inf) / self.nb_boites

        # points gauche ou droite (gauche: de borne_inf a borne_sup-largeur des rectangles,
        # droite: de borne_inf + largeur a borne sup
        # nb boites pour le nombre de points a evaluer, puisque np selectionne des points a distance egale les uns des autres(rects. toujours meme largeur)
        x_gauche = np.linspace(self.borne_inf, self.borne_sup - delta_x, self.nb_boites)
        x_droite = np.linspace(self.borne_inf + delta_x, self.borne_sup, self.nb_boites)

        f = sp.lambdify(x, self.__fonction, modules="numpy")

        # make sum
        if self.__is_gauche:
            return np.sum(f(x_gauche) * delta_x)
        else:
            return np.sum(f(x_droite) * delta_x)

    @property
    def is_gauche(self):
        return self.__is_gauche

    @is_gauche.setter
    def is_gauche(self, value):
        self.__is_gauche = value

    @property
    def fonction(self):
        return self.__fonction

    @fonction.setter
    def fonction(self, value: str):
        # TODO: set validator?
        self.__fonction = sp.sympify(value)

    @property
    def borne_inf(self):
        return self.__borne_inf

    @borne_inf.setter
    def borne_inf(self, value):
        # TODO: set validator?
        self.__borne_inf = value

    @property
    def borne_sup(self):
        return self.__borne_sup

    @borne_sup.setter
    def borne_sup(self, value):
        # TODO: set validator?
        self.__borne_sup = value

    @property
    def nb_boites(self):
        return self.__nb_boites

    @nb_boites.setter
    def nb_boites(self, value):
        # TODO: set validator?
        self.__nb_boites = value

    def __str__(self):

        return str(self.fonction)

    def latex(self):
        return str(sp.latex(self.fonction))

    def __eq__(self, other):
        if other is None:
            return False
        elif other.__class__.__name__ != self.__class__.__name__:
            return False
        else:
            return self.__str__() == other.__str__()

# test = IntegrationModel()
# test.fonction = "x**3"
# print(test.sum())
