# Bienvenue sur le dépôt du Projet Mécanique Quantique avec Python !

Un projet de **simulation et de visualisation de phénomènes de mécanique quantique** développé en Python dans un objectif pédagogique.

Ce dépôt propose des outils permettant de **rendre la mécanique quantique plus accessible** grâce à la modélisation numérique et à la visualisation interactive d’objets quantiques.

---

## Objectifs du projet

- Illustrer les concepts fondamentaux de la mécanique quantique  
- Implémenter numériquement les équations fondamentales  
- Explorer différents cas d’étude simples et pédagogiques  
- Analyser la propagation des ondes quantiques  
- Simuler l’évolution temporelle de paquets d’ondes  

---

## Contexte

La mécanique quantique repose sur des concepts abstraits difficiles à appréhender sans support visuel.  
Les outils existants sont souvent limités, dispersés ou peu personnalisables.

Ce projet vise à proposer une **solution open source**, centralisée et évolutive, permettant aux étudiants d’explorer concrètement les phénomènes quantiques à travers la simulation et la visualisation.

---

## Fonctionnalités principales

- Modélisation d’ondes planes et de paquets d’ondes  
- Résolution numérique de l’équation de Schrödinger en 1D  
- Simulation de la propagation :
  - en espace libre  
  - dans des potentiels simples (puits, barrières…)  
- Visualisation de :
  - la fonction d’onde (réelle, imaginaire, complexe)  
  - la densité de probabilité  
- Analyse qualitative de phénomènes quantiques :
  - dispersion  
  - réflexion  
  - transmission  

---

## Technologies utilisées

- **Python**
- **NumPy / SciPy** – calcul scientifique et méthodes numériques  
- **Matplotlib** – visualisation et animations  
- **Jupyter Notebook** – démonstrations et cas d’étude  
- **pytest** – tests et validation du code  
- **Poetry** – gestion des dépendances et de l’environnement virtuel 

---

## 🚀 Installation

### Prérequis

- Python 3.9+  
- [Poetry](https://python-poetry.org/) installé

### Installer le projet avec Poetry

1. **Cloner le dépôt :**
  ```bash
  git clone https://github.com/UgoW/QUANTUM-SIM.git
  cd QUANTUM-SIM
  ```
  
2. **Installer les dépencances**
  ```bash
  poetry install --with dev 
  ```

Retirer le paramètre --with dev si en production (retire les dépendences de test).

3. **Activer l’environnement virtuel (optionnel) :**
  ```bash
  poetry shell
  ```

4. **Installer le projet en mode développement :**
  ```bash
  poetry install -e .
  ```

### Lancer le projet
   ```bash
  poetry run python main.py
   ```

### Lancer les tests avec pytest
  ```bash
  poetry run pytest
  ```

---

## 🛠️ Développement

### Ajouter un nouveau module

1. Créer votre fichier Python dans le bon dossier (`waves/`, `potentials/`, `solver/`, `utils/`)
2. Ajouter votre classe/fonction dans le `__init__.py` correspondant
3. Documenter votre code
4. Écrire des tests dans le dossier `tests/`

---

## 📚 Documentation

- **Installation** : Voir [`docs/installation.md`]
- **Architecture** : Voir [`docs/architecture.md`]

---

## 📜 Licence

Ce projet est sous licence [MIT](LICENSE). Voir le fichier LICENSE pour plus de détails.

