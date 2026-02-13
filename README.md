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
- [Workflow /dev en detail](#workflow-dev-en-detail)
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
pip install git+https://github.com/YOUR_USERNAME/dcbp-cli.git
```

### En developpement local

```bash
git clone https://github.com/YOUR_USERNAME/dcbp-cli.git
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

Output :
```
[*] Initialisation de DCBP v0.1.0 dans /path/to/mon-projet

[+] Cree .dcbp/
[+] Cree CLAUDE.md

==================================================
[OK] DCBP initialise avec succes!
==================================================
```

### 2. Configurer votre projet

Editez `.dcbp/PROJECT.md` avec les informations de votre projet :

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
    ├── output/                  # Fichiers generes (optionnel)
    ├── skills/
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
| `/dev <feature>` | Developpement structure en 7 etapes | Nouvelle fonctionnalite |
| `/debug <bug>` | Investigation et correction | Bug a resoudre |
| `/review <cible>` | Revue de code | Avant merge/commit |
| `/status` | Vue d'ensemble du projet | Debut de session |

### Exemples d'utilisation

```
/dev ajouter un systeme de notifications par email
/dev -a implementer le CRUD pour les produits
/dev -r DEV-005 reprendre la tache en cours

/debug le login retourne 401 meme avec les bons credentials
/debug -a les tests echouent sur CI mais passent en local

/review src/services/payment.py
/review les derniers commits

/status
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

### 1. Toujours commencer par /status

Au debut de chaque session, lancez `/status` pour que Claude :
- Lise le contexte du projet
- Voie l'historique recent
- Identifie les taches en cours

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
pip install --upgrade git+https://github.com/YOUR_USERNAME/dcbp-cli.git
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
| CLAUDE.md | ~200 |
| PROJECT.md (rempli) | ~300 |
| PROGRESS.md (3 sessions) | ~250 |
| TASKS.md | ~100 |
| Skill /dev (1 step) | ~400 |
| **Memoire de base** | **~850** |
| **Workflow /dev complet** | **~6,600** |

### Pourcentage du context window

| Modele | Context | Usage DCBP |
|--------|---------|------------|
| Claude 3.5 Sonnet | 200K | ~3.3% |
| Claude 3 Opus | 200K | ~3.3% |

DCBP utilise moins de **4%** du context window, laissant 96% pour votre code et vos conversations.

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
