# Порядок выполнения практической части

## Установить инструменты

1. yc <https://yandex.cloud/ru/docs/cli/operations/install-cli>
2. kubectl <https://kubernetes.io/docs/tasks/tools/>
3. Lens <https://k8slens.dev/>
4. Helm <https://helm.sh/docs/intro/install/>

## Развернуть K8s кластер

Должен быть развернут по итогам зантия 35

## Соединиться и проверить что все работает

Проверить, что работаете с yandex:

```shell
kubectl config get-contexts
```

При необходимости переключиться на yanex:

```shell
kubectl config use-context you-yandex-context
```

Усли у вас не установлен контекст вашего кластера, то:

```shell
yc managed-kubernetes cluster get-credentials you-cluster-name --external
```

Если контекст установлен неправильно и его нужно перезаписать:

```shell
yc managed-kubernetes cluster get-credentials you-cluster-name --external --force
```

После этого переключить контекст на ваш кластер.

Вернуть список кластеров:

```shell
yc managed-kubernetes clusters list
```

Запустить кластер:

```shell
yc managed-kubernetes cluster start you-cluster-name
```

## Развернуть модель в кластере

Должна быть развернута модель titanic по итогам урока 33
<https://github.com/sdukshis/otus-ml-skel/tree/main>

Если нет - то развернуть модель:

```shell
cd otus-ml-skel
kubectl apply -f k8s/titanic-deployment.yml
kubectl apply -f k8d/titanic-service.yml
```

Проверить что модель работает:

```shell
kubectl port-forward services/titanic-service 8081:8000
```

## Развернуть prometheus на кластере

Добавить в helm репозиторий с prometheus:

```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

Установить на кластере prometheus+grafana:

```shell
helm install monitoring prometheus-community/kube-prometheus-stack
```

Посмотреть какие helm-charts установлены:

```shell
helm list
```

## Посмотрим на работу

Открыть мониторинг на сервис prometheus

Открыть мониторинг на сервис grafana

Показать где брать логин, пароль для входа в grafana

## Настрить мониторинг кастомных метрик

Показать где определяется сбор кастомных метрик
файл service/main.py

```python
from starlette_exporter import PrometheusMiddleware, handle_metrics
from prometheus_client import Counter

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

SURVIVED_COUNTER = Counter("survived", "Number of survived passengers")
PCLASS_COUNTER = Counter("pclass", "Number of passengers by class", ["pclass"])

```

Развернем сервис мониторинга titanic'a

```shell
kubectl apply -f k8s/monitoring-titanic.yml
```

Для сбора метрик развернем сервисный аккаунт

```shell
kubectl apply -f k8s/prom_rbac.yml
```

Проверим что метрики отображаются в grafana
