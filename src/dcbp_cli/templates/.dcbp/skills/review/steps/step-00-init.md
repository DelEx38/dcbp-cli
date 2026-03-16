---
name: step-00-init
description: Initialise le workflow review - parse flags, identifie le scope
next_step: steps/step-01-analyze.md
---

# Step 0: Initialisation

## Règles

- 🛑 TOUJOURS parser les flags en premier
- 🛑 TOUJOURS charger les conventions du projet
- ✅ Output compact (une table)
- ✅ Procéder immédiatement après l'init

## Séquence

### 1. Parser les flags

```
Défauts:
  auto_mode = false
  save_mode = false

Flags enable (minuscule):
  -a, --auto    → auto_mode = true
  -s, --save    → save_mode = true

Flags disable (MAJUSCULE):
  -A, --no-auto → auto_mode = false
  -S, --no-save → save_mode = false

Reste → {review_target}
```

### 2. Identifier le scope

```
Si {review_target} est un fichier:
  {files_to_review} = [fichier]

Si {review_target} est un dossier:
  {files_to_review} = [lister les fichiers de code]

Si {review_target} = "derniers commits":
  {files_to_review} = [fichiers modifiés récemment via git]
```

### 3. Générer identifiants

```
{target_name} = kebab-case du target (max 30 chars)
  Ex: "src/auth/" → "auth"
  Ex: "src/services/payment.py" → "payment"

{review_id} = REV-NN-{target_name}
  Ex: "REV-01-auth"
  (NN = prochain numéro disponible dans .claude/dcbp/output/review/)
```

### 4. Charger contexte projet

**OBLIGATOIRE :** Lire ces fichiers :
- `.claude/dcbp/PROJECT.md` - Conventions, style, architecture

Extraire :
- Style de code attendu
- Conventions de nommage
- Points d'attention spécifiques
- Outils de lint/format utilisés

### 5. Définir les critères

```markdown
### Critères de revue
- [x] Qualité du code (lisibilité, structure)
- [x] Bugs potentiels
- [x] Sécurité
- [x] Performance (si pertinent)
- [x] Conventions du projet
```

### 6. Créer output (si save_mode)

Si `{save_mode}` = true :

```bash
mkdir -p .claude/dcbp/output/review/{review_id}
```

Créer `00-init.md` :
```markdown
# DCBP Review: {review_id}

**Créé:** {timestamp}
**Target:** {review_target}

## Configuration
| Flag | Valeur |
|------|--------|
| auto_mode | {value} |
| save_mode | {value} |

## Scope
| Fichiers | {count} |
| Critères | qualité, bugs, sécurité, perf, conventions |

## Conventions projet
[Extrait de PROJECT.md]
```

### 7. Afficher résumé et continuer

```
✓ DCBP Review: {review_target}

| Variable | Valeur |
|----------|--------|
| {review_id} | REV-01-xxx |
| {files_count} | N fichier(s) |
| {auto_mode} | true/false |
| {save_mode} | true/false |

Fichiers à analyser:
- fichier1.py
- fichier2.py

→ Analyse en cours...
```

**Puis charger immédiatement** `step-01-analyze.md`

## Critères de succès

✅ Flags correctement parsés
✅ Scope identifié (liste de fichiers)
✅ Conventions projet chargées
✅ Procédé directement à step-01
