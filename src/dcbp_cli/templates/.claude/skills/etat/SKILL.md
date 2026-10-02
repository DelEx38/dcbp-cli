---
name: etat
tool: dcbp
description: "Vue d'ensemble rapide du projet DCBP. Affiche l'état actuel, les tâches en cours et les prochaines étapes."
allowed-tools: Read, Glob
---

# /etat - Vue d'Ensemble du Projet

Affiche un résumé complet de l'état du projet.

## Workflow

### Phase 1: Collect
1. Lire `.claude/dcbp/STATE.md` - état courant, objectif, blockers
2. Lire `.claude/dcbp/TASKS.md` - état du backlog
3. Lire `.claude/dcbp/ISSUES.md` - bugs ouverts
4. Lire `.claude/dcbp/PROJECT.md` - contexte général si nécessaire

### Phase 2: Summarize
1. Résumer l'état actuel du projet depuis STATE.md
2. Lister les tâches en cours
3. Lister les blocages éventuels
4. Suggérer les prochaines actions

## Template de sortie

```markdown
## Status: [nom projet]

### État courant
- Phase: ...
- Statut: ...
- Objectif: ...

### En cours
- [ ] Tâche 1
- [ ] Tâche 2

### Blocages
- Aucun / Liste...

### Bugs ouverts
- X critique(s), Y majeur(s)

### Prochaines étapes suggérées
1. ...
2. ...
```
