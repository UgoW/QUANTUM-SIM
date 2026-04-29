from quantum_sim import PlaneWave, WavePacket
import matplotlib.pyplot as plt
import numpy as np

#Génération des ondes planes avec différentes amplitudes et nombres de sinus
WaveOne = PlaneWave(1, 1)
WaveTwo = PlaneWave(2, 2)
WaveTree = PlaneWave(-3, 3)

#Génération d'un domaine d'étude de -10 à 10 avec 100 points
x = np.linspace(-10, 10, 100) 

WavePacket = WavePacket([WaveOne, WaveTwo, WaveTree])
psi = WavePacket.evaluate(x)

#Affichage de la partie réelle et imaginaire du paquet d'ondes
plt.plot(x, psi.real, label='Real Part')
plt.plot(x, psi.imag, label='Imaginary Part')
plt.title('Wave Packet')
plt.xlabel('Position')
plt.ylabel('Wave Function')
plt.legend()
plt.grid()
plt.show()
