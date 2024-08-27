# Helm

### Установить helm chart

`helm install temporaltest . --timeout 900s`

```bash
helm install \
    --set cassandra.config.cluster_size=1 \
    temporaltest . --timeout 900s
```

### Деинсталляция helm chart

`helm uninstall temporaltest`

### Показать все charts

`helm list`

### Удалить charts

`helm delete <chart name>`