---
name: step-03-fix
description: Implémenter le correctif et mettre à jour la mémoire
prev_step: steps/step-02-investigate.md
next_step: null
---

# Step 3: Fix & Complete

## Règles

- 🛑 TOUJOURS respecter les conventions du projet
- 🛑 TOUJOURS mettre à jour la mémoire DCBP
- ✅ Correctif minimal (pas de refactoring non demandé)
- ✅ Si save_mode : sauvegarder dans `03-fix.md`

## Séquence

### 1. Planifier le correctif

```markdown
### Plan de correction
- **Fichier:** `fichier.py`
- **Modification:** [description]
- **Impact:** [fichiers/fonctions affectés]
- **Risque de régression:** faible/moyen/élevé
```

### 2. Implémenter le correctif

- Appliquer la modification minimale nécessaire
- Respecter les conventions de PROJECT.md
- Ne PAS refactorer au-delà du nécessaire
- Ajouter un commentaire si le fix n'est pas évident

### 3. Vérifier le correctif

- Confirmer que le bug est résolu
- Vérifier l'absence de régression
- Exécuter les tests si disponibles :

```bash
# Commandes depuis PROJECT.md
{commande_test}
```

### 4. Mettre à jour ISSUES.md

Ajouter ou mettre à jour l'entrée :

```markdown
### {bug_id} : {bug_description} ✅ Résolu

- **Date:** {date}
- **Cause:** {cause racine}
- **Fix:** {description du correctif}
- **Fichiers:** {liste}
```

### 5. Mettre à jour PROGRESS.md

Ajouter une entrée :

```markdown
## [{date}] Debug: {bug_description}

### Ce qui a été fait
- [x] Bug reproduit et documenté
- [x] Cause identifiée : {cause}
- [x] Correctif appliqué : {fix}
- [x] Tests passés

### Fichiers modifiés
- `fichier.py` - {description}
```

### 6. Sauvegarder (si save_mode)

Créer `.claude/dcbp/output/debug/{bug_id}/03-fix.md` :

```markdown
# Step 3: Fix

## Correctif appliqué
**Fichier:** ...
**Avant:**
\`\`\`
[code avant]
\`\`\`

**Après:**
\`\`\`
[code après]
\`\`\`

## Vérification
- [ ] Bug résolu
- [ ] Tests passés
- [ ] Pas de régression

## Mémoire mise à jour
- [x] ISSUES.md
- [x] PROGRESS.md
```

### 7. Résumé final

```
════════════════════════════════════════════════════
✓ Bug corrigé : {bug_id}
════════════════════════════════════════════════════

Cause : {cause racine}
Fix   : {description courte}

Fichiers modifiés:
- fichier.py

Mémoire mise à jour:
- ISSUES.md ✓
- PROGRESS.md ✓

────────────────────────────────────────────────────
Tip: /status pour voir l'état du projet
════════════════════════════════════════════════════
```

## Fin du workflow

Le skill /debug est terminé.

## Critères de succès

✅ Correctif minimal appliqué
✅ Bug résolu confirmé
✅ Tests passés (si disponibles)
✅ ISSUES.md mis à jour
✅ PROGRESS.md mis à jour
