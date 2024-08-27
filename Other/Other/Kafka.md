# Kafka

# Quickstart

[https://kafka.apache.org/downloads](https://kafka.apache.org/downloads)

[https://kafka.apache.org/quickstart](https://kafka.apache.org/quickstart)

**# Get Kafka**

[Download](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.4.0/kafka_2.13-3.4.0.tgz) the latest Kafka release and extract it:

`$ tar -xzf kafka_2.13-3.4.0.tgz`

`$ cd kafka_2.13-3.4.0`

**# Start the ZooKeeper service**

[https://zookeeper.apache.org/doc/current/zookeeperStarted.html](https://zookeeper.apache.org/doc/current/zookeeperStarted.html)

1. Скачать ZooKeeper
2. To start ZooKeeper you need a configuration file. Here is a sample, create it in **conf/zoo.cfg**:
    
    ```
    tickTime=2000
    dataDir=/var/lib/zookeeper
    clientPort=2181
    ```
    
3. Now that you created the configuration file, you can start ZooKeeper:
    
    `$ sudo bin/zkServer.sh start`
    

ИЛИ

`$ bin/zookeeper-server-start.sh config/zookeeper.properties`

**# Start the Kafka broker service**

`$ bin/kafka-server-start.sh config/server.properties`

**# Create a topic**

`$ bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092`

`$ bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:29092,localhost:39092,localhost:49092`

**# Show details of topic**

`$ bin/kafka-topics.sh --describe --topic quickstart-events --bootstrap-server localhost:9092`

**# Write some events into the topic**

`$ bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092`
This is my first event
This is my second event

`$ bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:29092,localhost:39092,localhost:49092 --producer.config config/config.properties` 

You can stop the producer client with `Ctrl-C` at any time.

**# Read the events**

`$ bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9092`

This is my first event
This is my second event

`$ bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:29092,localhost:39092,localhost:49092`

You can stop the consumer client with `Ctrl-C` at any time.

**# Удаление логов и временных файлов Kafka**

`$ rm -rf /tmp/kafka-logs /tmp/zookeeper /tmp/kraft-combined-logs`

**# Удалить топик**

`$ bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic orders.commandreplies`

# **Kafka Connect**

**# Import/Export your data as streams of events with kafka connect**

Отредактируйте `config/connect-standalone.properties` файл, добавьте или измените `plugin.path` свойство конфигурации, соответствующее следующему, и сохраните файл:

`plugin.path=libs/connect-file-3.4.0.jar`

где 3.4.0 - версия kafka

Затем создайте файл для тестирования:

```
> echo -e "foo\nbar" > test.txt
```

Далее мы запустим два соединителя, работающих в автономном режиме

`> bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source.properties config/connect-file-sink.properties`

Во время запуска вы увидите ряд сообщений журнала, в том числе некоторые, указывающие на создание экземпляров соединителей. Как только процесс Kafka Connect запущен, коннектор-источник должен начать считывать строки из `test.txt` топика и передавать их в топик `connect-test`, а коннектор-приемник должен начать читать сообщения из топика `connect-test` и записывать их в файл `test.sink.txt`.

Обратите внимание, что данные хранятся в топике Kafka `connect-test`

`> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic connect-test --from-beginning`

# **Debezium**

[Debezium](Kafka/Debezium.md)

# CLI

Запуск команд из каталога kafka/bin/

Получить список топиков
`bin/kafka-topics.sh --bootstrap-server kafka-prod01.zvq.me:9092,kafka-prod02.zvq.me:9092,kafka-prod03.zvq.me:9092 --list`

`bin/kafka-topics.sh --bootstrap-server localhost:9092 —list`

Получить информацию о топике [https://kafka.apache.org/documentation/#topicconfigs](https://kafka.apache.org/documentation/#topicconfigs)
`bin/kafka-topics.sh --bootstrap-server kafka-prod01.zvq.me:9092,kafka-prod02.zvq.me:9092,kafka-prod03.zvq.me:9092 --describe --topic cs2proto_raw4`

Чтение топика
`bin/kafka-console-consumer.sh --topic content_request_events --bootstrap-server kafka-01.me:9092,kafka-02.me:9092 --from-beginning`

Получить список consumer groups

`bin/kafka-consumer-groups.sh  --list --bootstrap-server kafka-prod01.zvq.me:9092,kafka-prod02.zvq.me:9092,kafka-prod03.zvq.me:9092`

Получить описание consumer group

`bin/kafka-consumer-groups.sh --describe --group inapp-story-game-consumer --bootstrap-server kafka-prod01.zvq.me:9092,kafka-prod02.zvq.me:9092,kafka-prod03.zvq.me:9092`

`bin/kafka-topics.sh --bootstrap-server 10.40.2.37:9093,10.40.2.161:9093,10.40.2.69:9093,10.40.2.8:9093,10.40.2.181:9093 --list`

`bin/kafka-topics.sh --bootstrap-server 10.40.2.78:9093,10.40.2.250:9093,10.40.2.159:9093,10.40.2.87:9093,10.40.2.180:9093 --list`