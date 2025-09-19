import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from pprint import pprint
import json


class Electron():
    # attributs
    id_generator = 0
    __id: int
    __orbite: int

    def __init__(self, orbite):
        Electron.id_generator += 1

        self.__id = Electron.id_generator
        self.__orbite = orbite


class Atome():
    __nom: str
    __numero_atomique: int
    __electrons: list[Electron]

    def __init__(self, numero_atomique, nom):
        self.__nom = nom
        self.__numero_atomique = numero_atomique
        self.__electrons = []
        compteur_restants = self.numero_atomique

        derniere_periode_pleine = 0

        # check "periode"(selon regle simplifiee.) and add electrons.

        if self.numero_atomique > 1:  # if niveau un est plein, add all.
            self.electrons.append(Electron(1))
            compteur_restants += -2
            derniere_periode_pleine += 1

        if self.numero_atomique > 2:  # if niveau deux est plein, add all.
            for i in range(8):
                self.electrons.append(Electron(2))
                i += 1
            compteur_restants += -8
            derniere_periode_pleine += 1

        if self.numero_atomique > 10:  # if niveau trois est plein, add all.
            for i in range(18):
                self.electrons.append(Electron(3))
                i += 1
            compteur_restants += -18
            derniere_periode_pleine += 1

        if self.numero_atomique > 28:  # if niveau quatre est plein, add all.
            for i in range(32):
                self.electrons.append(Electron(4))
                i += 1
            compteur_restants += -32
            derniere_periode_pleine += 1

        if self.numero_atomique > 110:  # if niveau cinq est plein, add all.
            for i in range(50):
                self.electrons.append(Electron(5))
                i += 1
            compteur_restants += -50
            derniere_periode_pleine += 1

        if self.numero_atomique > 182:  # if niveau six est plein, add all.
            for i in range(72):
                self.electrons.append(Electron(6))
                i += 1
            compteur_restants += -72
            derniere_periode_pleine += 1

        for i in range(compteur_restants):  # ajout des electrons de valence
            self.electrons.append(Electron(derniere_periode_pleine + 1))
            i += 1

    @property
    def electrons(self):
        return self.__electrons

    @property
    def nom(self):
        return self.__nom

    @property
    def numero_atomique(self) -> int:
        return self.__numero_atomique

    @numero_atomique.setter
    def numero_atomique(self, value):
        pass

    def orbites(self):
        orbites = {}
        num_atom_compteur = self.numero_atomique
        unfinished = 0
        for n in range(1, 8):
            if num_atom_compteur > 2 * n ** 2:
                orbites[n] = 2 * n ** 2
            else:
                unfinished = n
                break
            num_atom_compteur -= 2 * n ** 2
        if unfinished > 0:
            orbites[unfinished] = num_atom_compteur

        return orbites

    def afficher_orbites(self):
        pprint(self.orbites())

    def dessiner_orbites(self):
        fig, axe = plt.subplots()
        plt.setp(axe, xticks=[], yticks=[])
        axe.set_xlim(-7, 7)
        axe.set_ylim(-7, 7)
        axe.axis('equal')
        axe.set_title(self.nom)

        # nucleus
        circle = Circle((0, 0), 0.5, color='black', fill=True, zorder=1)
        # Add the circle to the plot
        axe.add_patch(circle)

        orbs = self.orbites()

        list_colours = ['red', 'green', 'blue', 'red', 'green', 'blue', 'red']

        for niveau in orbs.keys():
            # make guide circle
            circle = Circle((0, 0), niveau, color='black', fill=False, zorder=1)
            axe.add_patch(circle)

            # find angles
            theta = (2 * np.pi) / (orbs[niveau])

            # add electrons
            for e in range(orbs[niveau]):
                electron = Circle((niveau * np.cos(theta * e), niveau * np.sin(theta * e)), 0.1,
                                  color=list_colours[niveau - 1], fill=True, zorder=2)
                axe.add_patch(electron)
                e += 1
        plt.show()

    @classmethod
    def from_dict(cls, data):
        atome = cls(data['numero_atomique'], data['nom'])
        return atome

    def to_dict(self):
        return {
            'numero_atomique': self.numero_atomique,
            'nom': self.nom,
        }

    def __repr__(self):
        return f'{self.__nom} ({self.numero_atomique}) '


class TableauPeriodique():
    # attribut
    __elements: list[Atome]

    def __init__(self, elements: list[Atome]):
        self.__elements = elements

        with open('tableau_periodique.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for a in data['elements']:
                self.__elements.append(Atome.from_dict(a))

    def get_atome(self, numero_atomique: int) -> Atome:
        return self.__elements[numero_atomique - 1]


if __name__ == '__main__':
    rep = ""
    while rep != 'N' and rep != 'n':
        t = TableauPeriodique([])
        rep = t.get_atome(int(input('Numero atomique: ')))
        rep.afficher_orbites()
        rep.dessiner_orbites()
        rep = input("Voulez-vous afficher la configuration electrique d'un autre atome? O/N")
