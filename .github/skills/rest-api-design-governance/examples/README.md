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
