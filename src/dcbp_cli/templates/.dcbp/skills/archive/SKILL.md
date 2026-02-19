---
name: archive
description: "Archive les anciennes sessions de PROGRESS.md pour économiser des tokens."
argument-hint: "[nombre_sessions_a_garder]"
---

# /archive - Archivage de PROGRESS.md

> Rappel : Faire uniquement ce qui est demandé.

Archive les anciennes sessions pour garder PROGRESS.md léger et économiser des tokens.

## Commande

```
/archive        # Garde les 5 dernières sessions (défaut)
/archive 3      # Garde les 3 dernières sessions
/archive 10     # Garde les 10 dernières sessions
```

## Ce que fait ce skill

1. **Compte** les sessions dans PROGRESS.md
2. **Déplace** les anciennes vers `.dcbp/archive/PROGRESS-{date}.md`
3. **Garde** les N dernières sessions dans PROGRESS.md
4. **Affiche** un résumé (tokens économisés)

## Structure d'archive

```
.dcbp/
├── PROGRESS.md              # Sessions récentes (5 dernières)
└── archive/
    ├── PROGRESS-2026-01.md  # Archive janvier
    ├── PROGRESS-2026-02.md  # Archive février
    └── ...
```

## Workflow (1 Phase)

Ce skill s'exécute en une seule phase.

## Point d'entrée

**PREMIÈRE ACTION :** Charger `steps/step-00-archive.md`
