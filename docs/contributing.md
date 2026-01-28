# Contributing Guide

Ce document décrit les conventions Git, les règles de contribution et le workflow de développement du projet. Il s’adresse à une **petite équipe** et vise la simplicité, la lisibilité et la qualité du code.

---

## 1. Workflow général

* La branche **`develop`** est la branche d’intégration principale.
* La branche **`main`** contient uniquement du code stable et prêt pour la production.
* Tout développement se fait **à partir de `develop`**.
* Aucun commit direct n’est autorisé sur `main` ou `develop`.
* Toute intégration passe par une **Pull Request (PR)**.

---

## 2. Gestion des issues

* Toute tâche commence par la création d’une **issue**.
* Le titre de l’issue doit contenir le **ticker ClickUp**.
* La description de l’issue doit inclure :

  * Le **nom du ticker ClickUp**
  * Le **lien ClickUp** associé

**Exemple :**
`US 1.2 - Authentification utilisateur`

---

## 3. Convention de nommage des branches

Les branches doivent être créées **depuis `develop`**.

### Format

```
<type>/<ticker>
```

### Types autorisés

* `feature/` : nouvelle fonctionnalité
* `fix/` : correction de bug
* `chore/` : maintenance, outillage, refactor léger

### Exemple

```
feature/US-1.2-authentification-utilisateur
```

---

## 4. Convention des messages de commit

Nous utilisons la convention **Google Conventional Commits (classique)**.

### Format

```
<type>(<scope>): <message>
```

### Types autorisés

* `feat` : nouvelle fonctionnalité
* `fix` : correction de bug
* `docs` : documentation
* `style` : formatage, sans impact fonctionnel
* `refactor` : refactorisation
* `test` : ajout ou modification de tests
* `chore` : tâches diverses

### Exemples

```
feat: ajout de la connexion par email
fix: correction du statut HTTP 401
docs: ajout des règles de PR
```

---

## 5. Labels Git

* **`DEVELOPING`** : la branche est en cours de développement
* **`WAITING FOR REVIEW`** : la PR est prête à être relue et mergée

Le label doit être mis à jour manuellement au bon moment.

---

## 6. Règles de Pull Request (PR)

### Création de la PR

* La PR doit cibler **`develop`**
* Le titre de la PR doit contenir le **ticker ClickUp**
* La description doit inclure :

  * Le lien ClickUp
  * Un résumé clair des changements

### Relecture

* **Au moins une personne** doit relire et approuver la PR
* Les commentaires doivent être adressés avant le merge

### Merge

* Le merge se fait uniquement **après validation**
* Utiliser **Squash and Merge**
* Le message de squash doit respecter la convention de commit

---

## 7. Règles de merge

* Pas de merge sans PR
* Pas de merge sans review
* Pas de merge sans squash
* La branche doit être à jour avec `develop`

---

## 8. Bonnes pratiques

* Des PR petites et lisibles
* Des commits atomiques
* Des messages clairs et explicites
* Une communication active pendant les reviews

## 9. Conventions de nommage (variables, classes...)
### Guide des Conventions de Nommage (PEP 8)

| Élément | Public | Interne / Privé |
| :--- | :--- | :--- |
| **Packages** | `lower_with_under` | |
| **Modules** | `lower_with_under` | `_lower_with_under` |
| **Classes** | `CapWords` | `_CapWords` |
| **Exceptions** | `CapWords` | |
| **Fonctions** | `lower_with_under()` | `_lower_with_under()` |
| **Constantes** | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER` |
| **Variables (Global/Classe)** | `lower_with_under` | `_lower_with_under` |
| **Variables d'instance** | `lower_with_under` | `_lower_with_under` |
| **Méthodes** | `lower_with_under()` | `_lower_with_under()` |
| **Paramètres** | `lower_with_under` | |
| **Variables locales** | `lower_with_under` | |

## 10. Commandes utiles
### Générer une documentation au format HTML de l'API
```bash
sh ./scripts/generate_docs.sh
```