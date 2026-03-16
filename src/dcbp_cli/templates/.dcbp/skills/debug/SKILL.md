---
name: debug
description: "Investigation et correction de bugs. Workflow structuré pour identifier la cause racine et appliquer un correctif."
argument-hint: "[-a] [-s] [-r <bug-id>] <description du bug>"
---

# /debug - Investigation et Correction de Bugs

> 🛑 **Rappel** : Faire uniquement ce qui est demandé. Suggérer les améliorations, ne pas les implémenter sans accord.

Workflow pour investiguer et corriger un bug de manière méthodique.

## Commande

```
/debug [-a] [-s] [-r <bug-id>] <description du bug>
```

## Flags

| Court | Long | Description |
|-------|------|-------------|
| `-a` | `--auto` | Mode autonome : pas de confirmations |
| `-s` | `--save` | Sauvegarde chaque étape dans `.claude/dcbp/output/debug/` |
| `-r` | `--resume` | Reprend un debug précédent |
| `-A` | `--no-auto` | Désactive le mode auto |
| `-S` | `--no-save` | Désactive la sauvegarde |

## Workflow (4 Phases)

| Phase | Fichier | Objectif |
|-------|---------|----------|
| 00 | step-00-init.md | Parser flags, charger contexte |
| 01 | step-01-reproduce.md | Comprendre et reproduire le bug |
| 02 | step-02-investigate.md | Identifier la cause racine |
| 03 | step-03-fix.md | Implémenter et vérifier le correctif |

## Variables d'état

| Variable | Description |
|----------|-------------|
| `{bug_id}` | Identifiant unique (ex: `BUG-01-login-401`) |
| `{bug_description}` | Description du bug |
| `{auto_mode}` | Mode autonome activé |
| `{save_mode}` | Sauvegarde activée |

## Structure de sauvegarde (si -s)

```
.claude/dcbp/output/debug/{bug_id}/
├── 00-init.md
├── 01-reproduce.md
├── 02-investigate.md
└── 03-fix.md
```

## Exemples

```bash
# Debug simple
/debug le login retourne 401

# Debug autonome avec sauvegarde
/debug -a -s les tests échouent sur CI

# Reprendre un debug
/debug -r BUG-01-login-401
```

## Point d'entrée

**PREMIÈRE ACTION :** Charger `steps/step-00-init.md`
