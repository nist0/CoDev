---
name: project-takeover
description: >
  Analyse en profondeur un ou plusieurs dépôts GitHub on-premise lors d'une
  prise en charge d'équipe. Produit une documentation exhaustive en français
  dans un répertoire local `.takeover/` (non commité). Couvre : structure des
  dépôts, état du Kanban de référence, graphe des sous-modules, dépendances API
  & BD, décomposition fonctionnelle complète, et plan d'étude point par point.
argument-hint: "[repos=url1,url2] [kanban=url] [output=.takeover]"
user-invocable: true

## disable-model-invocation: false

# Project Takeover (Prise en charge de projet) — Skill

## Quand utiliser cette skill

- Vous rejoignez une nouvelle équipe et devez maîtriser rapidement un ou
  plusieurs projets existants.

- Les dépôts sont hébergés sur un GitHub on-premise (GitHub Enterprise Server).

- Vous avez accès à un projet Kanban GitHub de référence.

- La documentation finale doit être en **français** et rester **locale** (jamais
  commitée).

## Pré-requis

| Élément | Requis | Notes |
|---|---|---|
| Accès réseau au GitHub on-prem | Oui | Token PAT avec `read:repo`, `read:project` |
| `gh` CLI configuré | Oui | `gh auth login --hostname <host>` |
| `git` CLI | Oui | Pour cloner et inspecter les sous-modules |
| Répertoire `.takeover/` dans `.gitignore` | Oui | Vérifier avant de démarrer |

## Procédure en 6 phases

---

### Phase 1 — Initialisation et collecte des dépôts

**Objectif** : Cloner localement tous les dépôts cibles et constituer l'inventaire de base.

1. Créer le répertoire de sortie :
   ```bash
   mkdir -p .takeover
   ```

2. Vérifier que `.takeover/` est dans `.gitignore`. Si absent, l'ajouter
   immédiatement avant toute production de fichier.

3. Pour chaque dépôt cible :
   ```bash
   gh repo clone <owner>/<repo> .takeover/repos/<repo> -- --depth=1
   ```

4. Produire `.takeover/00-inventaire.md` :

   ```markdown

# Inventaire des dépôts — <Date>

   | Dépôt | URL | Branche par défaut | Langue principale | Dernier commit |
   |---|---|---|---|---|
   | <nom> | <url> | <branche> | <langage> | <sha court + date> |
   ```

5. Pour chaque dépôt, noter :

   - Langage(s) dominant(s) (via `git ls-files | grep -E '\.(cs|ts|py|go|java)$' | ...`)

   - Présence de `README`, `CHANGELOG`, `docs/`, `.github/workflows/`

   - Nombre de contributeurs actifs sur les 90 derniers jours :
     ```bash
     git log --since="90 days ago" --format="%ae" | sort -u | wc -l
     ```

**Livrable** : `.takeover/00-inventaire.md`

---

### Phase 2 — État du projet Kanban

**Objectif** : Capturer l'état actuel du Kanban de référence et identifier les
travaux en cours, bloqués, ou en attente.

1. Lister les colonnes et items du projet :
   ```bash
   gh project view <N> --owner <owner> --format json > .takeover/kanban-raw.json
   ```

2. Lister les issues ouvertes liées au projet :
   ```bash
   gh issue list --repo <owner>/<repo> --state open --json number,title,assignees,labels,milestone \
     > .takeover/issues-open.json
   ```

3. Produire `.takeover/01-kanban.md` avec :

   - État des colonnes (Backlog / Todo / In Progress / In Review / Done)

   - Issues par colonne : numéro, titre, assigné, labels

   - Tableau des **travaux en cours** (WIP) avec responsable et date de dernière
     activité

   - Tableau des **blockers** identifiés (label `blocked` ou sans assigné depuis >7 j)

   - Milestones actives et leur avancement

**Livrable** : `.takeover/01-kanban.md`

---

### Phase 3 — Graphe des sous-modules et dépendances inter-dépôts

**Objectif** : Cartographier les relations entre dépôts (sous-modules Git,
packages internes, references croisées).

1. Pour chaque dépôt, détecter les sous-modules :
   ```bash
   git -C .takeover/repos/<repo> submodule status
   cat .takeover/repos/<repo>/.gitmodules 2>/dev/null
   ```

2. Détecter les dépendances inter-packages (packages internes NuGet/npm/pip) :

   - `.csproj` → `<PackageReference>` pointant vers un feed privé

   - `package.json` → dépendances `@<scope>/` ou version `file:`

   - `pyproject.toml` / `requirements.txt` → packages sur index privé

3. Construire le graphe en Mermaid :
   ```mermaid
   graph TD
     RepoA --> SubmoduleB
     RepoA --> LibC["LibC (NuGet interne)"]
     RepoB --> LibC
   ```

4. Produire `.takeover/02-graphe-dependances.md` avec :

   - Diagramme Mermaid du graphe complet

   - Tableau des sous-modules (dépôt parent → sous-module → commit épinglé →
     version)

   - Packages internes partagés et leurs consommateurs

   - Cycles de dépendances détectés (⚠️ à signaler explicitement)

**Livrable** : `.takeover/02-graphe-dependances.md`

---

### Phase 4 — Topologie API et base de données

**Objectif** : Identifier tous les contrats d'API exposés et consommés, ainsi
que les bases de données utilisées.

#### APIs exposées

1. Chercher les définitions OpenAPI/Swagger :
   ```bash
   find .takeover/repos/<repo> -name "openapi*.json" -o -name "swagger*.yaml" \
     -o -name "openapi*.yaml" 2>/dev/null
   ```

2. Chercher les contrôleurs/routes (heuristiques par langage) :

   - .NET : `[ApiController]`, `[Route(`, `app.MapGet(`

   - Node/Express : `app.get(`, `router.post(`

   - Python/FastAPI : `@app.get(`, `@router.post(`

   - Java/Spring : `@RestController`, `@RequestMapping`

3. Pour chaque API exposée, noter : méthode HTTP, path, rôle fonctionnel déduit,
   authentification (Bearer/API key/none).

#### APIs consommées

1. Chercher les clients HTTP :

   - `HttpClient`, `axios`, `requests.get(`, `RestTemplate`, `fetch(`

   - Variables d'environnement contenant `URL`, `ENDPOINT`, `HOST`, `API_URL`

   - Fichiers de configuration : `appsettings.json`, `.env.example`, `config.yaml`

2. Pour chaque dépendance externe identifiée, noter : URL/base URI, protocole
   (REST/gRPC/GraphQL/SOAP), sens (sortant), authentification.

#### Bases de données

1. Identifier les BD via :

   - Chaînes de connexion dans `appsettings*.json`, `.env.example`, `docker-compose.yml`

   - Migrations : répertoire `Migrations/`, `db/migrations/`, `alembic/versions/`

   - ORM/driver : `DbContext`, `Sequelize`, `SQLAlchemy`, `pg`, `mongoose`

2. Pour chaque BD : technologie (PostgreSQL/SQL Server/MongoDB/Redis/…), rôle
   fonctionnel, nom du schéma si détectable, nombre de migrations.

#### Livrable

Produire `.takeover/03-topologie-api-bd.md` avec :

- Diagramme Mermaid `C4Context` (ou équivalent) montrant :

  - Le ou les systèmes étudiés

  - Les API exposées (flèches entrantes)

  - Les API consommées (flèches sortantes)

  - Les bases de données

- Tableaux détaillés par catégorie

**Livrable** : `.takeover/03-topologie-api-bd.md`

---

### Phase 5 — Décomposition fonctionnelle

**Objectif** : Comprendre ce que fait le projet d'un point de vue métier et
technique, module par module.

1. Identifier les modules principaux :

   - Projets dans la solution (`.sln`), packages npm, modules Python

   - Répertoires `src/`, `lib/`, `packages/`, `apps/`

2. Pour chaque module, extraire :

   - **Rôle fonctionnel** : que fait-il ? (déduire du README, des noms de classes,
     des routes, des commentaires)

   - **Flux de données principaux** : entrée → traitement → sortie

   - **Points d'entrée** : `main`, controller, handler, CLI command

   - **Dépendances internes** : quels autres modules il utilise

   - **Tests associés** : présence et couverture estimée

3. Pour les domaines métier, chercher les termes du domaine :

   - Noms de classes `Order`, `Customer`, `Invoice`, `Product`, `User`…

   - Services nommés selon le domaine : `OrderService`, `BillingRepository`…

4. Produire `.takeover/04-decomposition-fonctionnelle.md` :

   ```markdown

# Décomposition fonctionnelle — <Projet>

## Vue d'ensemble

   <description de la raison d'être du système en 3-5 phrases>

## Modules

### <NomModule>

   **Rôle** : <description>
   **Point d'entrée** : `<fichier>:<fonction>`
   **Flux** : <entrée> → <traitement> → <sortie>
   **Dépendances** : <liste>
   **Tests** : <oui/non/partiel> — couverture estimée : <X%|non mesurée>

   ...
   ```

**Livrable** : `.takeover/04-decomposition-fonctionnelle.md`

---

### Phase 6 — Plan d'étude point par point

**Objectif** : Produire un guide d'apprentissage structuré et priorisé pour
maîtriser le projet de façon autonome.

1. Évaluer la complexité de chaque module / intégration (Simple / Modérée /
   Complexe) selon :

   - Nombre de lignes de code

   - Dépendances croisées

   - Présence de logique métier non triviale

2. Proposer un **ordre d'étude recommandé** (du plus simple au plus complexe,
   en commençant par les fondations).

3. Pour chaque point d'étude, fournir :

   - **Titre** du point

   - **Priorité** : Critique / Importante / Secondaire

   - **Durée estimée** : en heures

   - **Objectif d'apprentissage** : ce que l'on doit être capable de faire après

   - **Ressources** : fichiers clés à lire, issues à consulter, personnes à contacter

   - **Exercice de validation** : action concrète prouvant la maîtrise

4. Produire `.takeover/05-plan-etude.md` :

   ```markdown

# Plan d'étude — <Projet> — <Date>

## Synthèse

   | Dimension | Complexité | Durée estimée |
   |---|---|---|
   | Architecture globale | Simple | 2h |
   | Module X | Complexe | 8h |
   | Intégration API Y | Modérée | 4h |
   | Schéma BD | Simple | 1h |
   | **Total estimé** | | **Xh** |

## Points d'étude détaillés

### 1. <Titre>

   **Priorité** : Critique
   **Durée** : Xh
   **Objectif** : <ce que vous saurez faire>
   **Fichiers clés** : `<chemin>`
   **Exercice** : <action de validation>
   ```

**Livrable** : `.takeover/05-plan-etude.md`

---

## Récapitulatif des livrables

| Fichier | Contenu |
|---|---|
| `.takeover/00-inventaire.md` | Inventaire des dépôts, langages, contributeurs |
| `.takeover/01-kanban.md` | État du Kanban, WIP, blockers, milestones |
| `.takeover/02-graphe-dependances.md` | Graphe sous-modules + packages internes |
| `.takeover/03-topologie-api-bd.md` | Carte API exposées/consommées + BD |
| `.takeover/04-decomposition-fonctionnelle.md` | Modules, flux, domaine métier |
| `.takeover/05-plan-etude.md` | Plan d'apprentissage priorisé avec exercices |

## Invariants (non-négociables)

- **Tous les fichiers produits sont en français.**

- **Jamais commiter `.takeover/`** — vérifier `.gitignore` en Phase 1.

- Si une information ne peut pas être déduite de manière fiable, l'indiquer
  explicitement avec `⚠️ Non déterminé — à vérifier manuellement`.

- Les diagrammes Mermaid doivent être valides syntaxiquement.

- Chaque tableau doit avoir une ligne de séparation (`| --- | --- |`).

- Ne pas inventer de dépendances ou de fonctionnalités : se baser uniquement
  sur le code source, les fichiers de configuration, et les issues GitHub.

## Composition avec d'autres skills

Cette skill peut déléguer à :

| Skill | Quand |
|---|---|
| `repo-understanding` | Pour la carte de code détaillée d'un dépôt unique |
| `openapi` | Pour analyser un contrat OpenAPI complet |
| `postgres` | Pour inspecter un schéma PostgreSQL |
| `onboarding-factory` | Pour générer un guide onboarding complet par dépôt |
| `github-work-management` | Pour l'analyse approfondie du Kanban |
| `diagram-tooling` | Pour valider ou convertir les diagrammes Mermaid |
