---
name: cloud-web-hosting
description: Azure Static Web Apps, Azure Container Apps Consumption, Azure SQL Database Free Tier, and Cloudflare DNS for web app hosting and custom domains.
argument-hint: "[hosting-or-dns] [constraint]"
user-invocable: true

disable-model-invocation: false
---

# Cloud Web Hosting (Azure + Cloudflare) (Elite)

## When to use

- Choosing between Azure Static Web Apps and Azure Container Apps Consumption.

- Wiring a custom domain and DNS through Cloudflare.

- Sizing a low-cost web app stack around Azure SQL Database Free Tier.

- Planning the hosting side of a .NET API or web app that already uses EF Core.

> For EF Core modeling, migrations, and query performance, use the [`ef-core` skill](.github/skills/ef-core/SKILL.md).
> For broader Azure CLI and resource operations, use the [`azure` skill](.github/skills/azure/SKILL.md) and [`az` skill](.github/skills/az/SKILL.md).

## Workflow

1) Pick the hosting shape

   - Static front end with optional lightweight API -> Azure Static Web Apps.

   - Containerized app with flexible runtime -> Azure Container Apps Consumption.

   - Shared relational store for a small app -> Azure SQL Database Free Tier.
2) Define the boundary

   - Separate app hosting, app config, database, and DNS ownership.

   - Keep DNS records and TLS assumptions explicit.
3) Plan the data path

   - If the app uses EF Core, confirm provider, migrations flow, and connection string source.

   - Validate that free-tier limits fit the expected workload.
4) Wire DNS and custom domains

   - Decide whether Cloudflare is authoritative or just a registrar/proxy.

   - Verify CNAME/A records, TTLs, and certificate validation steps.
5) Verify deployment path

   - Check build output, startup command, and environment variables.

   - Confirm the app responds through the custom domain before widening traffic.

## Self-check

- [ ] Hosting model chosen explicitly: Static Web Apps, Container Apps Consumption, or another target.

- [ ] DNS ownership and record type confirmed before cutover.

- [ ] EF Core concerns handed off to the `ef-core` skill when schema or migration work is involved.

- [ ] Free-tier resource limits reviewed before launch.

- [ ] Verification path defined for the deployed URL and custom domain.

## Outputs

- Hosting recommendation and deployment shape.

- DNS and custom-domain checklist for Cloudflare.

- Free-tier sizing and risk notes.

- Cross-reference to EF Core and Azure operational skills when needed.
