---
name: bugfix
tool: dcbp
description: "Investigation et correction de bugs avec workflow BUG-XXX."
argument-hint: "<description du bug | BUG-XXX>"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# /bugfix — Investigation de Bugs

Investigation et correction de bugs. Utilise le même cycle workflow que /dev.

## Usage

```
/bugfix <description du bug>    # Nouveau bug → formalise + exécute
/bugfix BUG-XXX                  # Reprendre un bug en cours
```

## Identifiants

Namespace : `BUG-XXX` (BUG-001, BUG-002, ...)

## Workflow

### Phase 1: Formaliser (si nouveau bug)

Si aucun identifiant BUG-XXX fourni :
1. Comprendre le bug décrit
2. Créer `.claude/dcbp/tasks/BUG-XXX.md` avec :
   - Objective : corriger ce bug
   - Scope : fichiers / composants concernés
   - Acceptance Criteria : comportement attendu vs actuel
3. Indexer dans TASKS.md
4. Mettre STATE.md à jour

Transition : `REQUEST → READY`

### Phase 2: Reproduce

1. Identifier les étapes de reproduction
2. Confirmer comportement attendu vs actuel
3. Marquer la tâche `IMPLEMENTING`

Transition : `READY → IMPLEMENTING`

### Phase 3: Investigate

1. Localiser le code concerné
2. Analyser les causes possibles
3. Identifier la cause racine

### Phase 4: Fix

1. Implémenter le correctif
2. S'assurer de ne pas introduire de régression
3. Lancer les tests

### Phase 5: Transition vers VERIFYING

1. Mettre le statut à `VERIFYING`
2. Mettre STATE.md et TASKS.md à jour
3. Présenter le résumé pour /review

Transition : `IMPLEMENTING → VERIFYING`

**Note** : La transition `VERIFYING → DONE` appartient à `/review`.
