---
name: step-02-report
description: Générer le rapport final et mettre à jour la mémoire
prev_step: steps/step-01-analyze.md
next_step: null
---

# Step 2: Report & Complete

## Règles

- 🛑 TOUJOURS générer un rapport structuré
- 🛑 TOUJOURS mettre à jour la mémoire si critiques/majeurs
- ✅ Si save_mode : sauvegarder dans `02-report.md`
- ✅ Score objectif basé sur les observations

## Séquence

### 1. Consolider les observations

Regrouper toutes les observations par sévérité :

```markdown
## Toutes les observations

### 🔴 Critiques (X)
[Liste]

### 🟠 Majeures (X)
[Liste]

### 🟡 Mineures (X)
[Liste]

### 🔵 Notes (X)
[Liste]
```

### 2. Calculer le score

| Score | Critères |
|-------|----------|
| ⭐⭐⭐⭐⭐ 5/5 | Aucune critique ni majeure |
| ⭐⭐⭐⭐ 4/5 | Mineures uniquement |
| ⭐⭐⭐ 3/5 | 1-2 majeures, pas de critique |
| ⭐⭐ 2/5 | 3+ majeures ou 1 critique |
| ⭐ 1/5 | Plusieurs critiques |

### 3. Mettre à jour ISSUES.md (si critiques/majeurs)

Pour chaque observation critique ou majeure :

```markdown
### REV-{review_id}-{N} : {Titre}
- **Sévérité:** Critique/Majeure
- **Fichier:** `fichier.py:123`
- **Problème:** {description}
- **Suggestion:** {correction}
- **Statut:** Ouvert
```

### 4. Mettre à jour PROGRESS.md

```markdown
## [{date}] Review: {review_target}

### Ce qui a été fait
- [x] Review de {N} fichier(s)
- [x] {X} critique(s), {Y} majeure(s), {Z} mineure(s)
- [x] Score: {score}/5

### Observations clés
- {observation 1}
- {observation 2}

### Actions requises
- [ ] {action 1}
- [ ] {action 2}
```

### 5. Générer le rapport final

```markdown
════════════════════════════════════════════════════════════
/review: {review_target}
════════════════════════════════════════════════════════════

## Scope
- **Fichiers:** {N} fichier(s)
- **Critères:** qualité, bugs, sécurité, perf, conventions

## Score: {score}/5 {étoiles}

## Résumé

| Sévérité | Nombre |
|----------|--------|
| 🔴 Critique | {X} |
| 🟠 Majeur | {Y} |
| 🟡 Mineur | {Z} |
| 🔵 Note | {W} |

## Observations critiques
{Liste ou "Aucune ✓"}

## Observations majeures
{Liste ou "Aucune ✓"}

## Observations mineures
{Liste résumée}

## Notes
{Liste résumée}

## Actions requises
1. {Action prioritaire 1}
2. {Action prioritaire 2}

────────────────────────────────────────────────────────────
Mémoire mise à jour: ISSUES.md ✓ | PROGRESS.md ✓
Tip: /debug <issue> pour corriger les critiques
════════════════════════════════════════════════════════════
```

### 6. Sauvegarder (si save_mode)

Créer `.claude/dcbp/output/review/{review_id}/02-report.md` avec le rapport complet.

### 7. Point de confirmation (si !auto_mode)

Si observations critiques et pas en mode auto :

```
════════════════════════════════════════════
⚠️  {X} observation(s) critique(s) trouvée(s)

Voulez-vous procéder à la correction maintenant ?
[O] Oui, lancer /debug
[n] Non, terminer la review
════════════════════════════════════════════
```

## Fin du workflow

Le skill /review est terminé.

## Critères de succès

✅ Rapport structuré généré
✅ Score calculé objectivement
✅ ISSUES.md mis à jour (si critiques/majeurs)
✅ PROGRESS.md mis à jour
✅ Actions claires identifiées
