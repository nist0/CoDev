# Exemples — skill `project-takeover`

## Exemple 1 — Prise en charge d'un mono-dépôt on-prem

**Invocation** :

```text
/project-takeover repos=https://github.corp.example.com/myteam/billing-service kanban=https://github.corp.example.com/orgs/myteam/projects/3
```

**Résultat attendu** :

```text
.takeover/
  00-inventaire.md          ← 1 dépôt, .NET 8, 3 contributeurs actifs
  01-kanban.md              ← 12 issues en cours, 2 blockers identifiés
  02-graphe-dependances.md  ← 2 sous-modules (shared-contracts, logging-lib)
  03-topologie-api-bd.md    ← 3 endpoints REST exposés, 1 API externe (Stripe), PostgreSQL
  04-decomposition-fonctionnelle.md  ← 5 modules (Orders, Billing, Notifications, Auth, Common)
  05-plan-etude.md          ← 14h d'étude estimées, 8 points détaillés
```

## Exemple 2 — Prise en charge d'un mono-repo multi-projets

**Invocation** :

```text
/project-takeover repos=https://github.corp.example.com/platform/api,https://github.corp.example.com/platform/frontend,https://github.corp.example.com/platform/infra kanban=https://github.corp.example.com/orgs/platform/projects/1
```

**Résultat attendu** :

```text
.takeover/
  00-inventaire.md          ← 3 dépôts (C#, TypeScript, Bicep)
  01-kanban.md              ← Projet multi-repo, 34 items, 3 milestones
  02-graphe-dependances.md  ← frontend consomme api; infra déploie les deux
  03-topologie-api-bd.md    ← API REST + gRPC interne, Azure SQL + Redis
  04-decomposition-fonctionnelle.md  ← 9 modules sur 3 dépôts
  05-plan-etude.md          ← 32h estimées, ordre : infra → api → frontend
```

## Points clés à vérifier après exécution

- [ ] `.takeover/` est dans `.gitignore` (ne pas commiter)

- [ ] Tous les documents sont en français

- [ ] Aucune information inventée — les `⚠️ Non déterminé` sont présents là où les données manquent

- [ ] Les diagrammes Mermaid se rendent correctement dans un aperçu Markdown

- [ ] Le plan d'étude (Phase 6) contient des exercices de validation concrets
