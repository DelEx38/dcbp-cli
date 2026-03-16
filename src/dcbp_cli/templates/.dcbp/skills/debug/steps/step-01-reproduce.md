---
name: step-01-reproduce
description: Comprendre et reproduire le bug
prev_step: steps/step-00-init.md
next_step: steps/step-02-investigate.md
---

# Step 1: Reproduce

## Règles

- 🛑 TOUJOURS comprendre le comportement attendu vs observé
- 🛑 TOUJOURS documenter les étapes de reproduction
- ✅ Si save_mode : sauvegarder dans `01-reproduce.md`
- ✅ Si auto_mode : passer directement à investigate

## Séquence

### 1. Analyser la description du bug

Questions à répondre :
- Quel est le **comportement attendu** ?
- Quel est le **comportement observé** ?
- Dans quel **contexte** se produit-il ?
- Est-ce **reproductible** systématiquement ?

### 2. Identifier le contexte

- Environnement (dev, prod, CI) ?
- Données spécifiques requises ?
- Actions précédentes nécessaires ?

### 3. Documenter les étapes de reproduction

```markdown
### Étapes de reproduction
1. [Action 1]
2. [Action 2]
3. [Action 3]

### Résultat attendu
[Description]

### Résultat observé
[Description + message d'erreur si applicable]
```

### 4. Localiser le code concerné

- Identifier les fichiers/fonctions impliqués
- Noter les points d'entrée du flux
- Lister les fichiers à investiguer

### 5. Sauvegarder (si save_mode)

Créer `.claude/dcbp/output/debug/{bug_id}/01-reproduce.md` :

```markdown
# Step 1: Reproduce

## Bug
{bug_description}

## Reproduction
### Étapes
1. ...

### Attendu vs Observé
- **Attendu:** ...
- **Observé:** ...

## Fichiers concernés
- `fichier1.py:123` - [raison]
- `fichier2.py:456` - [raison]

## Hypothèses initiales
1. ...
2. ...
```

### 6. Point de confirmation (si !auto_mode)

```
════════════════════════════════════════════
Reproduction documentée

Fichiers à investiguer:
- fichier1.py
- fichier2.py

Continuer l'investigation ? [O/n]
════════════════════════════════════════════
```

Si `auto_mode` = true, continuer directement.

### 7. Transition

**Charger** `step-02-investigate.md`

## Critères de succès

✅ Comportement attendu/observé documenté
✅ Étapes de reproduction claires
✅ Fichiers concernés identifiés
✅ Hypothèses initiales formulées
