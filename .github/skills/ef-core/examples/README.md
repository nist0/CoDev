# EF Core Skill — Examples

## 1. Add Migration

```sh
dotnet ef migrations add InitialCreate
```

## 2. Update Database

```text
dotnet ef database update
```

## 3. LINQ Query

```csharp
var orders = await dbContext.Orders.Where(o => o.Status == "Open").ToListAsync();
```
