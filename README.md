# Test_IA

Ce projet fournit des utilitaires modulaires d'interaction et de gestion du dépôt, permettant de manipuler des fichiers (création, lecture, inspection de l'arborescence, recherche, copie et métadonnées) de manière programmable et rigoureusement testée.

## Fonctionnalités

Le module `src/repo_manager.py` inclut :
- `create_file(filepath, content)` : Crée un fichier avec le contenu spécifié et s'assure que les répertoires parents existent.
- `read_file_content(filepath)` : Lit et renvoie le contenu texte d'un fichier en UTF-8.
- `list_structure(base_dir)` : Retourne la liste ordonnée des chemins relatifs des fichiers d'un répertoire (en excluant les dossiers masqués).
- `search_files(base_dir, pattern)` : Recherche des fichiers correspondant à un motif glob (ex: `*.py`, `*.md`).
- `copy_file(src_path, dest_path)` : Copie un fichier vers une destination en gérant l'arborescence cible.
- `get_file_metadata(filepath)` : Retourne des métadonnées sur un fichier (existence, taille en octets, type).

## Structure du projet

- `src/` : Modules Python (`repo_manager.py`).
- `tests/` : Tests unitaires automatisés (`test_repo_manager.py`).
- `pytest.ini` : Configuration pytest pour la résolution des imports.
- `.gitignore` : Exclusion des caches et artefacts de compilation.

## Exécution des tests

Pour lancer les tests automatisés :

```bash
pytest -v
```
