---
name: step-06-complete
description: Complétion - mise à jour mémoire et résumé final
prev_step: steps/step-05-review.md
---

# Step 6: Complétion

## Règles

- ✅ TOUJOURS mettre à jour PROGRESS.md
- ✅ Ajouter les décisions importantes à DECISIONS.md
- ✅ Signaler les problèmes dans ISSUES.md
- ✅ Fournir un résumé clair
- 📋 TU ES UN DOCUMENTEUR

## Séquence

### 1. Résumé des changements

```markdown
## Résumé: {task_description}

### Fichiers modifiés
| Fichier | Changements |
|---------|-------------|
| `src/auth/handler.py` | +validate_token, +error handling |
| `src/api/route.py` | Intégration validation |

### Fichiers créés
| Fichier | Description |
|---------|-------------|
| `src/types/auth.py` | Types pour authentification |

### Tests
- Ajoutés: 3 nouveaux tests
- Modifiés: 1 test existant
- Couverture: 85%

### Critères d'acceptation
- [x] AC1: ✓
- [x] AC2: ✓
- [x] AC3: ✓
```

### 2. Mettre à jour PROGRESS.md

Ajouter une entrée de session :

```markdown
## Session {date} - {task_description}

### Ce qui a été fait
- [x] Analysé le codebase pour {feature}
- [x] Conçu le plan d'implémentation
- [x] Implémenté dans {N} fichiers
- [x] Validé (lint, types, tests)
- [x] Revue de code effectuée

### Décisions
> **Décision :** {décision importante si applicable}

### Fichiers modifiés
- `file1.py` - {description}
- `file2.py` - {description}

### Prochaines étapes
- [ ] {suggestion 1}
- [ ] {suggestion 2}
```

### 3. Mettre à jour DECISIONS.md (si applicable)

Si une décision architecturale importante a été prise :

```markdown
## DEC-XXX : {titre} ({date})

### Contexte
{pourquoi cette décision}

### Décision
{ce qui a été choisi}

### Justification
- {raison 1}
- {raison 2}
```

### 4. Mettre à jour ISSUES.md (si applicable)

Si des problèmes ont été découverts mais non résolus :

```markdown
### [BUG-XXX] {titre}
- **Sévérité** : 🟡 Majeur
- **Fichier** : `path/to/file.py:42`
- **Description** : {description}
- **Découvert** : {date}
```

### 5. Mettre à jour TASKS.md (si applicable)

- Marquer la tâche comme complétée
- Ajouter de nouvelles tâches découvertes

### 6. Créer summary.md (si save_mode)

```markdown
# Summary: {task_id}

**Terminé:** {timestamp}
**Durée:** ~{estimation}

## Changements
- {count} fichiers modifiés
- {count} fichiers créés
- {count} tests ajoutés

## Points clés
- {point 1}
- {point 2}

## Suivi
- [ ] {action de suivi si nécessaire}
```

### 7. Message final

```
✓ **DCBP Dev Terminé: {task_description}**

**Résumé:**
- {count} fichiers modifiés
- {count} tests passent
- Mémoire projet mise à jour

**Prochaines étapes suggérées:**
- {suggestion 1}
- {suggestion 2}

**Outputs:** `.claude/dcbp/output/dev/{task_id}/`
```

## Critères de succès

✅ PROGRESS.md mis à jour
✅ DECISIONS.md mis à jour (si applicable)
✅ ISSUES.md mis à jour (si applicable)
✅ summary.md créé (si save_mode)
✅ Message final clair avec prochaines étapes
