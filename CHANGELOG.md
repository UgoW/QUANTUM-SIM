# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-01-16

### Added

#### Architecture & Infrastructure
- Initialisation du projet avec Poetry et structure de base
- Architecture complète du projet avec organisation modulaire (`src/quantum_sim/`)
- Mise en place d'une CI/CD minimale (GitHub Actions)
- Configuration pytest avec marqueurs personnalisés (unit, wave)
- Support d'installation PyPI avec script d'entrée `quantum-sim`

#### Modélisation des Ondes Quantiques
- **Classe `WaveFunction`** : Représentation abstraite des fonctions d'onde quantiques
- **Classe `WavePacket`** : Modélisation des paquets d'ondes avec propriétés physiques (position, impulsion, dispersion)
- **Classe `PlaneWave`** : Implémentation des ondes planes quantiques avec paramètres initiaux
- **Classe `WaveResult`** : Structure pour stocker et manipuler les résultats de simulations

#### Modélisation des Potentiels
- **Classe abstraite `Potential`** : Interface de base pour tous les potentiels quantiques
- **Classe `FreePotential`** : Potentiel d'espace libre (cas sans obstacle)
- **Classe `InfiniteWell`** : Puits de potentiel infini (1D) - modèle pédagogique
- **Classe `StepPotential`** : Potentiel en marche (barrière/puits fini) - cas de transmission/réflexion
- Tests unitaires et architecture d'intégration pour les potentiels

#### Gestion des Erreurs & Validation
- **Module `exceptions.py`** : Classes d'exceptions personnalisées pour la gestion des erreurs spécifiques au domaine
  - `QuantumSimError` : Exception de base
  - `InvalidParameterError` : Paramètres invalides
  - `PhysicsError` : Erreurs physiques
- **Module `wave_validators.py`** : Validateurs de type et d'intégrité pour les fonctions d'onde
  - Validation des paramètres physiques
  - Vérification de la normalisation
  - Contrôle des types et dimensions

#### Tests
- Architecture complète de tests (tests unitaires et intégration)
- Tests pour exceptions et validateurs
- Tests pour `WaveResult` et la manipulation des résultats
- Tests pour les ondes et les potentiels
- Suivi de couverture de code avec `coverage`

#### Documentation
- **`README.md`** : Guide complet du projet avec objectifs, fonctionnalités et contexte
- **`docs/installation.md`** : Guide d'installation détaillé (Poetry, dépendances, virtualenv)
- **`docs/architecture.md`** : Documentation de l'architecture du projet
- **`docs/contributing.md`** : Guide de contribution
- **`docs/CI.md`** : Documentation du système CI/CD
- Convention de travail Git et structure de branches

### Dependencies
- **Python** ≥ 3.11
- **NumPy** (≥ 2.4.1, < 3.0.0) : Calcul scientifique et algèbre linéaire
- **Coverage** (≥ 7.13.1, < 8.0.0) : Mesure de couverture de tests
- **pytest** (^9.0.2) : Framework de testing
- **Poetry** (≥ 2.0.0) : Gestion des dépendances et du packaging

### Fixed
- Corrections de syntaxe et d'erreurs mineures dans le code (#18)
- Corrections d'instructions incorrectes dans la documentation
- Résolution de problèmes de duplication de code

### Known Issues
- Résolveur numérique pour l'équation de Schrödinger à implémente
- Visualisation interactive non encore intégrée
- Support limité aux systèmes 1D

---

## Notes de Développement

### Branches principales
- **main** : Version stable
- **develop** : Branche de développement intégrant les features

### Prochaines étapes envisagées
- Implémentation du résolveur numérique pour l'équation de Schrödinger
- Extension à 2D et 3D
- Intégration de Matplotlib pour la visualisation
- Cas d'étude pédagogiques complets
- Publication sur PyPI
