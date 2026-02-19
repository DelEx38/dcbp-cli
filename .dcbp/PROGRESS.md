# Journal de Progrès

> Historique des sessions de travail. Mis à jour automatiquement par les workflows DCBP.

---

## [2026-02-19] Support natif des skills Claude Code

### Ce qui a été fait
- [x] Ajout du dossier `.claude/skills/` avec format SKILL.md natif
- [x] Installation des skills dans `~/.claude/skills/` (global)
- [x] Création de la commande `dcbp install` pour installation globale
- [x] Renommage `/debug` → `/bugfix` (évite conflit avec commande native)
- [x] Renommage `/status` → `/etat` (évite conflit avec commande native)
- [x] Mise à jour du README avec nouveau workflow d'installation
- [x] Tests des skills `/start` et `/etat`

### Fichiers modifiés
- `src/dcbp_cli/cli.py` - Ajout commande `install`
- `src/dcbp_cli/commands.py` - Fonction `install_skills()` + copie vers ~/.claude/skills/
- `src/dcbp_cli/templates/.claude/skills/` - Nouveaux skills au format natif
- `src/dcbp_cli/templates/CLAUDE.md` - Mise à jour noms des skills
- `README.md` - Documentation complète du nouveau workflow

### Décisions
> **Décision :** Installer les skills dans `~/.claude/skills/` (global) en plus du projet local pour garantir leur disponibilité immédiate. Inspiré par AIBlueprint de Melvynx.

> **Décision :** Renommer `/debug` en `/bugfix` et `/status` en `/etat` car ce sont des commandes natives de Claude Code.

### Problèmes rencontrés
- [Skills non détectés] → Les skills doivent être dans `~/.claude/skills/` et Claude Code doit être redémarré
- [Conflit de noms] → `/debug` et `/status` sont natifs, renommés en `/bugfix` et `/etat`

→ **Prochaines étapes** : Tester sur un vrai projet, améliorer les workflows des skills

---

<!--
## Session YYYY-MM-DD - [Titre]

### Ce qui a été fait
- [x] ...

### Décisions
> **Décision :** ...

### Problèmes rencontrés
- [Problème] → [Solution]

### Prochaines étapes
- [ ] ...
-->
