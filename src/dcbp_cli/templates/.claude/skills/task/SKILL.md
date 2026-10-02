---
name: task
tool: dcbp
description: "Formalise une demande en tâche READY avec contrat complet."
argument-hint: "<description de la demande>"
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /task — Formalisation d'une Tâche

Transforme une demande humaine en tâche exécutable avec contrat complet.

## Usage

```
/task <description de la demande>
/task -a <description>    # Mode autonome
```

## Workflow

### Phase 1: Comprendre

1. Lire `.claude/dcbp/PROJECT.md` — contexte, conventions, architecture
2. Lire `.claude/dcbp/STATE.md` — état courant, tâche active éventuelle
3. Inspecter le code si nécessaire pour comprendre le périmètre
4. Consulter TASKS.md / ISSUES.md / DECISIONS.md si pertinent

### Phase 2: Clarifier (si nécessaire)

Si la demande comporte des ambiguïtés qui changent réellement le contrat :

- Poser uniquement les questions à forte valeur
- Attendre les réponses avant de passer à Phase 3

Une demande simple et claire peut passer directement à READY.

Statut conceptuel : `REQUEST → CLARIFYING → READY`

### Phase 3: Formaliser

1. Déterminer le type et le prochain identifiant :
   - Développement : `DEV-XXX` (incrément depuis TASKS.md)
   - Bug : `BUG-XXX`
   - Dette technique : `DEBT-XXX`
2. Créer `.claude/dcbp/tasks/<ID>.md` avec le contrat complet :

```markdown
---
id: <ID>
status: READY
created: <YYYY-MM-DD>
type: dev|bug|debt
---

# <ID> — <Titre court>

## Objective
[Ce qui doit être accompli — résultat attendu]

## Scope
[Ce qui est inclus dans cette tâche]

## Acceptance Criteria
- [ ] Critère 1
- [ ] Critère 2

## Out of Scope
[Ce qui est explicitement exclu — optionnel si évident]

## Context
[Informations utiles à l'implémentation — optionnel]

## Dependencies
[Dépendances externes ou sur d'autres tâches — optionnel]

## Verification
[Ce que /review devra vérifier — optionnel]
```

3. Indexer dans TASKS.md :
   - Ajouter une ligne dans le tableau avec `| <ID> | <Titre> | READY |`
4. Mettre STATE.md à jour si approprié (tâche active, prochaine action)
5. Terminer en présentant la tâche formalisée

## Identifiants

Détermine le prochain numéro en lisant les tâches existantes dans :
- `.claude/dcbp/tasks/*.md` (fichiers présents)
- `.claude/dcbp/TASKS.md` (index)

Le numéro est le max existant + 1 pour le namespace concerné.
Si aucune tâche n'existe : commencer à 001.

## Résultat attendu

La tâche est en statut `READY` et prête pour `/dev <ID>`.
