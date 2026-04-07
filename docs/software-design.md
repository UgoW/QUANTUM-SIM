# Documentation Technique — QuantumSim

Ce document sert de **point d’entrée unique** vers l’ensemble de la documentation technique du projet.

L’objectif est de fournir :

* une navigation claire entre les documents
* une séparation nette des responsabilités documentaires
* un niveau de rigueur compatible avec un projet scientifique / deep‑tech

---

# 1. Vue globale de la documentation

Les documents sont organisés par **domaine fonctionnel** :

## Architecture & conception

* ➜ [Architecture du projet](./architecture.md)

Décrit :

* la structure des dossiers
* les modules Python
* le flux scientifique de calcul
* les règles d’extension du code

---

## Intégration continue & qualité

* ➜ [Validation continue (CI)](./continuous-validation.md)

Décrit :

* le workflow GitHub Actions
* les déclencheurs push / pull request
* l’exécution des tests pytest et de la couverture
* les objectifs de qualité logicielle

---

## Contribution & workflow Git

* ➜ [Guide de contribution](./contributing.md)

Décrit :

* la stratégie de branches (`develop` / `main`)
* les conventions de nommage des branches
* les règles de commits conventionnels
* le processus de Pull Request et de review
* les bonnes pratiques d’équipe
* les conventions de nommage PEP 8

---

## Installation & exécution

* ➜ [Guide d’installation](./installation.md)

Décrit :

* les prérequis Python et Poetry
* l’installation des dépendances
* l’exécution du projet
* les tests, la couverture et le build

---

# 2. Positionnement des documents

La séparation actuelle suit une logique **propre aux projets logiciels professionnels** :

| Domaine       | Document                   | Rôle                                     |
| ------------- | -------------------------- | ---------------------------------------- |
| Architecture  | `architecture.md`          | Structure interne et flux scientifique   |
| Qualité / CI  | `continuous-validation.md` | Garanties automatiques de fonctionnement |
| Collaboration | `contributing.md`          | Règles Git et organisation d’équipe      |
| Exploitation  | `installation.md`          | Mise en place locale et exécution        |

Cette structuration est **cohérente et saine**. Elle respecte les standards observés en :

* projets open‑source scientifiques
* environnements R&D
* startups deep‑tech

---

# 3. Éléments manquants recommandés (niveau industriel)

Pour atteindre une **documentation complète d’ingénierie**, il manquerait idéalement :

## 3.1 Spécification d’API Python

Un document du type :

```
docs/api.md
```

Contenant :

* signatures des fonctions publiques
* types de données
* schémas JSON de sortie
* exemples d’utilisation

👉 Critique pour l’intégration WebAssembly et frontend.

---

## 3.2 Architecture Web & WebAssembly

Un document dédié :

```
docs/web-architecture.md
```

Décrivant :

* la transcompilation Python → WebAssembly
* le chargement côté navigateur
* l’intégration Next.js / Plotly / Three.js
* les contraintes de performance numérique

---

## 3.3 Roadmap scientifique et validation physique

Un document :

```
docs/scientific-validation.md
```

Incluant :

* cas tests physiques de référence
* tolérances numériques
* reproductibilité des simulations

👉 Essentiel pour crédibilité académique.

---

# 4. Avis d’ingénierie global

## Points forts

* Architecture modulaire claire
* CI simple mais efficace
* Workflow Git propre pour petite équipe
* Packaging Poetry standard

## Risques principaux

* Absence de **contrat de données formel** (JSON / types)
* Manque de **doc API publique**
* WebAssembly non documenté techniquement

Ces points sont **normaux à ce stade** mais seront critiques si :

* ouverture publique large
* usage académique
* industrialisation

---

# 5. Ordre de priorité recommandé

Si l’objectif est de professionnaliser le projet :

1. `api.md` ← priorité maximale
2. `web-architecture.md`
3. `scientific-validation.md`

C’est le chemin classique pour passer d’un **prototype scientifique** à un **produit logiciel robuste**.

---

**Fin de la documentation centrale.**
