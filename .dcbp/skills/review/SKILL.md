---
name: review
description: "Revue de code structurée. Analyse la qualité, les bugs potentiels, la sécurité et les conventions."
argument-hint: "[-a] [-s] <fichier ou dossier>"
---

# /review - Revue de Code

> 🛑 **Rappel** : Faire uniquement ce qui est demandé. Suggérer les améliorations, ne pas les implémenter sans accord.

Workflow pour effectuer une revue de code structurée et complète.

## Commande

```
/review [-a] [-s] <fichier ou dossier>
```

## Flags

| Court | Long | Description |
|-------|------|-------------|
| `-a` | `--auto` | Mode autonome : pas de confirmations |
| `-s` | `--save` | Sauvegarde le rapport dans `.dcbp/output/review/` |
| `-A` | `--no-auto` | Désactive le mode auto |
| `-S` | `--no-save` | Désactive la sauvegarde |

## Workflow (3 Phases)

| Phase | Fichier | Objectif |
|-------|---------|----------|
| 00 | step-00-init.md | Parser flags, identifier scope |
| 01 | step-01-analyze.md | Analyser chaque fichier |
| 02 | step-02-report.md | Générer rapport et mettre à jour mémoire |

## Critères de revue

| Catégorie | Points vérifiés |
|-----------|-----------------|
| Qualité | Lisibilité, nommage, structure |
| Bugs | Erreurs potentielles, edge cases |
| Sécurité | Injections, données sensibles |
| Performance | Complexité, optimisations |
| Conventions | Respect du style projet |

## Variables d'état

| Variable | Description |
|----------|-------------|
| `{review_id}` | Identifiant unique (ex: `REV-01-auth-module`) |
| `{review_target}` | Fichier ou dossier à reviewer |
| `{auto_mode}` | Mode autonome activé |
| `{save_mode}` | Sauvegarde activée |

## Structure de sauvegarde (si -s)

```
.dcbp/output/review/{review_id}/
├── 00-init.md
├── 01-analyze.md
└── 02-report.md
```

## Exemples

```bash
# Review simple
/review src/auth/

# Review avec sauvegarde
/review -s src/services/payment.py

# Review autonome (pas de confirmation)
/review -a -s src/api/
```

## Point d'entrée

**PREMIÈRE ACTION :** Charger `steps/step-00-init.md`
