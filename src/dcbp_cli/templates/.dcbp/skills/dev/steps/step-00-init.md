---
name: step-00-init
description: Initialise le workflow - parse flags, charge contexte projet
next_step: steps/step-01-context.md
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
  test_mode = false
  resume_task = null

Flags enable (minuscule):
  -a, --auto    → auto_mode = true
  -s, --save    → save_mode = true
  -t, --test    → test_mode = true
  -r, --resume  → resume_task = <argument suivant>

Flags disable (MAJUSCULE):
  -A, --no-auto → auto_mode = false
  -S, --no-save → save_mode = false
  -T, --no-test → test_mode = false

Reste → {task_description}
```

### 2. Générer identifiants

```
{feature_name} = kebab-case de la description
  Ex: "ajouter authentification" → "ajouter-authentification"

{task_id} = NN-{feature_name}
  Ex: "01-ajouter-authentification"
  (NN = prochain numéro disponible dans .claude/dcbp/output/dev/)
```

### 3. Mode Resume (si -r)

Si `{resume_task}` est défini :
1. Chercher le dossier dans `.claude/dcbp/output/dev/`
2. Lire `00-init.md` pour restaurer les variables
3. Trouver la dernière étape complétée
4. Charger l'étape suivante
5. **STOP** - ne pas continuer l'init

### 4. Charger contexte projet

**OBLIGATOIRE :** Lire ces fichiers avant de continuer :
- `.claude/dcbp/PROJECT.md` - Stack, conventions, architecture
- `.claude/dcbp/PROGRESS.md` - Sessions récentes (dernières 2-3)

Extraire :
- Stack technique
- Commandes de validation
- Conventions de code
- Points d'attention

### 5. Créer output (si save_mode)

Si `{save_mode}` = true :

```bash
mkdir -p .claude/dcbp/output/dev/{task_id}
```

Créer `00-init.md` :
```markdown
# DCBP Dev: {task_id}

**Créé:** {timestamp}
**Tâche:** {task_description}

## Configuration
| Flag | Valeur |
|------|--------|
| auto_mode | {value} |
| save_mode | {value} |
| test_mode | {value} |

## Contexte projet
- Stack: [extrait de PROJECT.md]
- Validation: [commandes]
```

### 6. Afficher résumé et continuer

```
✓ DCBP Dev: {task_description}

| Variable | Valeur |
|----------|--------|
| {task_id} | 01-feature-name |
| {auto_mode} | true/false |
| {save_mode} | true/false |
| {test_mode} | true/false |

→ Analyse du contexte...
```

**Puis charger immédiatement** `step-01-context.md`

## Critères de succès

✅ Flags correctement parsés
✅ Contexte projet chargé
✅ Output compact (une table)
✅ Procédé directement à step-01
