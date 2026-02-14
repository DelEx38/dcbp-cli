---
name: dev
description: "Workflow de développement structuré DCBP. 7 phases : Init → Context → Design → Implement → Verify → Review → Complete. Utilise /dev <description> pour développer une fonctionnalité de manière méthodique."
argument-hint: "[-a] [-s] [-r <task-id>] <description de la feature>"
---

# /dev - Workflow de Développement DCBP

> 🛑 **Rappel** : Faire uniquement ce qui est demandé. Suggérer les améliorations, ne pas les implémenter sans accord.

Workflow structuré pour implémenter des fonctionnalités de manière méthodique avec mémoire persistante.

## Commande

```
/dev [-a] [-s] [-t] [-r <task-id>] <description>
```

## Flags

| Flag | Long | Description |
|------|------|-------------|
| `-a` | `--auto` | Mode autonome : pas de confirmations |
| `-s` | `--save` | Sauvegarde chaque étape dans `.dcbp/output/dev/` |
| `-t` | `--test` | Inclut création et exécution des tests |
| `-r` | `--resume` | Reprend une tâche précédente |
| `-A` | `--no-auto` | Désactive le mode auto |
| `-S` | `--no-save` | Désactive la sauvegarde |

## Workflow (7 Phases)

| Phase | Nom | Objectif |
|-------|-----|----------|
| 00 | Init | Parse flags, charge contexte projet |
| 01 | Context | Explore le codebase, identifie patterns |
| 02 | Design | Crée le plan d'implémentation |
| 03 | Implement | Exécute le plan fichier par fichier |
| 04 | Verify | Valide (lint, types, tests) |
| 05 | Review | Revue critique du code produit |
| 06 | Complete | Met à jour la mémoire, résumé final |

## Variables d'état

| Variable | Description |
|----------|-------------|
| `{task_description}` | Description de la feature |
| `{task_id}` | Identifiant unique (ex: `01-add-auth`) |
| `{auto_mode}` | Skip les confirmations |
| `{save_mode}` | Sauvegarde les outputs |
| `{test_mode}` | Inclut les tests |
| `{output_dir}` | Chemin vers `.dcbp/output/dev/{task_id}/` |

## Output Structure (si save_mode)

```
.dcbp/output/dev/{task_id}/
├── 00-init.md
├── 01-context.md
├── 02-design.md
├── 03-implement.md
├── 04-verify.md
├── 05-review.md
├── 06-complete.md
└── summary.md
```

## Intégration Mémoire

Ce workflow :
1. **Lit** PROJECT.md et PROGRESS.md au démarrage
2. **Met à jour** PROGRESS.md à la fin
3. **Ajoute** les décisions importantes à DECISIONS.md
4. **Signale** les problèmes dans ISSUES.md

## Exemples

```bash
# Développement simple
/dev ajouter un bouton de déconnexion

# Mode autonome avec sauvegarde
/dev -a -s implémenter la pagination

# Avec tests
/dev -t ajouter validation email

# Reprendre une tâche
/dev -r 03-pagination
```

## Point d'entrée

**PREMIÈRE ACTION :** Charger `steps/step-00-init.md`
