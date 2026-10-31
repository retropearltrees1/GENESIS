# Test_IA

Ce projet fournit des utilitaires d'interaction et de gestion du dépôt, permettant de manipuler des fichiers (création, lecture, inspection de l'arborescence) de manière programmable et testée.

## Fonctionnalités

Le module `src/repo_manager.py` inclut :
- `create_file(filepath, content)` : Crée un fichier avec le contenu spécifié et s'assure que les répertoires parents existent.
- `read_file_content(filepath)` : Lit et renvoie le contenu texte d'un fichier en UTF-8.
- `list_structure(base_dir)` : Retourne la liste ordonnée des chemins relatifs des fichiers d'un répertoire (en excluant les dossiers masqués).

## Structure du projet

- `src/` : Modules Python (`repo_manager.py`).
- `tests/` : Tests unitaires automatisés (`test_repo_manager.py`).
- `pytest.ini` : Configuration pytest pour la résolution des imports.
- `.gitignore` : Exclusion des caches et artefacts de compilation.

## Exécution des tests

Pour lancer les tests automatisés :

```bash
pytest
```
