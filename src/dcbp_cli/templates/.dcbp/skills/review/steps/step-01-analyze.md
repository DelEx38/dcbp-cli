---
name: step-01-analyze
description: Analyser chaque fichier selon les critères définis
prev_step: steps/step-00-init.md
next_step: steps/step-02-report.md
---

# Step 1: Analyze

## Règles

- 🛑 TOUJOURS lire chaque fichier complètement
- 🛑 TOUJOURS classer par sévérité
- ✅ Si save_mode : sauvegarder dans `01-analyze.md`
- ✅ Si auto_mode : passer directement au rapport

## Séquence

### Pour chaque fichier dans {files_to_review}

#### 1. Lire le fichier

- Comprendre le but du code
- Identifier les fonctions/classes principales
- Noter la structure générale

#### 2. Vérifier la qualité

| Point | Questions |
|-------|-----------|
| Nommage | Variables/fonctions claires et cohérentes ? |
| Lisibilité | Code facile à comprendre ? |
| Structure | Fonctions courtes et focalisées ? |
| Documentation | Commentaires utiles (pas évidents) ? |
| DRY | Code dupliqué évitable ? |

#### 3. Chercher les bugs potentiels

| Point | Questions |
|-------|-----------|
| Edge cases | Cas limites gérés (null, vide, 0) ? |
| Erreurs | Try/catch appropriés ? |
| Ressources | Fichiers/connexions fermés ? |
| Async | Conditions de course possibles ? |
| Types | Conversions sûres ? |

#### 4. Vérifier la sécurité

| Point | Questions |
|-------|-----------|
| Injection | SQL, commandes, XSS possibles ? |
| Auth | Authentification/autorisation correcte ? |
| Données | Infos sensibles exposées ? |
| Validation | Entrées utilisateur validées ? |
| Secrets | Credentials en dur ? |

#### 5. Évaluer la performance

| Point | Questions |
|-------|-----------|
| Complexité | O(n²) évitable ? |
| N+1 | Requêtes en boucle ? |
| Mémoire | Gros objets en mémoire ? |
| I/O | Opérations coûteuses dans boucles ? |

#### 6. Vérifier les conventions

- Respect du style défini dans PROJECT.md ?
- Imports organisés correctement ?
- Types/docstrings si requis ?
- Nommage selon les conventions ?

### Classification des observations

| Sévérité | Critères | Action |
|----------|----------|--------|
| **🔴 Critique** | Bug confirmé, faille sécurité | Fix obligatoire |
| **🟠 Majeur** | Mauvaise pratique, dette technique | Fix recommandé |
| **🟡 Mineur** | Style, optimisation possible | Fix optionnel |
| **🔵 Note** | Suggestion, question | À considérer |

### Format d'observation

```markdown
#### [SÉVÉRITÉ] Titre court
- **Fichier:** `fichier.py:123`
- **Code:** `ligne de code concernée`
- **Problème:** Description du problème
- **Suggestion:** Comment corriger
```

### Sauvegarder (si save_mode)

Créer `.claude/dcbp/output/review/{review_id}/01-analyze.md` :

```markdown
# Step 1: Analyze

## Fichiers analysés

### fichier1.py
[Observations pour ce fichier]

### fichier2.py
[Observations pour ce fichier]

## Résumé des observations
| Sévérité | Nombre |
|----------|--------|
| 🔴 Critique | X |
| 🟠 Majeur | X |
| 🟡 Mineur | X |
| 🔵 Note | X |
```

### Transition

**Charger** `step-02-report.md`

## Critères de succès

✅ Chaque fichier lu et analysé
✅ Observations classées par sévérité
✅ Suggestions de correction fournies
✅ Pas de faux positifs évidents
