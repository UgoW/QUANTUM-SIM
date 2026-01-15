# Intégration Continue (CI)

Ce projet utilise **GitHub Actions** pour assurer une intégration continue simple.  
La CI vérifie automatiquement la qualité et le fonctionnement du projet à chaque push ou pull request sur les branches principales.

---

## Workflow actuel

- **Nom** : CI
- **Déclencheurs** :
  - `push` sur `main` et `develop`
  - `pull_request` vers `main` et `develop`
- **Python** : 3.14 (via `setup-python`)
- **Gestionnaire de dépendances** : Poetry

### Étapes exécutées

1. **Checkout** : Récupère le code du dépôt.
2. **Setup Python** : Configure l’interpréteur Python 3.14.
3. **Installer Poetry** : Installe Poetry pour gérer l’environnement et les dépendances.
4. **Installer les dépendances** : `poetry install --no-interaction`.
5. **Exécuter les tests** : `poetry run coverage run -m pytest`.
   - Si un test échoue, la CI échoue automatiquement et le merge est bloqué.

---

## Objectifs de la CI

- Garantir que le code reste fonctionnel à chaque modification.
- Automatiser les tests unitaires pour éviter les régressions.
- Fournir un feedback rapide aux contributeurs sur la qualité du code.
- Préparer le projet à être facilement installé et utilisé sur n’importe quelle machine.

---

## Ajouter des tests

### 1. Créer un fichier de test
- Tous les fichiers de tests doivent être placés dans le dossier `tests/`.
- Nommer les fichiers suivant la convention **`test_*.py`** ou `*_test.py`.
  
Exemple :
  tests/test_example.py

### 2. Créer des fonctions de test
- Chaque fonction de test doit commencer par `test_`.
- Utiliser **pytest** pour écrire les assertions.

Exemple :
```python
def test_addition():
    assert 1 + 1 == 2

def test_subtraction():
    assert 5 - 3 == 2
