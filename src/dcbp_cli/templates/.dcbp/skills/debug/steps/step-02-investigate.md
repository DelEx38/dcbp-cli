---
name: step-02-investigate
description: Identifier la cause racine du bug
prev_step: steps/step-01-reproduce.md
next_step: steps/step-03-fix.md
---

# Step 2: Investigate

## Règles

- 🛑 TOUJOURS lire le code avant de conclure
- 🛑 TOUJOURS valider la cause racine
- ✅ Si save_mode : sauvegarder dans `02-investigate.md`
- ✅ Si auto_mode : passer directement au fix

## Séquence

### 1. Lire le code concerné

Pour chaque fichier identifié :
- Lire et comprendre le flux d'exécution
- Identifier les dépendances
- Noter les comportements suspects

### 2. Tracer le flux d'exécution

```markdown
### Flux d'exécution
1. Entrée: [fonction/endpoint]
2. → Appel: [fonction2]
3. → Traitement: [description]
4. → ⚠️ PROBLÈME ICI: [description]
5. → Sortie: [résultat incorrect]
```

### 3. Formuler des hypothèses

Lister les causes possibles par ordre de probabilité :

```markdown
### Hypothèses
1. **[Hypothèse 1]** (probabilité: haute)
   - Indice: ...
   - Vérification: ...

2. **[Hypothèse 2]** (probabilité: moyenne)
   - Indice: ...
   - Vérification: ...
```

### 4. Valider la cause racine

- Confirmer l'hypothèse la plus probable
- Expliquer **pourquoi** le bug se produit
- Identifier la ligne/bloc de code responsable

```markdown
### Cause racine confirmée
**Fichier:** `fichier.py:123`
**Code problématique:**
\`\`\`python
# Code qui cause le bug
\`\`\`

**Explication:**
[Pourquoi ce code cause le bug]
```

### 5. Sauvegarder (si save_mode)

Créer `.claude/dcbp/output/debug/{bug_id}/02-investigate.md` :

```markdown
# Step 2: Investigate

## Fichiers analysés
- `fichier1.py` - [résumé]
- `fichier2.py` - [résumé]

## Flux d'exécution
[Trace du flux]

## Hypothèses testées
1. ❌ [Hypothèse rejetée] - [raison]
2. ✅ [Hypothèse confirmée]

## Cause racine
**Fichier:** ...
**Ligne:** ...
**Explication:** ...
```

### 6. Point de confirmation (si !auto_mode)

```
════════════════════════════════════════════
Cause racine identifiée

Fichier: fichier.py:123
Cause: [description courte]

Approuver et procéder au fix ? [O/n]
════════════════════════════════════════════
```

Si `auto_mode` = true, continuer directement.

### 7. Transition

**Charger** `step-03-fix.md`

## Critères de succès

✅ Code lu et compris
✅ Flux d'exécution tracé
✅ Cause racine identifiée et expliquée
✅ Fichier et ligne précis identifiés
