---
name: step-03-implement
description: Exécution du plan - implémenter fichier par fichier
prev_step: steps/step-02-design.md
next_step: steps/step-04-verify.md
---

# Step 3: Implémentation

## Règles

- 🛑 JAMAIS dévier du plan approuvé
- 🛑 JAMAIS ajouter de features non planifiées (scope creep)
- 🛑 JAMAIS modifier un fichier sans le lire d'abord
- ✅ Suivre le plan fichier par fichier
- ✅ Marquer les todos complétés immédiatement
- ✅ Lire AVANT d'éditer
- 📋 TU ES UN IMPLÉMENTEUR qui suit un plan

## Séquence

### 1. Créer les todos depuis le plan

Convertir chaque modification de fichier en todos :

```
Plan:
#### `src/auth/handler.py`
- Ajouter fonction `validate_token`
- Gérer erreur: token expiré

Devient:
- [ ] src/auth/handler.py: Ajouter validate_token
- [ ] src/auth/handler.py: Gérer token expiré
```

### 2. Implémenter fichier par fichier

Pour chaque todo :

**2.1 Marquer en cours**
- Un seul todo "in_progress" à la fois

**2.2 Lire avant d'éditer**
```
TOUJOURS lire le fichier avant de modifier :
- Comprendre la structure actuelle
- Trouver les points d'insertion exacts
- Vérifier que les patterns correspondent
```

**2.3 Implémenter**
```
Faire les changements du plan :
- Suivre les patterns de l'analyse (step-01)
- Utiliser les noms exacts du plan
- Gérer les erreurs comme spécifié
- PAS de commentaires sauf si vraiment nécessaires
```

**2.4 Marquer complété immédiatement**
- Après chaque todo, marquer ✓
- Ne pas regrouper les completions

**2.5 Logger (si save_mode)**
```markdown
### ✓ src/auth/handler.py
- Ajouté `validate_token` (lignes 45-78)
- Ajouté gestion token expiré
**Timestamp:** {ISO}
```

### 3. Gérer les blocages

**Si `{auto_mode}` = true :**
→ Prendre une décision raisonnable et continuer

**Si `{auto_mode}` = false :**

```yaml
questions:
  - header: "Blocage"
    question: "Problème rencontré. Comment procéder ?"
    options:
      - label: "Approche alternative (Recommandé)"
        description: "Description de l'alternative"
      - label: "Sauter cette partie"
        description: "Continuer sans ce changement"
      - label: "Discuter"
        description: "Je veux en discuter"
```

### 4. Vérification rapide

Après tous les todos, exécuter les commandes de validation du projet :

```bash
# Depuis PROJECT.md - section Validation
{lint_command}
{typecheck_command}
```

Corriger les erreurs immédiatement.

### 5. Résumé d'implémentation

```
**Implémentation terminée**

**Fichiers modifiés:**
- `src/auth/handler.py` - Ajouté validate_token, gestion erreurs
- `src/api/auth/route.py` - Intégré validation

**Nouveaux fichiers:**
- `src/types/auth.py` - Définitions de types

**Todos:** {X}/{Y} complétés
```

### 6. Transition

**Si `{auto_mode}` = true :**
→ Passer directement à la validation

**Si `{auto_mode}` = false :**

```yaml
questions:
  - header: "Implémentation"
    question: "Implémentation terminée. Valider ?"
    options:
      - label: "Valider (Recommandé)"
        description: "Lancer validation complète"
      - label: "Revoir les changements"
        description: "Je veux voir ce qui a changé"
```

**Puis charger** `step-04-verify.md`

## Critères de succès

✅ Tous les items du plan implémentés
✅ Tous les todos marqués complétés
✅ Pas de scope creep
✅ Fichiers lus avant modification
✅ Lint et typecheck passent
