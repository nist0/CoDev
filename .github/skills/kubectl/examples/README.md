# kubectl Skill -- Examples

## 1. List Pods

```sh
kubectl get pods -n my-namespace
```

## 2. Apply Manifest

```text
kubectl apply -f deployment.yaml
```

## 3. Debug Pod

```sh
kubectl exec -it my-pod -- /bin/sh
```
