from quantum_sim import PlaneWave
import matplotlib.pyplot as plt
import numpy as np

#Génération d'une onde plane avec une amplitude de 1 composé d'un sinus
Wave = PlaneWave(1, 1) 

#Génération d'un domaine d'étude de -10 à 10 avec 100 points
x = np.linspace(-10, 10, 100) 
psi = Wave.evaluate(x)

#Affichage de la partie réelle et imaginaire de l'onde plane
plt.plot(x, psi.real, label='Real Part')
plt.plot(x, psi.imag, label='Imaginary Part')
plt.title('Plane Wave')
plt.xlabel('Position')
plt.ylabel('Wave Function')
plt.legend()
plt.grid()
plt.show()
