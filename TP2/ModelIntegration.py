import sympy as sp


class IntegrationModel():
    __fonction:sp.Basic = "x"
    __borne_inf:int = 0
    __borne_sup:int = 0
    __nb_boites:int = 0
    __is_gauche:bool = True


    def __init__(self):
        x = sp.symbols('x')



    def integrate(self):
        return sp.integrate(self.__fonction)


    def sum(self):
        x, i, n, a = sp.symbols('x i n a')
        #set width
        a = (self.borne_sup-self.borne_inf)/self.nb_boites
        #make new function with dx to eval.
        f = sp.symbols('f', cls=sp.Function)
        f = self.__fonction*a
        # make sum
        if self.__is_gauche:
            n = self.nb_boites - 1
            return sp.summation(f.subs(x,(a*i) + self.borne_inf),(i,0,n)).doit().evalf()
        else:
            n = self.nb_boites
            return sp.summation(f.subs(x,(a*i) + self.borne_inf), (i, 1, n))


    @property
    def is_gauche(self):
        return self.is_gauche

    @is_gauche.setter
    def is_gauche(self, value):
        self.__is_gauche = value

    @property
    def fonction(self):
        return self.__fonction

    @fonction.setter
    def fonction(self, value:str):
        #TODO: set validator?
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


