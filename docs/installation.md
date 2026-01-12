# 🚀 Installation du projet

Ce document explique comment installer et configurer le projet **Mécanique Quantique avec Python**.

## Prérequis

- Python 3.9 ou supérieur  
- [Poetry](https://python-poetry.org/) installé

## Installer le projet avec Poetry

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

## Lancer le projet
   ```bash
  poetry run python main.py
   ```

## Lancer les tests avec pytest
  ```bash
  poetry run pytest
  ```

## Build le projet
  ```bash
  poetry build
  ```
La commande aura pour effet de crée un fichier `dist` avec les différents build. (**Attention à ne pas inclure le dossier dans le git**)

Pour tester localement : 
  ```bash
  pip install dist/quantum_sim-[...]
  ```