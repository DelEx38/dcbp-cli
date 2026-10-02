---
name: start
tool: dcbp
description: "Initialise une nouvelle session de travail. Charge le contexte minimal."
allowed-tools: Read, Glob
---

# /start — Initialisation de Session

Charge le contexte minimal nécessaire pour reprendre le travail.

## Workflow

### Phase 1: Charger le contexte

1. Lire `.claude/dcbp/PROJECT.md` — stack, architecture, conventions
2. Lire `.claude/dcbp/STATE.md` — état courant, tâche active, prochaine action
3. Si une tâche est active (mentionnée dans STATE.md) : lire `.claude/dcbp/tasks/<ID>.md`
4. Lire `.claude/dcbp/TASKS.md` — aperçu rapide des statuts

Ne pas charger tout l'historique ni tout le backlog.

### Phase 2: Analyser

1. Identifier la tâche active et son statut workflow
2. Identifier les blockers éventuels
3. Déterminer la prochaine action concrète

### Phase 3: Afficher le résumé

```markdown
╔════════════════════════════════════════════════════════════╗
║  SESSION DCBP INITIALISÉE                                  ║
╚════════════════════════════════════════════════════════════╝

## Projet : [nom]

**Stack** : [stack résumée]

───────────────────────────────────────────────────────────────

## État courant

**Phase** : [phase]
**Tâche active** : [DEV-XXX — titre] ou Aucune
**Statut workflow** : [REQUEST | CLARIFYING | READY | IMPLEMENTING | VERIFYING | DONE | BLOCKED]

───────────────────────────────────────────────────────────────

## Prochaines actions suggérées

1. **[action prioritaire]** — [raison]
2. **[action secondaire]** — [raison]

───────────────────────────────────────────────────────────────
Skills : /task <demande> | /dev <ID> | /review <ID> | /bugfix <bug> | /etat
╚═════════════════════════════════════════════════════════════╝
```

### Note DONE ≠ PUSH

Si des tâches sont DONE mais non pushées, rappeler :
- `DONE` signifie validé techniquement
- Push nécessite une autorisation explicite (`.claude/dcbp/.push_auth`)
