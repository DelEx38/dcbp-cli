---
name: step-05-review
description: Revue critique - identifier les problèmes potentiels
prev_step: steps/step-04-verify.md
next_step: steps/step-06-complete.md
---

# Step 5: Revue

## Règles

- ✅ Adopter une posture CRITIQUE
- ✅ Vérifier sécurité, logique, qualité
- ✅ Classifier par sévérité
- 📋 TU ES UN REVIEWER SCEPTIQUE

## Séquence

### 1. Rassembler les changements

Identifier tous les fichiers modifiés/créés dans cette session.

### 2. Checklist de revue

#### Sécurité
- [ ] Pas d'injection (SQL, commandes, XSS)
- [ ] Validation des entrées utilisateur
- [ ] Pas de secrets dans le code
- [ ] Auth/authz vérifiés sur les routes protégées

#### Logique
- [ ] Gestion des erreurs complète
- [ ] Edge cases gérés
- [ ] Vérifications null/undefined
- [ ] Pas de race conditions

#### Qualité
- [ ] Suit les patterns existants
- [ ] Pas de duplication
- [ ] Nommage clair
- [ ] Complexité raisonnable

### 3. Classifier les trouvailles

**Sévérité :**
- 🔴 CRITIQUE : Sécurité, perte de données
- 🟡 IMPORTANT : Bug significatif
- 🟢 SUGGESTION : Amélioration optionnelle

**Validité :**
- **Réel** : À corriger
- **Bruit** : Pas un vrai problème
- **Incertain** : À discuter

### 4. Rapport de revue

```markdown
## Findings

| ID | Sévérité | Catégorie | Fichier | Problème |
|----|----------|-----------|---------|----------|
| F1 | 🔴 | Sécurité | auth.py:42 | Input non validé |
| F2 | 🟡 | Logique | handler.py:78 | Missing null check |
| F3 | 🟢 | Qualité | utils.py:15 | Fonction complexe |

**Résumé:** {count} findings ({blocking} bloquants)
```

### 5. Corriger les problèmes critiques

**Si findings CRITIQUES ou IMPORTANTS :**
1. Corriger immédiatement
2. Re-valider (step-04 rapide)
3. Mettre à jour le rapport

### 6. Décision finale

**Si `{auto_mode}` = true :**
→ Corriger les Réels, ignorer les Suggestions, passer à complete

**Si `{auto_mode}` = false :**

```yaml
questions:
  - header: "Revue"
    question: "Revue terminée. Comment procéder ?"
    options:
      - label: "Finaliser (Recommandé)"
        description: "Passer à la complétion"
      - label: "Corriger suggestions"
        description: "Appliquer aussi les suggestions"
      - label: "Discuter findings"
        description: "Je veux discuter certains points"
```

### 7. Transition

**Charger** `step-06-complete.md`

## Critères de succès

✅ Tous les fichiers revus
✅ Checklist sécurité complétée
✅ Findings classifiés
✅ Problèmes critiques corrigés
✅ Rapport clair
