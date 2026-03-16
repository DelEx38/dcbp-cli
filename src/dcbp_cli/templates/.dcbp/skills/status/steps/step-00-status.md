# Step 00 - Status

## Objectif

Afficher une vue d'ensemble complète du projet.

## Instructions

### 1. Lire la mémoire

Lire les fichiers suivants :
- `.claude/dcbp/PROJECT.md` - Contexte général
- `.claude/dcbp/PROGRESS.md` - Dernières sessions
- `.claude/dcbp/TASKS.md` - État du backlog
- `.claude/dcbp/ISSUES.md` - Bugs ouverts

### 2. Extraire les informations clés

#### Depuis PROJECT.md
- Nom du projet
- Stack technique
- Commandes principales

#### Depuis PROGRESS.md
- Date de la dernière session
- Ce qui a été fait récemment
- Prochaines étapes mentionnées

#### Depuis TASKS.md
- Tâches en cours (`[~]` ou `- [ ]` sous "En cours")
- Nombre de tâches à faire
- Nombre de tâches terminées

#### Depuis ISSUES.md
- Bugs critiques ouverts
- Bugs majeurs ouverts
- Dette technique notable

### 3. Générer le rapport

```markdown
════════════════════════════════════════════════════
STATUS: [Nom du projet]
════════════════════════════════════════════════════

## Stack
[Stack résumée]

## Dernière activité
- **Date** : [Date]
- **Résumé** : [Ce qui a été fait]

## Tâches

### En cours
- [ ] Tâche 1
- [ ] Tâche 2

### À faire (priorité haute)
- [ ] Tâche 3
- [ ] Tâche 4

**Total** : X en cours, Y à faire, Z terminées

## Bugs ouverts
- **Critiques** : X
- **Majeurs** : Y

[Liste des critiques si présents]

## Prochaines étapes suggérées
1. [Étape 1 - basée sur PROGRESS.md ou TASKS.md]
2. [Étape 2]
3. [Étape 3]

────────────────────────────────────────────────────
Commands: /dev <feature> | /debug <bug> | /review <file>
════════════════════════════════════════════════════
```

## Fin du workflow

Le skill /status est terminé.
