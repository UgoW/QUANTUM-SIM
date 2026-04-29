from quantum_sim import GaussianWavePacket
import matplotlib.pyplot as plt
import numpy as np

#Génération d'un paquet d'ondes gaussien avec une impulsion centrale nulle, une largeur en espace de 1, composé de 200 ondes planes, et centré en x=0
GaussianPacket = GaussianWavePacket(k_center=0, sigma_k=1)

#Génération d'un domaine d'étude de -10 à 10 avec 100 points
x = np.linspace(-10, 10, 100) 

psi = GaussianPacket.evaluate(x)

#Affichage de la partie réelle et imaginaire du paquet d'ondes
plt.plot(x, psi.real, label='Real Part')
plt.title('Gaussian Wave Packet')
plt.xlabel('Position')
plt.ylabel('Wave Function')
plt.legend()
plt.grid()
plt.show()
