---
name: review
tool: dcbp
description: "Valide une tâche VERIFYING. Propriétaire de VERIFYING → DONE."
argument-hint: "<DEV-XXX | fichier>"
allowed-tools: Read, Glob, Grep, Edit, Write
---

# /review — Validation et Clôture de Tâche

Examine une tâche en `VERIFYING` et décide : `DONE` ou retour en `IMPLEMENTING`.

## Usage

```
/review <DEV-XXX>          # Valider une tâche VERIFYING
/review <fichier>          # Revue de code ad-hoc (sans workflow)
```

## Workflow (mode tâche)

### Phase 1: Scope

1. Lire `.claude/dcbp/tasks/<ID>.md` — contrat, critères d'acceptation
2. Vérifier que le statut est `VERIFYING`
3. Lire PROJECT.md pour les règles et conventions

### Phase 2: Examine

Selon la tâche, examiner :

- Critères d'acceptation (de la tâche)
- Diff des fichiers modifiés
- Tests (passants ?)
- Architecture / règles PROJECT.md
- Issues connues pertinentes (ISSUES.md)
- Décisions en vigueur (DECISIONS.md)

### Phase 3: Décision

**Validation réussie** → `VERIFYING → DONE`
- Mettre le statut à `DONE` dans le fichier de tâche et TASKS.md
- Mettre STATE.md à jour
- Présenter le rapport de validation

**Correction nécessaire** → `VERIFYING → IMPLEMENTING`
- Documenter les problèmes trouvés
- Mettre le statut à `IMPLEMENTING`
- Présenter ce qui doit être corrigé avant resoumission

### Important

`DONE` ne signifie pas `PUSH_ALLOWED`.  
Une tâche DONE est validée techniquement. L'autorisation de push reste une décision humaine explicite.

## Classification des problèmes

| Sévérité | Action |
|----------|--------|
| Critique | Retour IMPLEMENTING obligatoire |
| Majeur   | Retour IMPLEMENTING recommandé |
| Mineur   | DONE avec note de suivi |
| Suggestion | DONE, suggestion documentée |

## Mode revue ad-hoc (sans workflow)

Sans identifiant de tâche :
1. Identifier les fichiers à reviewer
2. Analyser qualité, bugs, conventions
3. Générer rapport (sévérité + score)
4. Mettre à jour ISSUES.md si problèmes critiques
5. Mettre à jour STATE.md si impact courant
