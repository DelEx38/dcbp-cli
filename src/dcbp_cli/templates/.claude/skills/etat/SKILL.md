---
name: etat
tool: dcbp
description: "Vue d'ensemble rapide du projet DCBP. État, workflow, tâches actives."
allowed-tools: Read, Glob
---

# /etat — Vue d'Ensemble du Projet

Affiche l'état courant du projet et du workflow.

## Workflow

### Phase 1: Collect

1. Lire `.claude/dcbp/STATE.md` — état global, tâche active, blockers
2. Lire `.claude/dcbp/TASKS.md` — index des tâches et statuts
3. Lire `.claude/dcbp/ISSUES.md` — bugs ouverts
4. Si une tâche est active : lire `.claude/dcbp/tasks/<ID>.md`
5. Lire `.claude/dcbp/PROJECT.md` si contexte nécessaire

### Phase 2: Summarize

Présenter :

```markdown
## Status: [nom projet]

### État courant
- Phase: ...
- Statut global: ...

### Tâche active
- ID: DEV-XXX / BUG-XXX / Aucune
- Statut workflow: REQUEST | CLARIFYING | READY | IMPLEMENTING | VERIFYING | DONE | BLOCKED
- Titre: ...

### Tâches en VERIFYING (en attente de /review)
- DEV-XXX — titre

### Tâches READY (prêtes à exécuter)
- DEV-XXX — titre

### Blocages
- Aucun / Liste des blockers

### Bugs ouverts
- X critique(s), Y majeur(s)

### Prochaine action suggérée
1. ...
```

### Note workflow

Rappeler si nécessaire :
- `DONE` ≠ `PUSH_ALLOWED`
- Push nécessite une autorisation explicite séparée
