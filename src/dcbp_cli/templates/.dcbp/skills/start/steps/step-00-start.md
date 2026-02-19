# Step 00 - Start Session

## Objectif

Initialiser une session de travail avec tout le contexte nécessaire.

## Instructions

### 1. Charger la mémoire complète

Lire **tous** les fichiers de mémoire :

| Fichier | Contenu |
|---------|---------|
| `.dcbp/PROJECT.md` | Stack, architecture, conventions |
| `.dcbp/PROGRESS.md` | Journal des sessions |
| `.dcbp/TASKS.md` | Backlog et tâches en cours |
| `.dcbp/ISSUES.md` | Bugs et dette technique |
| `.dcbp/DECISIONS.md` | Décisions architecturales |

### 2. Analyser le contexte

#### Depuis PROGRESS.md
- Extraire la **dernière session** (date, ce qui a été fait)
- Identifier les **prochaines étapes** suggérées
- Noter les **décisions récentes**

#### Depuis TASKS.md
- Tâches **en cours** (`[~]`)
- Tâches **à faire prioritaires** (`[ ]` en haut de liste)
- Compter : en cours / à faire / terminées

#### Depuis ISSUES.md
- Bugs **critiques** et **majeurs** ouverts
- Dette technique importante

#### Depuis DECISIONS.md
- Décisions **récentes** (dernière semaine si daté)
- Décisions **en attente** de validation

### 3. Générer le rapport de session

```markdown
╔════════════════════════════════════════════════════════════╗
║  SESSION DCBP INITIALISÉE                                  ║
╚════════════════════════════════════════════════════════════╝

## Projet : [Nom depuis PROJECT.md]

**Stack** : [Stack résumée en 1 ligne]

───────────────────────────────────────────────────────────────

## Dernière session

**[Date]** - [Titre de la session]

### Ce qui a été fait
- [Point 1]
- [Point 2]
- [Point 3]

### Prochaines étapes suggérées
→ [Étape 1]
→ [Étape 2]

───────────────────────────────────────────────────────────────

## Tâches

### En cours [~]
- [~] Tâche 1
- [~] Tâche 2

### À faire (priorité haute)
- [ ] Tâche 3
- [ ] Tâche 4

**Statistiques** : X en cours | Y à faire | Z terminées

───────────────────────────────────────────────────────────────

## Issues ouvertes

| Sévérité | Count | Détails |
|----------|-------|---------|
| Critique | X | [Liste si > 0] |
| Majeur | Y | [Liste si > 0] |
| Mineur | Z | - |

**Dette technique** : [Résumé si présent]

───────────────────────────────────────────────────────────────

## Décisions récentes

- [Date] : [Décision 1]
- [Date] : [Décision 2]

───────────────────────────────────────────────────────────────

## Suggestions pour cette session

Basé sur le contexte, voici ce que tu pourrais faire :

1. **[Action prioritaire]** - [Raison]
2. **[Action secondaire]** - [Raison]
3. **[Action optionnelle]** - [Raison]

───────────────────────────────────────────────────────────────
Skills : /dev <feature> | /debug <bug> | /review <file> | /status
╚═════════════════════════════════════════════════════════════╝
```

### 4. Notes importantes

- Si un fichier mémoire est vide ou n'existe pas, l'indiquer simplement
- Si aucune tâche en cours, suggérer de commencer par les prioritaires
- Si des bugs critiques existent, les mettre en avant dans les suggestions
- Les suggestions doivent être **concrètes** et **actionnables**

## Fin du workflow

Le skill /start est terminé. Attendre les instructions de l'utilisateur.
