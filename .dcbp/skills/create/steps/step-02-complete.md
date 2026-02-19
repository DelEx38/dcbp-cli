# Step 02 - Completion

## Objectif

Mettre à jour la mémoire DCBP et fournir un résumé final.

## Instructions

### 1. Mettre à jour PROJECT.md

Remplacer le contenu de `.dcbp/PROJECT.md` avec les informations du projet créé.

#### Pour Python basique :

```markdown
# {project_name}

> Description du projet

## Stack Technique

| Catégorie | Technologie |
|-----------|-------------|
| Langage | Python 3.10+ |
| Tests | pytest |
| Linting | ruff |
| Build | setuptools |

## Structure

```
src/{package_name}/    # Code source
tests/                 # Tests unitaires
```

## Commandes

| Action | Commande |
|--------|----------|
| Install | `pip install -e ".[dev]"` |
| Run | `python -m {package_name}` |
| Test | `pytest` |
| Lint | `ruff check .` |
| Format | `ruff format .` |

## Conventions

- Style: PEP 8 via ruff
- Types: Type hints recommandés
- Tests: pytest, un fichier test_*.py par module
```

#### Pour Django :

```markdown
# {project_name}

> Application web Django

## Stack Technique

| Catégorie | Technologie |
|-----------|-------------|
| Langage | Python 3.10+ |
| Framework | Django 5.0+ |
| Tests | pytest-django |
| Linting | ruff |

## Structure

```
{package_name}/    # Configuration Django
apps/              # Applications Django
templates/         # Templates HTML
static/            # Fichiers statiques
```

## Commandes

| Action | Commande |
|--------|----------|
| Install | `pip install -r requirements.txt` |
| Migrate | `python manage.py migrate` |
| Run | `python manage.py runserver` |
| Test | `pytest` |
| Lint | `ruff check .` |
| Shell | `python manage.py shell` |

## Conventions

- Apps dans `apps/`
- Templates dans `templates/`
- Static dans `static/`
- Variables d'env dans `.env`
```

### 2. Mettre à jour PROGRESS.md

Ajouter une nouvelle entrée :

```markdown
## {DATE} - Création du projet

### Ce qui a été fait
- [x] Création du projet {project_type}: {project_name}
- [x] Structure de base initialisée
- [x] Configuration des outils (ruff, pytest)
- [x] PROJECT.md mis à jour

### Prochaines étapes
- [ ] Configurer l'environnement virtuel
- [ ] Installer les dépendances
- [ ] Commencer le développement avec /dev
```

### 3. Résumé final

Afficher :

```
═══════════════════════════════════════════════════════
✓ Projet {project_name} créé avec succès !
═══════════════════════════════════════════════════════

Type: {project_type}
Emplacement: {chemin}

Prochaines étapes:

1. Créer l'environnement virtuel:
   python -m venv venv
   source venv/bin/activate  # ou: venv\Scripts\activate

2. Installer les dépendances:
   {commande_install}

3. Commencer le développement:
   /dev <votre première feature>

───────────────────────────────────────────────────────
Tip: Utilisez /status pour voir l'état du projet
═══════════════════════════════════════════════════════
```

## Fin du workflow

Le skill /create est terminé.
