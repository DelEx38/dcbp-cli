# DCBP - DC Blueprint

> Système de mémoire persistante et workflows structurés pour Claude Code.

## Workflow de Session (TOUJOURS SUIVRE)

### 🟢 Début de session

1. **Utiliser `/start`** pour initialiser la session (ou lire manuellement le contexte)
2. **Comprendre la demande** avant d'agir

### 🟡 Pendant la session

3. **Appliquer la règle de focus** (voir ci-dessous)
4. **Utiliser les skills** si approprié (`/dev`, `/bugfix`, `/review`, `/etat`)
5. **Documenter les décisions importantes** dans `DECISIONS.md`

### 🔴 Fin de session

6. **Mettre à jour `STATE.md`** :
   ```markdown
   | Phase        | {phase courante}        |
   | Statut       | {En cours / Terminé}    |
   | Branche      | {branche git}           |
   | Tâche active | {DEV-XXX ou Aucune}     |
   | Blockers     | {Aucun / description}   |

   ## Dernière action complétée
   {description de ce qui vient d'être fait}

   ## Prochaine action
   {prochaine étape concrète}
   ```

7. **Checklist de fin de session** :
   - [ ] `TASKS.md` → Tâches complétées ou créées ?
   - [ ] `DECISIONS.md` → Décisions architecturales prises ?
   - [ ] `ISSUES.md` → Bugs découverts ou dette technique identifiée ?

## Skills Disponibles

| Commande | Description |
|----------|-------------|
| `/start` | Initialiser une session (contexte + tâches + suggestions) |
| `/dev <feature>` | Développement structuré (Analyze → Plan → Execute → Verify) |
| `/bugfix <bug>` | Investigation et correction de bugs |
| `/review <cible>` | Revue de code |
| `/etat` | Vue d'ensemble du projet DCBP |
| `/archive [n]` | Archiver PROGRESS.md legacy (projets existants uniquement) |

### Flags communs
- `-a` : Mode autonome (pas de confirmations)
- `-r <id>` : Reprendre une tâche

## Mémoire Projet (dans `.claude/dcbp/`)

| Fichier | Contenu |
|---------|---------|
| `PROJECT.md` | Stack, technologies, architecture, fonctionnalités, règles |
| `STATE.md` | État courant compact du projet |
| `TASKS.md` | Index du travail |
| `tasks/DEV-XXX.md` | Contexte et contrat d'une tâche active |
| `ISSUES.md` | Problèmes ouverts |
| `DECISIONS.md` | Décisions durables et leur justification |
| Git | Historique technique |

## Règles

### Règle fondamentale : Focus sur la tâche

🛑 **FAIRE uniquement ce qui est demandé** - Pas d'initiatives non sollicitées.

| Action | Autorisé |
|--------|----------|
| Exécuter la tâche demandée | ✅ Obligatoire |
| Faire des actions non demandées | ❌ Interdit |
| Suggérer des améliorations | ✅ Autorisé (sans les implémenter) |

**Exemple :**
```
Demande : "Corrige le bug dans auth.py"

✅ Correct :
   1. Corriger le bug
   2. Suggérer : "Je remarque que X pourrait être amélioré.
      Voulez-vous que je le fasse ?"

❌ Incorrect :
   1. Corriger le bug
   2. Refactorer le code (non demandé)
   3. Ajouter des tests (non demandé)
```

### Autres règles

1. **Toujours mettre à jour la mémoire** après chaque session
2. **Suivre les workflows** définis dans les skills
3. **Documenter les décisions** importantes dans DECISIONS.md
4. **Respecter les conventions** définies dans PROJECT.md
5. **Ne pas ajouter "Co-Authored-By"** dans les messages de commit
