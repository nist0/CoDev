# Examples - rest-api-design-governance

## New API design

```text
/rest-api-new-service apiName=CatalogApi resources="Products,Categories" versioning=route
```

Expected output:

- Route map per resource.

- DTO and IMediator command/query map.

- Error/OpenAPI quality checklist.

## Add a resource safely

```text
/rest-api-add-resource resource=Products operations="create,getById,update,delete,list" apiVersion=v1
```

Expected output:

- Resource endpoints and contracts.

- Validation and `ProblemDetails` mapping.

- Compatibility notes for existing clients.

## REST API Design Governance Skill -- Examples

## 1. OpenAPI Validation

```sh
swagger-cli validate openapi.yaml
```

## 2. Versioned Route Example

```text
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/orders")]
```

## 3. Contract Test (Pact)

```js
const { Pact } = require('@pact-foundation/pact');
// ...
```
