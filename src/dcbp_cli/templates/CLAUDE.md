# DCBP - DC Blueprint

> Système de mémoire persistante et workflows structurés pour Claude Code.

## Activation

Ce projet utilise **DCBP**. Au début de chaque session :

1. Lis `.dcbp/PROJECT.md` pour le contexte
2. Lis `.dcbp/PROGRESS.md` pour l'historique récent
3. Utilise les skills disponibles selon la tâche

## Skills Disponibles

| Commande | Description |
|----------|-------------|
| `/create [python\|django]` | Créer un nouveau projet Python ou Django |
| `/dev <feature>` | Développement structuré (Analyze → Plan → Execute → Verify) |
| `/debug <bug>` | Investigation et correction de bugs |
| `/review <cible>` | Revue de code |
| `/status` | Vue d'ensemble du projet |

### Flags communs
- `-a` : Mode autonome (pas de confirmations)
- `-s` : Sauvegarde dans `.dcbp/output/`
- `-r <id>` : Reprendre une tâche

## Mémoire Projet

| Fichier | Contenu |
|---------|---------|
| `PROJECT.md` | Stack, conventions, architecture |
| `PROGRESS.md` | Journal des sessions |
| `TASKS.md` | Backlog et TODO |
| `ISSUES.md` | Bugs et dette technique |
| `DECISIONS.md` | Décisions architecturales |

## Règles

1. **Toujours mettre à jour la mémoire** après chaque session
2. **Suivre les workflows** définis dans les skills
3. **Documenter les décisions** importantes dans DECISIONS.md
4. **Respecter les conventions** définies dans PROJECT.md
5. **Ne pas ajouter "Co-Authored-By"** dans les messages de commit
