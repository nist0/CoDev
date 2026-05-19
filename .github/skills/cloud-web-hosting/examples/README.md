# Cloud Web Hosting Examples

## Example 1 - Static Web App with custom domain

Use when the app is mostly static content with a small API surface:

```text
Goal: host a marketing site on Azure Static Web Apps and point app.example.com through Cloudflare.
Need: custom domain, TLS, preview environments, and a low-maintenance deployment path.
```

Expected guidance:

- pick Azure Static Web Apps for the front end

- keep DNS in Cloudflare with a CNAME validation flow

- verify the deployed URL before updating the public record

## Example 2 - Container Apps Consumption with SQL Free Tier

Use when the app needs a container runtime and a cheap relational backend:

```text
Goal: deploy an ASP.NET Core API to Azure Container Apps Consumption with Azure SQL Database Free Tier.
Need: startup health checks, environment variables, and an EF Core migration path.
```

Expected guidance:

- choose Container Apps Consumption for the runtime

- keep the database connection string externalized

- use the `ef-core` skill for migrations and provider-specific model guidance

## Example 3 - DNS cutover for an existing app

Use when moving an existing hostname to Azure-hosted infrastructure:

```text
Goal: move api.example.com from a legacy host to Azure Container Apps.
Need: minimize downtime, keep Cloudflare authoritative, and confirm certificate issuance.
```

Expected guidance:

- lower TTL before cutover

- verify CNAME or A record target matches the Azure service

- test the new endpoint before and after DNS propagation
