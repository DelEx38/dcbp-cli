---
name: create
description: "Crée un nouveau projet Python ou Django après initialisation de DCBP. Utilise /create pour démarrer un projet avec une structure prête à l'emploi."
argument-hint: "[python|django]"
---

# /create - Création de Projet Python/Django

Workflow pour créer un nouveau projet Python ou Django avec une structure minimale et fonctionnelle.

## Commande

```
/create [python|django]
```

## Types de Projets

| Type | Description |
|------|-------------|
| `python` | Projet Python basique (script/CLI/lib) |
| `django` | Application web Django |

## Workflow (3 Phases)

| Phase | Nom | Objectif |
|-------|-----|----------|
| 00 | Init | Détermine le type de projet (demande si non spécifié) |
| 01 | Scaffold | Crée la structure de fichiers |
| 02 | Complete | Met à jour PROJECT.md, résumé final |

## Structure Créée

### Python Basique

```
{project_name}/
├── src/
│   └── {package_name}/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── __init__.py
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── README.md
└── pyproject.toml
```

### Django

```
{project_name}/
├── {project_name}/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   └── .gitkeep
├── static/
│   └── .gitkeep
├── templates/
│   └── base.html
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── README.md
├── manage.py
└── .env.example
```

## Variables d'état

| Variable | Description |
|----------|-------------|
| `{project_type}` | `python` ou `django` |
| `{project_name}` | Nom du projet (kebab-case) |
| `{package_name}` | Nom du package Python (snake_case) |

## Intégration Mémoire

Ce workflow :
1. **Met à jour** PROJECT.md avec la stack du projet créé
2. **Ajoute** une entrée dans PROGRESS.md
3. **Configure** les commandes de validation appropriées

## Exemples

```bash
# Demande interactivement le type
/create

# Créer un projet Python
/create python

# Créer un projet Django
/create django
```

## Point d'entrée

**PREMIÈRE ACTION :** Charger `steps/step-00-init.md`
