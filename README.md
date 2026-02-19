# DCBP - DC Blueprint pour Claude Code

> Systeme de memoire persistante et workflows structures pour Claude Code.

DCBP resout un probleme fondamental de Claude Code : **la perte de contexte entre les sessions**. En structurant la memoire du projet et en fournissant des workflows guides, DCBP permet a Claude de reprendre exactement la ou il s'etait arrete.

---

## Table des matieres

- [Concept](#concept)
- [Installation](#installation)
- [Demarrage rapide](#demarrage-rapide)
- [Structure des fichiers](#structure-des-fichiers)
- [Fichiers de memoire](#fichiers-de-memoire)
- [Skills disponibles](#skills-disponibles)
- [Workflow /create en detail](#workflow-create-en-detail)
- [Workflow /dev en detail](#workflow-dev-en-detail)
- [Workflow /start en detail](#workflow-start-en-detail)
- [Workflow /archive en detail](#workflow-archive-en-detail)
- [Flags et options](#flags-et-options)
- [Bonnes pratiques](#bonnes-pratiques)
- [Mise a jour](#mise-a-jour)
- [Token Usage](#token-usage)

---

## Concept

### Le probleme

Claude Code perd son contexte entre les sessions. A chaque nouvelle conversation :
- Il ne sait plus ou en etait le projet
- Il oublie les decisions prises precedemment
- Il peut refaire des erreurs deja corrigees
- Il ne connait pas les conventions du projet

### La solution DCBP

DCBP cree une **memoire persistante** via des fichiers Markdown que Claude lit au debut de chaque session :

1. **CLAUDE.md** - Point d'entree automatique, charge par Claude Code
2. **Fichiers de memoire** - Contexte, progres, decisions, taches
3. **Skills structures** - Workflows guides etape par etape

---

## Installation

### Depuis GitHub

```bash
pip install git+https://github.com/DelEx38/dcbp-cli.git
```

### En developpement local

```bash
git clone https://github.com/DelEx38/dcbp-cli.git
cd dcbp-cli
pip install -e .
```

### Verification

```bash
dcbp --version
# dcbp-cli 0.1.0
```

---

## Demarrage rapide

### 1. Initialiser DCBP dans votre projet

```bash
cd mon-projet
dcbp init
```

L'assistant vous posera quelques questions :

```
============================================================
  DCBP v0.1.0 - Initialisation du projet
============================================================

Repondez aux questions suivantes pour configurer votre projet.
(Appuyez sur Entree pour accepter la valeur par defaut)

Nom du projet [mon-projet]:
Description courte [Un projet genial]: Mon application web

Langage principal ?
  1. Python
  2. JavaScript/TypeScript
  3. Go
  4. Rust
  5. Autre
Choix [1]: 1

Framework Python ?
  1. FastAPI
  2. Django
  3. Flask
  4. CLI (Click/Typer)
  5. Script simple
  6. Autre
Choix [1]: 1

Base de donnees ?
  1. PostgreSQL
  2. MySQL
  3. SQLite
  4. MongoDB
  5. Redis
  6. Aucune
  7. Autre
Choix [6]: 1

============================================================
  [OK] DCBP initialise avec succes!
============================================================

  Projet    : mon-projet
  Langage   : Python
  Framework : FastAPI
  Database  : PostgreSQL
```

### Mode rapide (sans questions)

```bash
dcbp init --quick   # Utilise les templates par defaut
```

### 2. Configuration manuelle (optionnel)

Si vous voulez ajuster la configuration, editez `.dcbp/PROJECT.md` :

```markdown
# Mon Projet

## Stack technique
- **Langage** : Python 3.11
- **Framework** : FastAPI
- **Base de donnees** : PostgreSQL
- **Tests** : pytest

## Conventions
- Code en anglais, commentaires en francais
- Type hints obligatoires
- Docstrings Google style

## Architecture
src/
├── api/          # Endpoints REST
├── services/     # Logique metier
├── models/       # Modeles SQLAlchemy
└── utils/        # Utilitaires
```

### 3. Utiliser les skills

Dans Claude Code, utilisez les commandes :

```
/dev ajouter l'authentification JWT
/debug le endpoint /users retourne 500
/review src/api/auth.py
/status
```

---

## Structure des fichiers

Apres `dcbp init`, votre projet contient :

```
mon-projet/
├── CLAUDE.md                    # Point d'entree Claude Code
└── .dcbp/
    ├── PROJECT.md               # [EDITER] Configuration projet
    ├── PROGRESS.md              # Journal des sessions
    ├── TASKS.md                 # Backlog et taches
    ├── ISSUES.md                # Bugs et dette technique
    ├── DECISIONS.md             # Decisions architecturales
    ├── archive/                 # Sessions archivees (via /archive)
    ├── output/                  # Fichiers generes (optionnel)
    ├── skills/
    │   ├── create/
    │   │   ├── SKILL.md         # Definition du skill /create
    │   │   └── steps/
    │   │       ├── step-00-init.md
    │   │       ├── step-01-scaffold.md
    │   │       └── step-02-complete.md
    │   └── dev/
    │       ├── SKILL.md         # Definition du skill /dev
    │       └── steps/
    │           ├── step-00-init.md
    │           ├── step-01-context.md
    │           ├── step-02-design.md
    │           ├── step-03-implement.md
    │           ├── step-04-verify.md
    │           ├── step-05-review.md
    │           └── step-06-complete.md
    └── scripts/
        ├── init_task.py         # Initialisation de taches
        ├── update_progress.py   # Mise a jour du progres
        └── sync_memory.py       # Synchronisation memoire
```

---

## Fichiers de memoire

### PROJECT.md - Configuration du projet

**But** : Donner a Claude le contexte technique permanent du projet.

**Contenu recommande** :
- Stack technique (langages, frameworks, outils)
- Conventions de code (style, nommage, documentation)
- Architecture du projet (structure des dossiers)
- Commandes utiles (build, test, deploy)
- Points d'attention specifiques

**Quand le modifier** : Au debut du projet, puis lors de changements majeurs.

---

### PROGRESS.md - Journal des sessions

**But** : Tracer l'historique du travail effectue.

**Format** :
```markdown
## Session 2024-01-15 - Ajout authentification

### Ce qui a ete fait
- [x] Cree le modele User
- [x] Implemente JWT auth
- [x] Ajoute les tests

### Decisions
> **Decision :** Utiliser python-jose pour JWT (plus leger que PyJWT)

### Problemes rencontres
- [Probleme] CORS bloquait les cookies -> [Solution] Ajoute allow_credentials=True

### Prochaines etapes
- [ ] Ajouter refresh tokens
- [ ] Implementer logout
```

**Quand le modifier** : Automatiquement par les workflows, ou manuellement en fin de session.

---

### TASKS.md - Backlog et taches

**But** : Suivre les taches a faire, en cours et terminees.

**Format** :
```markdown
## En cours
- [ ] #feature Authentification JWT (DEV-003)

## A faire
### Priorite haute
- [ ] #feature Reset password
- [ ] #bugfix Fix memory leak

### Priorite basse
- [ ] #refactor Nettoyer les imports

## Termine
- [x] #feature Setup projet (DEV-001)
- [x] #feature Modele User (DEV-002)
```

**Quand le modifier** : Lors de la planification et apres chaque tache completee.

---

### ISSUES.md - Bugs et dette technique

**But** : Documenter les problemes connus et la dette technique.

**Format** :
```markdown
## Bugs actifs

### BUG-001 : Memory leak sur /export (Severite: Haute)
- **Symptome** : RAM augmente progressivement
- **Reproduction** : Exporter > 1000 lignes
- **Cause suspectee** : Fichier temporaire non ferme

## Dette technique

### DEBT-001 : Tests manquants sur auth
- **Impact** : Risque de regression
- **Effort estime** : 2h
```

**Quand le modifier** : Quand un bug est decouvert ou resolu.

---

### DECISIONS.md - Decisions architecturales

**But** : Documenter les decisions importantes pour ne pas les rediscuter.

**Format** :
```markdown
## DEC-001 : Choix de FastAPI vs Flask (2024-01-10)

### Contexte
Besoin d'un framework async pour gerer les webhooks.

### Options considerees
1. **Flask** - Simple mais sync
2. **FastAPI** - Async natif, validation Pydantic
3. **Django** - Trop lourd pour ce cas

### Decision
FastAPI

### Justification
- Support async natif pour les webhooks
- Validation automatique avec Pydantic
- Documentation OpenAPI generee
```

**Quand le modifier** : Lors de decisions architecturales importantes.

---

## Skills disponibles

| Commande | Description | Quand l'utiliser |
|----------|-------------|------------------|
| `/start` | Initialisation de session complete | Debut de chaque session |
| `/dev <feature>` | Developpement structure en 7 etapes | Nouvelle fonctionnalite |
| `/debug <bug>` | Investigation et correction | Bug a resoudre |
| `/review <cible>` | Revue de code | Avant merge/commit |
| `/status` | Vue d'ensemble du projet | Vue rapide de l'etat |
| `/archive [n]` | Archivage de PROGRESS.md | Quand PROGRESS.md > 10KB |
| `/create [python\|django]` | Scaffold de code (optionnel) | Creer la structure de fichiers |

### Exemples d'utilisation

```
/start                     # Initialise la session (contexte + taches + suggestions)

/create                    # Demande interactivement Python ou Django
/create python             # Cree un projet Python basique
/create django             # Cree un projet Django

/dev ajouter un systeme de notifications par email
/dev -a implementer le CRUD pour les produits
/dev -r DEV-005 reprendre la tache en cours

/debug le login retourne 401 meme avec les bons credentials
/debug -a les tests echouent sur CI mais passent en local

/review src/services/payment.py
/review les derniers commits

/status                    # Vue d'ensemble rapide

/archive                   # Archive PROGRESS.md (garde 5 sessions)
/archive 3                 # Garde seulement les 3 dernieres sessions
```

---

## Workflow /create en detail

Le skill `/create` permet de creer un nouveau projet Python ou Django apres avoir initialise DCBP.

### Quand l'utiliser

- Apres `dcbp init` dans un dossier vide
- Pour demarrer un nouveau projet avec une structure propre
- Pour configurer automatiquement PROJECT.md

### Types de projets

| Type | Description | Structure |
|------|-------------|-----------|
| `python` | Projet Python basique (script, CLI, lib) | src/, tests/, pyproject.toml |
| `django` | Application web Django | manage.py, apps/, templates/, static/ |

### Workflow en 3 phases

#### Phase 0 : Init
- Demande le type de projet (si non specifie)
- Demande le nom du projet
- Determine l'emplacement de creation

#### Phase 1 : Scaffold
- Cree la structure de fichiers appropriee
- Configure les outils (pytest, ruff)
- Genere les fichiers de base (requirements.txt, .gitignore, README.md)

#### Phase 2 : Complete
- Met a jour PROJECT.md avec la stack du projet
- Ajoute une entree dans PROGRESS.md
- Affiche les prochaines etapes

### Structure creee

#### Python basique

```
mon-projet/
├── src/
│   └── mon_projet/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── __init__.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
└── README.md
```

#### Django

```
mon-projet/
├── mon_projet/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
├── templates/
│   └── base.html
├── static/
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── .env.example
└── README.md
```

### Exemples

```bash
# Interactif : demande le type et le nom
/create

# Direct : cree un projet Python nomme "mon-cli"
/create python
# > Nom du projet : mon-cli

# Direct : cree un projet Django
/create django
# > Nom du projet : mon-app-web
```

---

## Workflow /dev en detail

Le skill `/dev` suit une methodologie en **7 phases** inspiree d'APEX :

### Phase 0 : Init
**But** : Initialiser la tache et creer un identifiant unique.

- Genere un `task_id` (ex: DEV-007)
- Cree un fichier de suivi dans `.dcbp/output/`
- Parse les flags (-a, -s, -r)

**Output** : `task_id` et contexte initial

---

### Phase 1 : Context
**But** : Comprendre le codebase existant.

- Lit PROJECT.md pour le contexte projet
- Lit PROGRESS.md pour l'historique recent
- Analyse les fichiers pertinents
- Identifie les patterns existants

**Output** : Resume du contexte et fichiers cles identifies

---

### Phase 2 : Design
**But** : Concevoir le plan d'implementation.

- Definit l'approche technique
- Liste les fichiers a creer/modifier
- Identifie les dependances
- Estime la complexite

**Output** : Plan detaille avec etapes

**Point de validation** : En mode normal, demande confirmation avant d'implementer.

---

### Phase 3 : Implement
**But** : Ecrire le code.

- Suit le plan etabli
- Respecte les conventions du projet
- Cree/modifie les fichiers necessaires
- Documente le code

**Output** : Code implemente

---

### Phase 4 : Verify
**But** : Valider le code produit.

- Execute les linters (si configures)
- Verifie les types (si TypeScript/mypy)
- Lance les tests unitaires
- Verifie que le build passe

**Output** : Rapport de validation

---

### Phase 5 : Review
**But** : Auto-revue du code.

- Verifie la qualite du code
- Detecte les problemes potentiels
- Suggere des ameliorations
- Valide la couverture de tests

**Output** : Rapport de review avec recommandations

---

### Phase 6 : Complete
**But** : Finaliser et mettre a jour la memoire.

- Met a jour PROGRESS.md avec le travail effectue
- Met a jour TASKS.md (tache completee)
- Ajoute les decisions dans DECISIONS.md si necessaire
- Genere un resume de session

**Output** : Memoire mise a jour, tache marquee complete

---

## Workflow /start en detail

Le skill `/start` initialise une session de travail avec tout le contexte necessaire.

### Ce que fait /start

1. **Charge la memoire complete** - PROJECT, PROGRESS, TASKS, ISSUES, DECISIONS
2. **Resume la derniere session** - Ce qui a ete fait, prochaines etapes
3. **Affiche les taches actives** - En cours et prioritaires
4. **Liste les issues ouvertes** - Bugs et dette technique
5. **Suggere des actions** - 3 actions concretes basees sur le contexte

### Exemple de sortie

```
╔════════════════════════════════════════════════════════════╗
║  SESSION DCBP INITIALISEE                                  ║
╚════════════════════════════════════════════════════════════╝

## Projet : Mon App

**Stack** : Python 3.11, FastAPI, PostgreSQL

## Derniere session

**[2026-02-18]** - Ajout authentification JWT
- Implementation du login/logout
- Tests unitaires

→ Prochaines etapes : Ajouter refresh tokens

## Taches

### En cours [~]
- [~] Refresh tokens

### A faire (priorite haute)
- [ ] Reset password

## Suggestions pour cette session

1. **Continuer refresh tokens** - Tache en cours
2. **Corriger BUG-003** - Bug critique ouvert
3. **Implementer reset password** - Priorite haute
```

---

## Workflow /archive en detail

Le skill `/archive` archive les anciennes sessions de PROGRESS.md pour economiser des tokens.

### Pourquoi archiver ?

PROGRESS.md grandit avec le temps. Apres 20 sessions, il peut atteindre 15-20 KB (~5000 tokens), ce qui consomme une part significative de votre quota.

### Commandes

```
/archive        # Garde les 5 dernieres sessions (defaut)
/archive 3      # Garde les 3 dernieres sessions
/archive 10     # Garde les 10 dernieres sessions
```

### Structure des archives

```
.dcbp/
├── PROGRESS.md              # Sessions recentes (5 dernieres)
└── archive/
    ├── PROGRESS-2026-01.md  # Archive janvier
    ├── PROGRESS-2026-02.md  # Archive fevrier
    └── ...
```

### Quand archiver ?

- Quand PROGRESS.md depasse 10 KB
- Periodiquement (1x par mois)
- Avant une longue session pour maximiser les tokens disponibles

---

## Flags et options

### Flags communs

| Flag | Description | Exemple |
|------|-------------|---------|
| `-a` | Mode autonome (sans confirmations) | `/dev -a feature` |
| `-s` | Sauvegarde les outputs dans `.dcbp/output/` | `/dev -s feature` |
| `-r <id>` | Reprendre une tache existante | `/dev -r DEV-005` |

### Combinaisons

```bash
# Developpement autonome avec sauvegarde
/dev -a -s implementer le cache Redis

# Reprendre une tache en mode autonome
/dev -a -r DEV-003
```

### Mode autonome (-a)

En mode autonome, Claude :
- Ne demande pas de confirmation entre les phases
- Prend les decisions de maniere independante
- Continue jusqu'a completion ou erreur

**Recommande pour** : Taches bien definies, corrections mineures.

**Deconseille pour** : Nouvelles fonctionnalites complexes, refactoring majeur.

---

## Bonnes pratiques

### 1. Toujours commencer par /start

Au debut de chaque session, lancez `/start` pour que Claude :
- Charge tout le contexte (PROJECT, PROGRESS, TASKS, ISSUES, DECISIONS)
- Affiche la derniere session et les prochaines etapes
- Liste les taches en cours et prioritaires
- Suggere des actions concretes pour la session

### 2. Maintenir PROJECT.md a jour

Un PROJECT.md bien rempli = un Claude plus efficace.

Incluez :
- La stack complete
- Les commandes de build/test/deploy
- Les conventions de code
- Les points d'attention

### 3. Documenter les decisions

Utilisez DECISIONS.md pour :
- Eviter de rediscuter les memes choix
- Expliquer pourquoi (pas juste quoi)
- Tracer l'evolution de l'architecture

### 4. Utiliser les bons flags

- `-a` pour les taches simples et bien definies
- Sans flag pour les taches complexes (validation a chaque etape)
- `-r` pour reprendre apres une interruption

### 5. Nettoyer regulierement

- Archivez les vieilles sessions de PROGRESS.md
- Fermez les taches completees dans TASKS.md
- Resolvez les issues dans ISSUES.md

---

## Mise a jour

### Mettre a jour les templates

Quand une nouvelle version de DCBP sort :

```bash
pip install --upgrade git+https://github.com/DelEx38/dcbp-cli.git
cd mon-projet
dcbp update
```

La commande `update` :
- Met a jour les skills (`.dcbp/skills/`)
- Met a jour les scripts (`.dcbp/scripts/`)
- **Preserve** vos fichiers de memoire (PROJECT.md, PROGRESS.md, etc.)

### Reinitialiser completement

Pour repartir de zero (perte de la memoire) :

```bash
dcbp init --force
```

---

## Token Usage

DCBP est optimise pour minimiser l'utilisation du context window de Claude.

### Chargement progressif

Les steps du workflow `/dev` sont charges **un par un**, pas tous en meme temps. Cela economise des tokens.

### Estimation des tokens

| Composant | Tokens (approx) |
|-----------|-----------------|
| CLAUDE.md | ~820 |
| PROJECT.md | ~540 |
| PROGRESS.md (5 sessions) | ~2000 |
| TASKS.md | ~205 |
| ISSUES.md | ~200 |
| DECISIONS.md | ~390 |
| **Memoire complete** | **~4150** |

### Cout par action

| Action | Tokens (input) |
|--------|----------------|
| `/start` (lit tout) | ~5700 |
| `/status` (vue rapide) | ~3000 |
| `/dev` (1 step) | ~1500-2000 |
| `/archive` | ~500 |

### Limites par abonnement (Claude)

| Plan | Tokens/fenetre | Reset |
|------|----------------|-------|
| Pro | ~44,000 | 5h |
| Max5 | ~88,000 | 5h |
| Max20 | ~220,000 | 5h |

### Impact sur votre quota

Avec un abonnement **Pro** (44K tokens/5h) :
- `/start` consomme ~13% du quota
- Une session complete (3-4 echanges) : ~35-45%
- Vous pouvez faire 2-3 sessions confortables par fenetre

### Optimisation : /archive

Utilisez `/archive` regulierement pour reduire la taille de PROGRESS.md :

| PROGRESS.md | Tokens | Apres /archive |
|-------------|--------|----------------|
| 20 sessions (~15 KB) | ~4300 | ~2000 (5 sessions) |
| **Economie** | | **~2300 tokens** |

---

## Depannage

### DCBP ne se charge pas

Verifiez que :
1. `CLAUDE.md` est a la racine du projet
2. Le dossier `.dcbp/` existe
3. Vous etes dans le bon repertoire

### Les skills ne fonctionnent pas

1. Verifiez que `.dcbp/skills/` contient les fichiers
2. Essayez `dcbp update` pour reinstaller les templates

### Claude oublie le contexte

1. Lancez `/status` en debut de session
2. Verifiez que PROJECT.md est bien rempli
3. Assurez-vous que PROGRESS.md contient l'historique recent

---

## Licence

MIT

---

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le repository
2. Creez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements
4. Poussez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request
