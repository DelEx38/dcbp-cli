---
name: step-04-verify
description: Validation - vérifier que tout fonctionne
prev_step: steps/step-03-implement.md
next_step: steps/step-05-review.md
---

# Step 4: Vérification

## Règles

- ✅ Exécuter TOUTES les commandes de validation
- ✅ Corriger les erreurs avant de continuer
- ✅ Vérifier les critères d'acceptation
- 📋 TU ES UN TESTEUR, pas un développeur

## Séquence

### 1. Charger les commandes de validation

Depuis `.claude/dcbp/PROJECT.md` section "Validation" :
- `{lint_command}`
- `{typecheck_command}`
- `{test_command}`
- `{build_command}` (optionnel)

### 2. Exécuter la validation

```bash
# Lint
{lint_command}

# Type check (si applicable)
{typecheck_command}

# Tests
{test_command}
```

### 3. Gérer les erreurs

**Pour chaque erreur :**
1. Identifier le fichier et la ligne
2. Comprendre l'erreur
3. Corriger
4. Re-exécuter la validation

**Logger les corrections :**
```markdown
### Corrections
- `file.py:42` - Corrigé import manquant
- `file.py:78` - Ajouté type annotation
```

### 4. Tests (si test_mode)

**Si `{test_mode}` = true :**

1. Identifier les tests existants liés
2. Les exécuter
3. Si échecs : corriger ou créer les tests manquants

```bash
# Tests spécifiques
pytest tests/test_auth.py -v

# Ou tous les tests
pytest
```

### 5. Vérifier les critères d'acceptation

```markdown
## Vérification des Critères

- [x] AC1: [description] ✓ Vérifié par [comment]
- [x] AC2: [description] ✓ Vérifié par [comment]
- [ ] AC3: [description] ⚠️ Non vérifié - [raison]
```

### 6. Rapport de validation

```
**Validation terminée**

### Résultats
| Check | Status |
|-------|--------|
| Lint | ✓ Pass |
| Types | ✓ Pass |
| Tests | ✓ Pass (12/12) |
| Build | ✓ Pass |

### Critères d'acceptation
- [x] AC1: ✓
- [x] AC2: ✓
- [x] AC3: ✓

### Corrections effectuées
- {count} corrections mineures
```

### 7. Transition

**Si tous les checks passent :**

**Si `{auto_mode}` = true :**
→ Passer à la revue

**Si `{auto_mode}` = false :**

```yaml
questions:
  - header: "Validation"
    question: "Validation réussie. Continuer vers la revue ?"
    options:
      - label: "Revue de code (Recommandé)"
        description: "Faire une revue critique du code"
      - label: "Sauter la revue"
        description: "Aller directement à la fin"
```

**Puis charger** `step-05-review.md` ou `step-06-complete.md`

## Critères de succès

✅ Lint passe
✅ Typecheck passe (si applicable)
✅ Tests passent
✅ Tous les AC vérifiés
✅ Aucune erreur en suspens
