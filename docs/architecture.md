# ⚙️ Architecture du projet

Ce document décrit l’architecture du projet **Mécanique Quantique avec Python**.

## Structure des dossiers

```
quantumsim/
├─ waves/
├─ potentials/
├─ solver/
├─ utils/
├─ tests/
├─ docs/
├─ pyproject.toml
├─ poetry.lock
└─ main.py
```

## Modules principaux

- **waves/** : Fonctions et classes liées aux ondes quantiques
- **potentials/** : Définition des potentiels
- **solver/** : Résolution numérique de l’équation de Schrödinger
- **utils/** : Fonctions utilitaires
- **tests/** : Tests unitaires avec pytest

## Flux général

1. Définir un paquet d’ondes et un potentiel
2. Le solver calcule l’évolution temporelle
3. Visualisations :
   - Fonction d’onde (réelle, imaginaire, complexe)
   - Densité de probabilité
4. Tests pytest pour valider les modules

## Ajouter un nouveau module

1. Créer votre fichier Python dans le bon dossier (`waves/`, `potentials/`, `solver/`, `utils/`)
2. Ajouter votre classe/fonction dans le `__init__.py` correspondant
3. Documenter votre code
4. Écrire des tests dans le dossier `tests/`

## Notes

- Poetry gère les dépendances et l’environnement virtuel
- `poetry.lock` doit être versionné pour garantir la cohérence des versions