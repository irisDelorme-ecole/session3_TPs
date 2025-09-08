import sympy as sp
from sympy import Eq, init_printing
import matplotlib.pyplot as plt
import numpy as np


#1
init_printing()


#f(x) = 3x**3-5x**2+2x-7
x = sp.Symbol('x')
f = sp.Symbol('f(x)')
equ = 3*(x**3)-5*(x**2)+2*(x)-7
#a)
print('f(x)')
sp.pprint(Eq(f, equ))

#b)
print('derivee de f(x)')
deriv = sp.diff(equ,x)
sp.pprint(deriv)

#c)
print("points critiques de f'(x)")
solved_deriv = sp.solve(deriv,x)
sp.pprint(solved_deriv)

#d)
print('f au points critiques')
sp.pprint(equ.subs(x,solved_deriv[0]))

sp.pprint(equ.subs(x,solved_deriv[1]))

#e)
print('integrale indefinie de f(x)')
sp.pprint(sp.integrate(deriv, x))

#f)
print('integrale de f(x) entre 0 et 2')
sp.pprint(sp.integrate(equ, (x,0,2)))

#g) a i)
y = sp.Symbol('y')
derivvv = 9*y**2 - 10*y +2
new_equ = 3*(y**3)-5*(y**2)+2*(y)-7
f_num = sp.lambdify(x, equ)
x = np.linspace(-2,3,50)

fprime_num = sp.lambdify(y, derivvv)

tanplot = np.linspace(-2,3,50)
tanplot_num = derivvv.subs(y,-1)*(x+1) + new_equ.subs(y, -1)

plt.axhline(0, color='black', linewidth=1, linestyle='--')
plt.axvline(0, color='black', linewidth=1, linestyle='--')
plt.plot(x,f_num(x), label="f(x)")
plt.plot(x,fprime_num(x), label="f'(x)")


#reste 2 et 3

plt.plot( solved_deriv[1],0, marker=".", color="black",  markersize=4, label="derivative of f(x) == 0")
plt.plot(solved_deriv[0],0, marker=".", color="black",  markersize=4, label="derivative of f(x) == 0")
plt.plot(x, tanplot_num, label="tangente de f(x) a x = -1")
plt.legend()
plt.show()