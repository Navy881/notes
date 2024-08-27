# Debezium

# Установка

[https://debezium.io/documentation/reference/2.2/install.html](https://debezium.io/documentation/reference/2.2/install.html)

1. Скачать архив с подключаемым модулем для нужного коннетора
2. Распокавать в директорию кафки kafka-3.3.1/kafka/connect
3. В файле config/connect-distributed.properties `plugin.path=` указать абсолютный путь по плагина
    
    ```bash
    plugin.path=/Users/aristov-gv/kafka_2.13-3.4.0/kafka/connect
    ```
    
4. Перезапустить Kafka Connect
    
    `$ bin/connect-distributed.sh config/connect-distributed.properties`
    
5. Настройка конфигурации коннектора (пример для PostgreSQL). 
Ниже приведен пример конфигурации коннектора PostgreSQL, который подключается к серверу PostgreSQL через порт 5432 по адресу 0.0.0.0, логическое имя которого — `fulfillment`.
    
    ```json
    {
      "name": "fulfillment-connector",
      "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    
        "database.hostname": "0.0.0.0",
        "database.port": "5432",
        "database.user": "postgres",
        "database.password": "911911",
        "database.dbname" : "postgres",
    
        "table.whitelist": "public.*",
    
        "topic.prefix": "fulfillment",
    
        "transforms": "Reroute, unwrap",
        "transforms.Reroute.type": "io.debezium.transforms.ByLogicalTableRouter",
        "transforms.Reroute.topic.regex": "(.*)",
        "transforms.Reroute.topic.replacement": "fulfillment",
        "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    
        "key.converter": "org.apache.kafka.connect.json.JsonConverter",
        "key.converter.schemas.enable": false,
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter.schemas.enable": false,
    
        "plugin.name": "pgoutput",
    
        "slot.name": "fulfillment_slot"
      }
    }
    ```
    
    Сохраните конфигурацию в json-файл
    
6. Включить логическую репликацию на сервере PostgreSQL.
В файле postgresql.conf поменять (файл обычно лежит в /var/lib/postgresql/data/)
    
    ```json
    wal_level = logical
    ```
    
    Перезапустить PostgreSQL сервер
    
    ИЛИ
    
    Развернуть в docker образ c настроенным PostgreSQL сервером [https://github.com/debezium/container-images/tree/main/postgres/13](https://github.com/debezium/container-images/tree/main/postgres/13)
    
    `docker build -t "pg13" .` 
    
    `docker run --name "pg_for_debezium" -e POSTGRES_PASSWORD=911911 -d --rm -p 5432:5432 "pg13"`
    
7. Вы можете отправить эту конфигурацию с помощью `POST` команды в работающую службу Kafka Connect. 
`curl -X POST -H "Content-Type: application/json" --data @debezium-config-pg.json http://localhost:8083/connectors`
Служба записывает конфигурацию и запускает одну задачу коннектора, которая выполняет следующие действия:
    1. Подключается к базе данных PostgreSQL.
    2. Читает журнал транзакций.
    3. Потоки меняют записи событий в топик Kafka.
    
    Для удаления конфигурации `curl -X DELETE http://localhost:8083/connectors/{name}` 
8. После внсения изменений в БД в Kafka появится топик **fulfillment** c событиями об изменениях в базе в люблей таблицы схемы public
Просмотр событий в топике **fulfillment**
`bin/kafka-console-consumer.sh --topic fulfillment --from-beginning --bootstrap-server localhost:9092`

# Файл конфигурации

```json
{
  "name": "fulfillment-connector",  // Название коннектора
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",  // Класс коннектора

    "database.hostname": "0.0.0.0",  // Адрес БД
    "database.port": "5432",  // Порт БД
    "database.user": "postgres",  // User в БД
    "database.password": "911911",  // Пароль в БД
    "database.dbname" : "postgres",  // Название БД

    "table.whitelist": "public.*",  // Таблицы для захвата
		"table.include.list": "public.inventory",  // Список таблиц для захвата

    "topic.prefix": "fulfillment",  // Префикс топика Kafka

    "transforms": "Reroute, unwrap",  // Перобразователи сообщения для Kafka (перенаправление, формат extra-данных)
    "transforms.Reroute.type": "io.debezium.transforms.ByLogicalTableRouter",  // Тип преобразователя перенаправления событий
    "transforms.Reroute.topic.regex": "(.*)",  // Условия перенаправления
    "transforms.Reroute.topic.replacement": "fulfillment",  // Название топика для перенаправленных событий
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState", // Тип преобразования extra данных события

    "key.converter": "org.apache.kafka.connect.json.JsonConverter",  // Конвертер для key события
    "key.converter.schemas.enable": false, // Не возвращать schema в json key для события Kafka

    "value.converter": "org.apache.kafka.connect.json.JsonConverter",  // Конвертер для value события
    "value.converter.schemas.enable": false,  // Не возвращать schema в json value для события Kafka

    "plugin.name": "pgoutput",  // Модуль логического декодирования вывода в PostgreSQL
		"publication.autocreate.mode": "filtered",  // Параметр определяет, как должно работать создание публикации

    "slot.name": "fulfillment_slot_pgoutput"  // Название репликационного слота в PostgreSQL (в случае изменения модуля вывода необходимо изменить slot)
  }
}
```