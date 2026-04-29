# Notebooks de cours — QUANTUM-SIM

Ce dossier regroupe des notebooks pédagogiques pour découvrir les briques principales de la bibliothèque, de la fonction d’onde simple jusqu’à la résolution numérique de l’équation de Schrödinger en présence de potentiels.

## Objectif

- Présenter progressivement les concepts physiques et numériques.
- Montrer des exemples directement exécutables.

## Parcours recommandé

1. **01_WaveFunction.ipynb**  
	Introduction à la classe de base pour représenter une fonction d’onde.

2. **02_PlaneWave.ipynb**  
	Construction et visualisation d’une onde plane.

3. **03_WavePacket.ipynb**  
	Superposition d’ondes planes pour former un paquet d’ondes.

4. **04_GaussianWavePacket.ipynb**  
	Paquet d’ondes gaussien et paramètres physiques associés.

5. **05_SchrodingerSolver.ipynb**  
	Résolution de l’équation de Schrödinger dépendante du temps (cas libre), visualisation de $|\psi(x,t)|^2$ et suivi de la dynamique.

6. **06_SchrodingerSolver_InfiniteWell.ipynb**  
	Propagation dans un puits carré infini (`InfiniteWell`), avec comparaison potentiel/densité et animation temporelle.

## Pré-requis

- Python $\geq 3.11$
- Dépendances du projet installées
- Environnement notebook (Jupyter / VS Code notebooks)