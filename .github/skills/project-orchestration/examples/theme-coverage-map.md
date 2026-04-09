# Theme Coverage Map

## Objective

Cover requested themes while preventing duplication by reusing existing assets first.

## Coverage

- **Diagrams (PlantUML/open-source tools)**
  - Added: `diagram-tooling` skill
  - Added: `/diagram-ops` prompt

- **.NET top-tier expertise**
  - Reused: `aspnet-core`, `ef-core`, `dotnet-cli`, `dotnet-testing`, `openapi`, `contracts`
  - Governance: route through project orchestration + review gates

- **Scripting**
  - Reused: `bash`, `powershell`, `python`, `perl`, `batch`
  - Routing already available under automation capabilities

- **Markdown docs operations**
  - Added: `markdown-docops` skill
  - Added: `/markdown-ops` prompt
  - Reused: `doc-architecture-model`, `doc-qa`, `/doc-lint-fix`, `/generate-docs-tree`

- **React front ends**
  - Reused: `react`, `typescript`, `js-testing`

- **PostgreSQL**
  - Reused: `postgres`, `pgadmin`

- **EF in .NET**
  - Reused: `ef-core`, `dotnet-testing`

- **Deep PR reviewing**
  - Reused: `pr-review` skill and `/pr-review` prompt

## Routing updates included

- docs-system aliases expanded for markdown/diagram operations
- docs-system domain keywords include PlantUML/Mermaid/markdown operations
- matrix includes `/diagram-ops` and `/markdown-ops` with skills

## Governance updates included

- Added customization governance instruction for mandatory instruction/routing compliance
- Updated PromptSmith and `new-theme-pack` expectations to enforce routing end-to-end
