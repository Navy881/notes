# Prometheus

Приложение, используемое для мониторинга и оповещения о событиях. Оно записывает метрики в реальном времени в базу данных временных рядов, созданную с использованием модели извлечения HTTP, с гибкими запросами и оповещениями в реальном времени.

[localhost:9090/graph](http://localhost:9090/graph)

[localhost:9090/metrics](http://localhost:9090/metrics)

# Установка

`docker run -p 9090:9090 prom/prometheus`

Со своим кофигом

```bash
docker run \
    -p 9090:9090 \
    -v /home/u1/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```

<aside>
💡 Если Grafana и Prometheus развернуты в Docker.

Локальный хост одного контейнера не является локальным хостом другого контейнера, даже если вы опубликовали порт для хоста – вы не можете связаться с контейнером Prometheus или хостом, используя localhost из контейнера Grafana. Вам необходимо использовать IP-адрес контейнера Prometheus или имя хоста, если вы используете Docker Compose.

</aside>

<aside>
💡 Для досутпа из docker-контейнера с Grafana в docker-контейнер БД необходимо настроить сеть между контейнерами [https://habr.com/ru/post/554190/](https://habr.com/ru/post/554190/)

</aside>

Установка на машину

```
wget https://github.com/prometheus/prometheus/releases/download/v2.40.7/prometheus-2.40.7.linux-amd64.tar.gz
tar xvf prometheus-2.40.7.linux-amd64.tar.gz
cd prometheus-2.40.7.linux-amd64
```

Запуск

`./prometheus --config.file=/home/u1/prometheus/prometheus.yml`

# **Monitor Linux Servers Using Prometheus**

[https://prometheus.io/docs/guides/node-exporter/](https://prometheus.io/docs/guides/node-exporter/)

### Setup Node Exporter Binary

**Step 1:** Download the latest node exporter package. You should check the [Prometheus downloads section](https://prometheus.io/download/) for the latest version and update this command to get that package.

```
cd /tmp
curl -LO https://github.com/prometheus/node_exporter/releases/download/v1.5.0/node_exporter-1.5.0.linux-amd64.tar.gz
```

**Step 2:** Unpack the tarball

```
tar -xvf node_exporter-1.5.0.linux-amd64.tar.gz
```

**Step 3:** Move the node export binary to /usr/local/bin

```
sudo mv node_exporter-1.5.0.linux-amd64.tar.gz/node_exporter /usr/local/bin/
```

### Create a Custom Node Exporter Service

**Step 1:** Create a node_exporter user to run the node exporter service.

```
sudo useradd -rs /bin/false node_exporter
```

**Step 2:** Create a node_exporter service file under systemd.

```
sudo vi /etc/systemd/system/node_exporter.service
```

**Step 3:** Add the following service file content to the service file and save it.

```
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

**Step 4:** Reload the system daemon and star the node exporter service.

```
sudo systemctl daemon-reload
sudo systemctl start node_exporter
```

**Step 5:** check the node exporter status to make sure it is running in the active state.

```
sudo systemctl status node_exporter
```

**Step 6:** Enable the node exporter service to the system startup.

```
sudo systemctl enable node_exporter
```

Now, node exporter would be exporting **metrics on port 9100.**

You can see all the server metrics by visiting your server URL on /metrics as shown below.

```
http://<server-IP>:9100/metrics 

curl http://localhost:9100/metrics
```