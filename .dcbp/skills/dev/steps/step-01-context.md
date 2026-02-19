---
name: step-01-context
description: Exploration du codebase - comprendre ce qui EXISTE
prev_step: steps/step-00-init.md
next_step: steps/step-02-design.md
---

# Step 1: Contexte (Exploration)

## Règles

- 🛑 JAMAIS planifier ou proposer des solutions (c'est step-02)
- 🛑 JAMAIS créer de todos ou tâches
- ✅ Focus sur "Qu'est-ce qui EXISTE ?"
- ✅ Documenter avec chemins et numéros de ligne
- 📋 TU ES UN EXPLORATEUR, pas un planificateur

## Séquence

### 1. Extraire les mots-clés

De `{task_description}`, identifier :
- **Termes métier** : auth, user, payment...
- **Termes techniques** : API, route, component...
- **Actions** : créer, modifier, ajouter...

### 2. Explorer le codebase

**Utiliser les outils :**
- `Glob` pour trouver les fichiers : `**/*{keyword}*`
- `Grep` pour chercher dans le contenu
- `Read` pour examiner les fichiers pertinents

**Chercher :**
- Fichiers existants liés à la feature
- Patterns et conventions utilisés
- Utilitaires réutilisables
- Tests similaires

### 3. Documenter les trouvailles

```markdown
## Contexte Codebase

### Fichiers pertinents
| Fichier | Lignes | Contenu |
|---------|--------|---------|
| `src/auth/login.py` | 1-150 | Logique de login existante |
| `src/utils/validate.py` | 20-45 | Helpers de validation |

### Patterns observés
- **Routes** : Utilise FastAPI avec `@router.post`
- **Validation** : Pydantic models dans `schemas/`
- **Erreurs** : Exceptions custom dans `exceptions.py`

### Utilitaires disponibles
- `src/lib/auth.py` - Fonctions JWT
- `src/lib/db.py` - Session database

### Implémentations similaires
- `src/auth/login.py:42` - Flow de login (référence)

### Patterns de tests
- Tests dans `tests/` avec pytest
- Fixtures dans `conftest.py`
```

### 4. Inférer critères d'acceptation

```markdown
## Critères d'acceptation inférés

Basé sur "{task_description}" et les patterns existants :

- [ ] AC1: [critère mesurable]
- [ ] AC2: [critère mesurable]
- [ ] AC3: [critère mesurable]

_Seront affinés dans l'étape de design._
```

### 5. Résumé et transition

```
**Exploration terminée**

**Fichiers analysés:** {count}
**Patterns identifiés:** {count}
**Utilitaires trouvés:** {count}

**Points clés:**
- [résumé des fichiers pertinents]
- [patterns à suivre]

→ Passage au design...
```

**Puis charger** `step-02-design.md`

### 6. Sauvegarder (si save_mode)

Ajouter à `01-context.md` :
```markdown
---
## Étape complète
**Status:** ✓ Complete
**Fichiers analysés:** {count}
**Timestamp:** {ISO}
```

## Critères de succès

✅ Fichiers pertinents identifiés avec chemins et lignes
✅ Patterns documentés avec exemples
✅ Utilitaires listés
✅ Critères d'acceptation inférés
✅ AUCUNE planification ou proposition de solution
