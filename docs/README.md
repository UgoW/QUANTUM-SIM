# Documentation – Quantum Sim

Ce dossier contient la documentation technique du projet **quantum-sim-lib**.

La bibliothèque constitue le cœur du projet et est utilisée :
- dans des notebooks Python
- dans une interface web dédiée

---

## Sommaire

- 🚀 [Installation](installation.md)  
  Guide complet pour installer et configurer le projet.

- ⚙️ [Architecture](architecture.md)  
  Description détaillée de l’architecture logicielle, des modules internes et des flux du projet.

- 🔄 [Intégration Continue](continuous-validation.md)  
  Fonctionnement des pipelines CI/CD, tests automatiques et publication.

- 🤝 [Contributing](contributing.md)  
  Règles de contribution, workflow Git et conventions de nommage.

---

## Organisation du projet

Le dépôt principal contient :

- La bibliothèque Python `quantum-sim-lib`
- Les tests unitaires
- Les pipelines CI/CD

La bibliothèque est ensuite utilisée :
- localement via `pip install`
- dans une interface web via WebAssembly

Pour plus de détails techniques, consulter la section Architecture.
