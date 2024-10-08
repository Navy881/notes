# Transactional outbox (Публикация событий)

### **Проблема**

Сервису нужно публиковать сообщения в рамках транзакции, обновляющей базу данных. Обновление базы данных и отправка сообщения должны происходить в пределах одной транзакции, иначе сервис может обновить БД и, например, отказать до того, как сообщение будет отправлено. Если не выполнять эти две операции атомарно, сбой может оставить систему в несогласованном состоянии.

### **Решение**

Сервис публикует событие или сообщение в рамках транзакции БД, сохраняя его в таблицу OUTBOX.

Он использует таблицу БД в качестве временной очереди сообщений. У сервиса, отправляющего сообщения, есть таблица OUTBOX. В рамках транзакции, которая создает, обновляет и удаляет бизнес-объекты, сервис шлет со­общения, вставляя их в эту таблицу. Поскольку это локальная ACID-транзакция, атомарность гарантируется.

Таблица OUTBOX играет роль временной очереди сообщений. 

*Ретранслятор* (MessageRelay) — это компонент, который читает таблицу OUTBOX и передает со­общения брокеру.

![Untitled](Transactional%20outbox%20(%D0%9F%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F%20%D1%81%D0%BE%D0%B1%D1%8B%D1%82%D0%B8%D0%B8%CC%86)/Untitled.png)

Аналогичный подход можно применять и к некоторым базам данных NoSQL. Каждый бизнес-объект, хранящийся в виде записи внутри БД, имеет атрибут со списком сообщений, которые нужно опубликовать. Обновляя этот объект, сервис добавляет в список новое сообщение. Это атомарная операция, поскольку она вы­полняется за один запрос к базе данных. Трудность данного подхода связана с эффек­тивным поиском бизнес-объектов, содержащих события, и их публикацией.

Существует несколько способов доставки сообщений от базы данных к брокеру.

[**Polling publisher (Опрашивающий издатель)**](Polling%20publisher%20(%D0%9E%D0%BF%D1%80%D0%B0%D1%88%D0%B8%D0%B2%D0%B0%D1%8E%D1%89%D0%B8%D0%B8%CC%86%20%D0%B8%D0%B7%D0%B4%D0%B0%D1%82%D0%B5%D0%BB%D1%8C).md)

[**Transaction log tailing (Отслеживание тразакционного журнала)**](Transaction%20log%20tailing%20(%D0%9E%D1%82%D1%81%D0%BB%D0%B5%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%82%D1%80%D0%B0%D0%B7%D0%B0%D0%BA%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%BE.md)