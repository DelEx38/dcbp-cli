---
name: start
description: "Initialise une nouvelle session de travail. Charge le contexte complet, affiche l'état du projet et suggère quoi faire."
argument-hint: ""
---

# /start - Initialisation de Session

> Rappel : Faire uniquement ce qui est demandé. Suggérer les améliorations, ne pas les implémenter sans accord.

Lance une nouvelle session de travail avec tout le contexte nécessaire.

## Commande

```
/start
```

## Ce que fait ce skill

1. **Charge le contexte complet** - PROJECT, PROGRESS, TASKS, ISSUES, DECISIONS
2. **Résume la dernière session** - Ce qui a été fait, prochaines étapes
3. **Affiche les tâches actives** - En cours et prioritaires
4. **Liste les issues ouvertes** - Bugs et dette technique
5. **Suggère quoi faire** - Basé sur le contexte et les priorités

## Workflow (1 Phase)

Ce skill s'exécute en une seule phase rapide.

## Point d'entrée

**PREMIÈRE ACTION :** Charger `steps/step-00-start.md`
