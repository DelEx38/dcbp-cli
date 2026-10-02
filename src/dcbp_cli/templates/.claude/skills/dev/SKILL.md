---
name: dev
tool: dcbp
description: "Exécuteur de tâches READY. Implémente, teste, mène à VERIFYING."
argument-hint: "<DEV-XXX>"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# /dev — Exécution d'une Tâche

Exécute une tâche formalisée en statut `READY`. Conduit jusqu'à `VERIFYING`.

## Usage

```
/dev <DEV-XXX>        # Exécuter une tâche READY
/dev -r <DEV-XXX>     # Reprendre une tâche IMPLEMENTING
```

**Important** : `/dev` requiert une tâche existante en statut `READY` ou `IMPLEMENTING`.
Si aucune tâche valide n'existe, utilisez d'abord `/task <description>`.

## Workflow

### Phase 1: Init

1. Vérifier que `<DEV-XXX>` existe dans `.claude/dcbp/tasks/`
2. Lire le fichier de tâche — vérifier statut `READY` (ou `IMPLEMENTING` pour reprise)
3. Si statut invalide : expliquer et arrêter
4. Mettre le statut à `IMPLEMENTING` dans le fichier de tâche et TASKS.md
5. Mettre STATE.md à jour (tâche active, statut IMPLEMENTING)

Transition : `READY → IMPLEMENTING`

### Phase 2: Context

1. Lire `.claude/dcbp/PROJECT.md`
2. Lire `.claude/dcbp/STATE.md`
3. Lire uniquement le fichier de tâche concerné
4. Inspecter le code pertinent

### Phase 3: Implement

1. Suivre le plan du contrat de tâche
2. Respecter les conventions du projet (PROJECT.md)
3. Créer/modifier les fichiers nécessaires

### Phase 4: Verify

1. Exécuter les linters si configurés
2. Lancer les tests
3. Si des tests nécessaires échouent : rester en `IMPLEMENTING`

### Phase 5: Self-review

1. Relire les critères d'acceptation de la tâche
2. Vérifier que chaque critère est satisfait
3. Identifier les points que /review devra examiner

### Phase 6: Transition vers VERIFYING

1. Mettre le statut à `VERIFYING` dans le fichier de tâche et TASKS.md
2. Mettre STATE.md à jour
3. Présenter un résumé pour /review :
   - Critères d'acceptation vérifiés
   - Fichiers modifiés
   - Tests passants
   - Points d'attention pour la revue

Transition : `IMPLEMENTING → VERIFYING`

**Note** : `/dev` ne peut pas passer `VERIFYING → DONE`. Cette transition appartient à `/review`.
