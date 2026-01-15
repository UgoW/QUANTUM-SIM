# ⚙️ Architecture du projet

Ce document décrit l’architecture du projet **QuantumSim**.

## Structure des dossiers

```
├─.github/worflows
├─docs
├─src/quantumsim/
├──── errors/
├──── potentials/
├──── solver/
├──── utils/
├──── validators/
├──── waves/
├─ tests/
├─ .gitignore
├─ CHANGELOG.md
├─ LICENSE
├─ poetry.lock
├─ pyproject.toml
└─ README.md
```

## Modules principaux

- **errors/** : Gestion des erreurs personnalisées
- **potentials/** : Définition des potentiels
- **solver/** : Résolution numérique de l’équation de Schrödinger
- **utils/** : Fonctions utilitaires
- **validators/** : Validation des entrées utilisateur
- **waves/** : Fonctions et classes liées aux ondes quantiques
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