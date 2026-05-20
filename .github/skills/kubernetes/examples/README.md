# Kubernetes Skill -- Examples

## 1. Validate Resource with kubeval

```sh
kubeval deployment.yaml
```

## 2. Check Events

```text
kubectl get events -n my-namespace
```

## 3. Patch Resource

```sh
kubectl patch deployment my-app -p '{"spec":{"replicas":2}}'
```
