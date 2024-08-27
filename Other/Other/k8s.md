# k8s

# **Как выглядит доступ в Kubernetes?**

Коллеги DevOps предоставят вам конфигурацию следующего содержимого для подключения к каждому из кластеров Kubernetes.

В каждом из таких блоков будет информация о подключении к кластеру, имени пользователя и токене.

```bash
apiVersion: v1
kind: Config
clusters:
  - name: internal
    cluster:
      server: 'https://101.160.0.106:5443'
      certificate-authority-data: >-
        <Long-Long-Long BASE64 DATA>
users:
  - name: <username>
    user:
      token: >-
        <Long-Long-Long BASE64 DATA>
contexts:
  - name: internal
    context:
      user: <username>
      cluster: internal
      namespace: default
current-context: internal
```

Сохраните конфигурацию каждого из кластеров в отдельные файлы `stage`, `infra`, `preprod` и `prod` в профиле пользователя в директорию:

- На Mac: `~./kube/config/`
- На Windows: `C:\Users\<Username>\.kube\config\`

На Windows для управления кластерами Kubernetes понадобится приложение kubectl. Как его установить, смотрите на странице [https://kubernetes.io/ru/docs/tasks/tools/install-kubectl/](https://kubernetes.io/ru/docs/tasks/tools/install-kubectl/) .

Проверьте доступность всех кластеров выполнением команд `kubectl cluster-info` с указанием пути к конфигурации кластеров.

```bash
Windows C:\Users>kubectl cluster-info --kubeconfig=%USERPROFILE%\.kube\config\stage
Mac user@C02DNCGRMD6M ~ % kubectl cluster-info --kubeconfig=./.kube/config_stage.json --namespace=backend

Kubernetes control plane is running at https://10.16.0.106:5443
CoreDNS is running at https://10.16.0.106:5443/api/v1/namespaces/kube-system/services/coredns:dns/proxy
 
To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
 
C:\Users>kubectl cluster-info --kubeconfig=%USERPROFILE%\.kube\config\preprod
Kubernetes control plane is running at https://10.14.1.46:5443
CoreDNS is running at https://10.14.1.46:5443/api/v1/namespaces/kube-system/services/coredns:dns/proxy
 
To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
 
C:\Users>kubectl cluster-info --kubeconfig=%USERPROFILE%\.kube\config\prod
Kubernetes control plane is running at https://10.40.0.245:5443
CoreDNS is running at https://10.40.0.245:5443/api/v1/namespaces/kube-system/services/coredns:dns/proxy
 
To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

В дальнейшем при длительной работе с конкретным кластером можно устанавливать значение переменной окружения `KUBECONFIG`, после чего значение `--kubeconfig` можно не указывать. Например:

```bash
C:\Users>set KUBECONFIG=%USERPROFILE%\.kube\config\stage

C:\Users>kubectl cluster-info
Kubernetes control plane is running at https://10.16.0.106:5443
CoreDNS is running at https://10.16.0.106:5443/api/v1/namespaces/kube-system/services/coredns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

# kubectl

[Шпаргалка по kubectl](https://kubernetes.io/ru/docs/reference/kubectl/cheatsheet/)

## **Просмотр и поиск ресурсов**

```bash
kubectl get pods --kubeconfig=./.kube/config_stage.json --namespace=backend

# Get-команды с основном выводом
kubectl get services                          # Вывести все сервисы в пространстве имён
kubectl get pods --all-namespaces             # Вывести все поды во всех пространств имён
kubectl get pods -o wide                      # Вывести все поды в текущем пространстве имён с подробностями
kubectl get deployment my-dep                 # Вывести определённое развёртывание
kubectl get pods                              # Вывести все поды в пространстве имён
kubectl get pod my-pod -o yaml                # Получить информацию по поду в формате YAML

# Посмотреть дополнительные сведения команды с многословным выводом
kubectl describe nodes my-node
kubectl describe pods my-pod

# Вывести сервисы, отсортированные по имени
kubectl get services --sort-by=.metadata.name

# Вывести поды, отсортированные по количеству перезагрузок
kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'

# Вывести постоянные тома (PersistentVolumes), отсортированные по емкости
kubectl get pv --sort-by=.spec.capacity.storage

# Получить метку версии всех подов с меткой app=cassandra
kubectl get pods --selector=app=cassandra -o \
  jsonpath='{.items[*].metadata.labels.version}'

# Получить все рабочие узлы (с помощью селектора исключаем узлы с меткой 'node-role.kubernetes.io/master')
kubectl get node --selector='!node-role.kubernetes.io/master'

# Получить все запущенные поды в пространстве имён
kubectl get pods --field-selector=status.phase=Running

# Получить внешние IP-адреса (ExternalIP) всех узлов
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'

# Вывести имена подов, принадлежащие к определённому RC
# Использование команды "jq" помогает упросить поиск в jsonpath, подробнее смотрите на сайте https://stedolan.github.io/jq/
sel=${$(kubectl get rc my-rc --output=json | jq -j '.spec.selector | to_entries | .[] | "\(.key)=\(.value),"')%?}
echo $(kubectl get pods --selector=$sel --output=jsonpath={.items..metadata.name})

# Показать метки всех подов (или любого другого объекта Kubernetes, которым можно прикреплять метки)
kubectl get pods --show-labels

# Получить готовые узлы
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}' \
 && kubectl get nodes -o jsonpath="$JSONPATH" | grep "Ready=True"

# Вывод декодированных секретов без внешних инструментов
kubectl get secret my-secret -o go-template='{{range $k,$v := .data}}{{"### "}}{{$k}}{{"\n"}}{{$v|base64decode}}{{"\n\n"}}{{end}}'

# Вывести все секреты, используемые сейчас в поде.
kubectl get pods -o json | jq '.items[].spec.containers[].env[]?.valueFrom.secretKeyRef.name' | grep -v null | sort | uniq

# Вывести все идентификаторы (containerID) контейнеров инициализации (initContainers) во всех подах.
# Это полезно при очистке остановленных контейнеров, не удаляя при этом контейнеры инициализации.
kubectl get pods --all-namespaces -o jsonpath='{range .items[*].status.initContainerStatuses[*]}{.containerID}{"\n"}{end}' | cut -d/ -f3

# Вывести события, отсортированные по временной метке
kubectl get events --sort-by=.metadata.creationTimestamp

# Сравнить текущее состояние кластера с состоянием, в котором находился бы кластер в случае применения манифеста.
kubectl diff -f ./my-manifest.yaml
```

Получить все jobs

`kubectl get jobs`

Удалить job

`kubectl delete job <job name>`

Проброс локального порта вашей машины к сервису 

`kubectl port-forward services/temporaltest-web 8080:8080`

Получить все сервисы

`kubectl get svc`

**To restart a Kubernetes pod through the scale command:**

1. Use the following command to set the number of the pod’s replicas to 0:`kubectl scale deployment demo-deployment --replicas=0`The command will turn the Kubernetes pod off.
2. Use the following command to set the number of the replicas to a number more than zero and turn it on:`kubectl scale deployment demo-deployment --replicas=1`The command creates new replicas of the pod that the previous command destroyed. However, the new replicas will have different names.
3. Use the following command to check the status and new names of the replicas:`kubectl get pods`

[Helm](k8s/Helm.md)

[Minikube](k8s/Minikube.md)

[Kiali](k8s/Kiali.md)