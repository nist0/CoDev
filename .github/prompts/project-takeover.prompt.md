---
name: project-takeover
description: "Analyse exhaustive d'un ou plusieurs dépôts GitHub on-prem lors d'une prise en charge d'équipe. Produit une documentation complète en français dans .takeover/ (non commité)."
agent: "Project Takeover"

argument-hint: "repos=<url1,url2,...> kanban=<project-url> [output=.takeover]"
---

Argument handling:

- If arguments are provided, treat them as authoritative.

- If arguments are omitted, infer missing values from the current workspace, active file, and session context.

- If required details still cannot be inferred with high confidence, ask concise clarifying questions before proceeding.

- Do not fail solely because arguments were omitted.

Inputs:

- repos: ${input:repos:URL(s) des dépôts GitHub on-prem, séparés par des virgules}

- kanban: ${input:kanban:URL du projet Kanban GitHub de référence}

- output: ${input:output:.takeover}

Tu es l'agent **Project Takeover**. Lance la skill `project-takeover` en 6 phases
pour analyser les dépôts et produire la documentation complète en français.

## Pré-condition obligatoire

Avant de démarrer la Phase 1, vérifie que `.takeover/` est dans `.gitignore`.
Si absent, demande confirmation avant de l'ajouter automatiquement.

## Séquence d'exécution

| Phase | Livrable | Dépendances |
|---|---|---|
| 1 -- Inventaire des dépôts | `.takeover/00-inventaire.md` | repos, accès réseau |
| 2 -- État du Kanban | `.takeover/01-kanban.md` | kanban |
| 3 -- Graphe des sous-modules | `.takeover/02-graphe-dependances.md` | Phase 1 terminée |
| 4 -- Topologie API et BD | `.takeover/03-topologie-api-bd.md` | Phase 1 terminée |
| 5 -- Décomposition fonctionnelle | `.takeover/04-decomposition-fonctionnelle.md` | Phases 3 & 4 |
| 6 -- Plan d'étude | `.takeover/05-plan-etude.md` | Phase 5 terminée |

## Règles absolues

- Tous les fichiers produits doivent être **en français**.

- Ne jamais commiter `.takeover/` -- vérifier `.gitignore` avant Phase 1.

- Ne pas inventer d'informations : signaler `U+26A0U+FE0F Non déterminé` quand la source
  est absente ou ambiguë.

- Produire un résumé de fin de phase avant de passer à la suivante.

## Agent delegation chain

| Step | Agent | Trigger condition | Prompt | Done criteria |
|------|-------|-------------------|--------|---------------|
| 1 | **Project Takeover** | toujours -- analyse multi-repo | *(ce prompt)* | 6 fichiers produits dans `.takeover/` |
| 2 | **Reviewer** | documentation produite | `/pr-review` | Documents vérifiés pour exactitude et complétude |
| 3 | **Delivery Lead** | si des actions découlent de l'analyse | `/project-dispatch` | Issues créées, plan d'action établi |
