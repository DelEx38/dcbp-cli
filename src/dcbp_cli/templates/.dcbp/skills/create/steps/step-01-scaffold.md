# Step 01 - Scaffold

## Objectif

Créer la structure de fichiers du projet selon le type choisi.

## Instructions

### Si `{project_type}` == "python"

Créer la structure suivante :

#### 1. Structure des dossiers

```
src/{package_name}/__init__.py
src/{package_name}/main.py
tests/__init__.py
```

#### 2. Fichiers de configuration

**pyproject.toml** :
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

**requirements.txt** :
```
# Production dependencies
```

**requirements-dev.txt** :
```
pytest>=7.0
pytest-cov>=4.0
ruff>=0.1.0
```

**.gitignore** :
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
.venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Environment
.env
.env.local
```

**README.md** :
```markdown
# {project_name}

## Installation

\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

pip install -e ".[dev]"
\`\`\`

## Usage

\`\`\`bash
python -m {package_name}
\`\`\`

## Tests

\`\`\`bash
pytest
\`\`\`
```

**src/{package_name}/__init__.py** :
```python
"""Package {package_name}."""

__version__ = "0.1.0"
```

**src/{package_name}/main.py** :
```python
"""Point d'entrée principal."""


def main() -> None:
    """Fonction principale."""
    print("Hello, World!")


if __name__ == "__main__":
    main()
```

**tests/__init__.py** :
```python
"""Tests pour {package_name}."""
```

---

### Si `{project_type}` == "django"

Créer la structure suivante :

#### 1. Utiliser django-admin

Exécuter :
```bash
pip install django
django-admin startproject {package_name} .
```

#### 2. Structure additionnelle

```
apps/.gitkeep
static/.gitkeep
templates/base.html
```

#### 3. Fichiers de configuration

**requirements.txt** :
```
Django>=5.0
python-dotenv>=1.0
```

**requirements-dev.txt** :
```
pytest>=7.0
pytest-django>=4.5
ruff>=0.1.0
```

**.gitignore** (ajouter au .gitignore Django standard) :
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# Virtual environments
venv/
.venv/

# IDE
.vscode/
.idea/

# Django
*.log
local_settings.py
db.sqlite3
media/

# Environment
.env
.env.local

# Static files (collectstatic)
staticfiles/
```

**.env.example** :
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

**templates/base.html** :
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{project_name}{% endblock %}</title>
    {% block extra_head %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

**README.md** :
```markdown
# {project_name}

Application Django.

## Installation

\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt
\`\`\`

## Configuration

\`\`\`bash
cp .env.example .env
# Éditer .env avec vos valeurs
\`\`\`

## Lancer le serveur

\`\`\`bash
python manage.py migrate
python manage.py runserver
\`\`\`

## Tests

\`\`\`bash
pytest
\`\`\`
```

#### 4. Modifier settings.py

Ajouter dans `{package_name}/settings.py` :
- TEMPLATES DIRS: `[BASE_DIR / 'templates']`
- STATICFILES_DIRS: `[BASE_DIR / 'static']`
- Support de python-dotenv pour les variables d'environnement

## Output

Liste des fichiers créés avec confirmation.

## Transition

Passer à **step-02-complete.md**
