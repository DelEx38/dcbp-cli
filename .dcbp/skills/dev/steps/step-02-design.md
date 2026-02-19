---
name: step-02-design
description: Planification stratégique - créer le plan d'implémentation
prev_step: steps/step-01-context.md
next_step: steps/step-03-implement.md
---

# Step 2: Design (Planification)

## Règles

- 🛑 JAMAIS implémenter (c'est step-03)
- 🛑 JAMAIS écrire ou modifier du code
- ✅ Structurer le plan par FICHIER, pas par feature
- ✅ Inclure les numéros de ligne de l'analyse
- ✅ Mapper les critères d'acceptation aux changements
- 📋 TU ES UN ARCHITECTE, pas un développeur

## Séquence

### 1. Réflexion approfondie

**Avant d'écrire le plan, PENSER :**
- Parcourir mentalement l'implémentation
- Identifier TOUS les fichiers à modifier
- Déterminer l'ordre logique (dépendances d'abord)
- Considérer les edge cases
- Planifier la couverture de tests

### 2. Clarifier les ambiguïtés

**Si `{auto_mode}` = true :**
→ Utiliser l'option recommandée

**Si `{auto_mode}` = false ET plusieurs approches valides :**

```yaml
questions:
  - header: "Approche"
    question: "Plusieurs approches possibles. Laquelle utiliser ?"
    options:
      - label: "Approche A (Recommandée)"
        description: "Description et compromis"
      - label: "Approche B"
        description: "Description et compromis"
```

### 3. Créer le plan détaillé

**Structure par FICHIER :**

```markdown
## Plan d'implémentation: {task_description}

### Vue d'ensemble
[1-2 phrases: stratégie et approche]

### Prérequis
- [ ] Prérequis 1 (si nécessaire)
- [ ] Prérequis 2

---

### Modifications de fichiers

#### `src/path/file1.py`
- Ajouter fonction `do_something` qui gère X
- Suivre le pattern de `similar_file.py:45`
- Gérer le cas d'erreur: [scénario spécifique]

#### `src/path/file2.py`
- Mettre à jour les imports
- Appeler `do_something` dans le flow existant (ligne ~42)
- Ajouter type `NewType`

#### `src/path/file3.py` (NOUVEAU)
- Créer utilitaire pour Z
- Exporter: `utility_function`, `HelperType`
- Pattern: suivre `similar_util.py`

---

### Stratégie de tests

**Nouveaux tests:**
- `tests/test_file1.py` - Tester do_something avec:
  - Cas nominal
  - Cas d'erreur
  - Edge case

**Mettre à jour:**
- `tests/test_existing.py` - Ajouter test pour nouveau flow

---

### Mapping Critères d'Acceptation
- [ ] AC1: Satisfait par `file1.py`
- [ ] AC2: Satisfait par `file2.py`

---

### Risques et considérations
- Risque 1: [problème potentiel et mitigation]
```

### 4. Vérifier la complétude

Checklist :
- [ ] Tous les fichiers identifiés
- [ ] Ordre logique (dépendances d'abord)
- [ ] Actions claires et spécifiques
- [ ] Stratégie de tests définie
- [ ] Pas de scope creep
- [ ] Tous les AC mappés

### 5. Demander approbation

**Si `{auto_mode}` = true :**
→ Passer directement à l'implémentation

**Si `{auto_mode}` = false :**

```yaml
questions:
  - header: "Plan"
    question: "Plan prêt. Procéder ?"
    options:
      - label: "Approuver et implémenter (Recommandé)"
        description: "Le plan est bon, commencer"
      - label: "Ajuster le plan"
        description: "Je veux modifier certaines parties"
      - label: "Questions"
        description: "J'ai des questions sur le plan"
```

### 6. Sauvegarder et transition

Si `{save_mode}` = true :
- Sauvegarder le plan complet dans `02-design.md`

**Puis charger** `step-03-implement.md`

## Critères de succès

✅ Plan complet fichier par fichier
✅ Ordre logique des dépendances
✅ Tous les AC mappés
✅ Stratégie de tests définie
✅ Utilisateur a approuvé (ou auto-approuvé)
✅ AUCUN code écrit
