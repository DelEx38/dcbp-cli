---
name: step-00-init
description: Initialise le workflow debug - parse flags, charge contexte
next_step: steps/step-01-reproduce.md
---

# Step 0: Initialisation

## Règles

- 🛑 TOUJOURS parser les flags en premier
- 🛑 TOUJOURS charger le contexte projet
- ✅ Output compact (une table, pas de logs verbeux)
- ✅ Procéder immédiatement après l'init

## Séquence

### 1. Parser les flags

```
Défauts:
  auto_mode = false
  save_mode = false
  resume_bug = null

Flags enable (minuscule):
  -a, --auto    → auto_mode = true
  -s, --save    → save_mode = true
  -r, --resume  → resume_bug = <argument suivant>

Flags disable (MAJUSCULE):
  -A, --no-auto → auto_mode = false
  -S, --no-save → save_mode = false

Reste → {bug_description}
```

### 2. Générer identifiants

```
{bug_name} = kebab-case de la description (max 30 chars)
  Ex: "le login retourne 401" → "login-401"

{bug_id} = BUG-NN-{bug_name}
  Ex: "BUG-01-login-401"
  (NN = prochain numéro disponible dans .dcbp/output/debug/)
```

### 3. Mode Resume (si -r)

Si `{resume_bug}` est défini :
1. Chercher le dossier dans `.dcbp/output/debug/`
2. Lire `00-init.md` pour restaurer les variables
3. Trouver la dernière étape complétée
4. Charger l'étape suivante
5. **STOP** - ne pas continuer l'init

### 4. Charger contexte projet

**OBLIGATOIRE :** Lire ces fichiers :
- `.dcbp/PROJECT.md` - Stack, architecture
- `.dcbp/ISSUES.md` - Bugs connus (vérifier si déjà documenté)

Extraire :
- Stack technique
- Commandes de test
- Bugs similaires déjà résolus

### 5. Créer output (si save_mode)

Si `{save_mode}` = true :

```bash
mkdir -p .dcbp/output/debug/{bug_id}
```

Créer `00-init.md` :
```markdown
# DCBP Debug: {bug_id}

**Créé:** {timestamp}
**Bug:** {bug_description}

## Configuration
| Flag | Valeur |
|------|--------|
| auto_mode | {value} |
| save_mode | {value} |

## Contexte
- Stack: [extrait de PROJECT.md]
- Bugs similaires: [depuis ISSUES.md]
```

### 6. Afficher résumé et continuer

```
✓ DCBP Debug: {bug_description}

| Variable | Valeur |
|----------|--------|
| {bug_id} | BUG-01-xxx |
| {auto_mode} | true/false |
| {save_mode} | true/false |

→ Reproduction du bug...
```

**Puis charger immédiatement** `step-01-reproduce.md`

## Critères de succès

✅ Flags correctement parsés
✅ Contexte projet chargé
✅ Output compact (une table)
✅ Procédé directement à step-01
