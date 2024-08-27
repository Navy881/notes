# Redis

Подключение к удалённому серверу (REDIS_DSN=redis://:sQeGCF9Nynh6W6JJh29BWCsY@10.16.5.224:6379)

redis-cli -h 10.16.5.224 -p 6379 -a sQeGCF9Nynh6W6JJh29BWCsY

**Команды:**

- `info memory` - информация о используемой памяти
- `INFO Keyspace | grep ^db` - информация о количестве ключей
- `KEYS *` - посмотреть все ключи
- `flushall` - удаляет все ключи из всех баз данных на текущем хосте.