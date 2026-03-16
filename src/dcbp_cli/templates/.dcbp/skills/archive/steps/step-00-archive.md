# Step 00 - Archive PROGRESS.md

## Objectif

Archiver les anciennes sessions pour économiser des tokens.

## Instructions

### 1. Parser les arguments

```
/archive      → garder = 5 (défaut)
/archive N    → garder = N
```

### 2. Lire PROGRESS.md

- Identifier chaque session par le pattern `## [YYYY-MM-DD]`
- Compter le nombre total de sessions
- Si sessions ≤ garder → rien à archiver, terminer

### 3. Séparer les sessions

```
Sessions totales : [1, 2, 3, 4, 5, 6, 7, 8]
                   |___ à archiver ___|  |_ à garder _|
```

- **À garder** : les N dernières (plus récentes, en haut du fichier)
- **À archiver** : toutes les autres (plus anciennes)

### 4. Créer/mettre à jour l'archive

Fichier : `.claude/dcbp/archive/PROGRESS-{YYYY-MM}.md`

```markdown
# PROGRESS - Archive {Mois YYYY}

> Sessions archivées depuis PROGRESS.md

---

## [2026-02-01] Session archivée 1
...

## [2026-02-05] Session archivée 2
...
```

**Règles** :
- Grouper par mois (YYYY-MM)
- Si le fichier d'archive existe, ajouter les sessions au début (après le header)
- Conserver l'ordre chronologique inverse (plus récent en haut)

### 5. Mettre à jour PROGRESS.md

Garder uniquement :
- Le header (titre + description)
- Les N dernières sessions

```markdown
# PROGRESS - Journal des sessions

> Historique des sessions de travail sur {Projet}.

---

## [2026-02-19] Session récente 1
...

## [2026-02-18] Session récente 2
...
```

### 6. Afficher le résumé

```markdown
╔════════════════════════════════════════════════════════════╗
║  ARCHIVAGE TERMINÉ                                         ║
╚════════════════════════════════════════════════════════════╝

Sessions avant  : X
Sessions après  : Y (gardées)
Sessions archivées : Z

Fichiers modifiés :
- .claude/dcbp/PROGRESS.md (réduit)
- .claude/dcbp/archive/PROGRESS-2026-02.md (créé/mis à jour)

Estimation tokens économisés : ~{estimation}

───────────────────────────────────────────────────────────────
Conseil : Lancez /archive quand PROGRESS.md dépasse 10 KB
╚═════════════════════════════════════════════════════════════╝
```

### 7. Calcul estimation tokens

```
Tokens économisés ≈ (taille archivée en bytes) / 3.5
```

## Notes

- Ne jamais supprimer de sessions, toujours archiver
- Le dossier `.claude/dcbp/archive/` est créé automatiquement si nécessaire
- Les archives peuvent être consultées mais ne sont pas chargées par `/start`

## Fin du workflow

Le skill /archive est terminé.
