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

6. **Mettre à jour la mémoire** :
   ```markdown
   ## [{date}] {Titre court de la session}

   ### Ce qui a été fait
   - [x] Action 1
   - [x] Action 2

   ### Fichiers modifiés
   - `fichier1.py` - {description}

   ### Suggestions non implémentées
   - {suggestion 1}

   → **Prochaines étapes** : {next steps}
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
| `/archive [n]` | Archiver PROGRESS.md (garde n sessions, défaut: 5) |

### Flags communs
- `-a` : Mode autonome (pas de confirmations)
- `-s` : Sauvegarde dans `.claude/dcbp/output/`
- `-r <id>` : Reprendre une tâche

## Mémoire Projet (dans `.claude/dcbp/`)

| Fichier | Contenu |
|---------|---------|
| `PROJECT.md` | Stack, conventions, architecture |
| `PROGRESS.md` | Journal des sessions |
| `TASKS.md` | Backlog et TODO |
| `ISSUES.md` | Bugs et dette technique |
| `DECISIONS.md` | Décisions architecturales |

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
