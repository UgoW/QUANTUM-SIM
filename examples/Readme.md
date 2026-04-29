# Exemples — QUANTUM-SIM

Ce dossier contient des scripts de démonstration pour visualiser rapidement les objets principaux de la bibliothèque.

## Prérequis

Depuis la racine du projet, installez le package puis `matplotlib` (utilisé par les exemples) :

- `pip install -e .`
- `pip install matplotlib`

## Lancer un exemple

Depuis la racine du projet :

- `python examples/demo_plane_wave.py`
- `python examples/demo_wavePacket.py`
- `python examples/demo_waveGausianPacket.py`
- `python examples/demo_schrodinger.py`
- `python examples/demo_schrodingerStep.py`
- `python examples/demo_shrodingerWell.py`
- `python examples/demo_shrodinger_animation.py`

## Contenu des scripts

- **demo_plane_wave.py**  
	Génère une onde plane et affiche ses composantes réelle et imaginaire.

- **demo_wavePacket.py**  
	Construit un paquet d’ondes à partir de plusieurs ondes planes et affiche son évolution spatiale instantanée.

- **demo_waveGausianPacket.py**  
	Crée un paquet d’ondes gaussien et affiche sa forme (partie réelle).

- **demo_schrodinger.py**  
	Propage un paquet gaussien en espace libre avec `SchrodingerSolver` et affiche $|\psi(x,t)|^2$ à plusieurs instants.

- **demo_schrodingerStep.py**  
	Propage un paquet gaussien face à un potentiel en marche (`StepPotential`) pour observer réflexion/transmission.

- **demo_shrodingerWell.py**  
	Propage un paquet gaussien dans un puits infini (`InfiniteWell`) et affiche la densité de probabilité temporelle.

- **demo_shrodinger_animation.py**  
	Anime $|\psi(x,t)|^2$ dans le temps pour le cas du potentiel en marche.