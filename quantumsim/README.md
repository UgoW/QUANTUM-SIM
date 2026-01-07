
## 🚀 Installation

### Prérequis

- Python 
- pip (gestionnaire de packages Python)

### Installation en mode développement

1. **Cloner le dépôt** :
   ```bash
   git clone <URL_DU_REPO>
   cd quantumsim
   ```

2. **Installer le package** (obligatoire) :
   ```bash
   pip install -e .
   ```
   
   Cette commande installe le projet en mode développement (`-e`), ce qui permet :
   - D'utiliser `quantumsim` comme un vrai package Python
   - De modifier le code et voir les changements immédiatement
   - D'importer depuis n'importe quel dossier : `from quantumsim.waves import ...`
---


## 📚 Documentation

- **Installation** : Voir [`docs/installation.md`]
- **Architecture** : Voir [`docs/architecture.md`]

---

## 🛠️ Développement

### Ajouter un nouveau module

1. Créer votre fichier Python dans le bon dossier (`waves/`, `potentials/`, `solver/`, `utils/`)
2. Ajouter votre classe/fonction dans le `__init__.py` correspondant
3. Documenter votre code
4. Écrire des tests dans le dossier `tests/`


## 📜 Licence

Ce projet est sous licence [MIT](LICENSE). Voir le fichier LICENSE pour plus de détails.







