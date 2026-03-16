# Step 00 - Initialisation

## Objectif

Déterminer le type de projet à créer et collecter les informations nécessaires.

## Instructions

### 1. Parser l'argument

Si l'utilisateur a spécifié un type (`/create python` ou `/create django`), utiliser ce type.

### 2. Demander le type si non spécifié

Si aucun type n'est fourni, demander à l'utilisateur :

```
Quel type de projet voulez-vous créer ?

1. **Python** - Projet Python basique (script, CLI, bibliothèque)
   - Structure src/ avec package
   - pyproject.toml pour la configuration
   - Tests avec pytest

2. **Django** - Application web Django
   - Structure Django standard
   - Configuration prête pour le développement
   - Templates et static files organisés
```

### 3. Demander le nom du projet

Demander le nom du projet à l'utilisateur :
- Doit être en kebab-case (ex: `mon-super-projet`)
- Sera converti en snake_case pour le nom de package Python

### 4. Vérifier le répertoire

- Si on est dans un dossier vide (seulement .claude/dcbp/ et CLAUDE.md), créer à la racine
- Sinon, créer un sous-dossier avec le nom du projet

### 5. Définir les variables d'état

```
{project_type} = "python" | "django"
{project_name} = "nom-du-projet"
{package_name} = "nom_du_projet"
{create_in_root} = true | false
```

## Output

Résumé des choix :
- Type de projet sélectionné
- Nom du projet
- Emplacement de création

## Transition

Passer à **step-01-scaffold.md**
