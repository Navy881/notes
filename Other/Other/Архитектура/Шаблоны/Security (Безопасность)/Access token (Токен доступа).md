# Access token (Токен доступа)

### Проблема

Как передать данные об отправителе запроса сервисам, обрабатывающим запрос?

Аутентификацию пользователей можно реализовать несколькими способами. Например, эту функцию могут взять на себя отдельные сервисы. 

Проблемы этого подхода:

- Он допускает попадание неаутентифицированных запросов во внутреннюю сеть. К тому же каждая команда разработчиков должна обеспечить надлежащую безопасность своих сервисов. В итоге существенно возрастает риск возникновения уязвимостей.
- Разные клиенты могут по-разному себя аутентифицировать. Клиенты, работающие исключительно через API, предоставляют учетные данные в каждом запросе (так, например, делается при HTTP-аутентификации). Другие клиенты могут сначала войти в систему, а затем прилагать токен сеанса к каждому вызову. Мы не хотим, чтобы сервисы отвечали за поддержку разнообразных механизмов аутентификации.

Лучше сделать так, чтобы любой запрос, прежде чем попасть к сервису, аутен­тифицировался API-шлюзом. 

					

### Решение

API-шлюз передаёт токен с информацией о пользователе, включая его идентификатор и роли, сервисам, к которым тот обращается.

Клиенты аутентифициру­ются API-шлюзом и включают свои учетные данные в каждый запрос. Клиенты, которым нужно сначала войти в систему, шлют API-шлюзу сведения о пользователе методом POST, получая в ответ токен сеанса. Аутентифицировав запрос, API-шлюз обращается к одному или нескольким сервисам.

Сервис, к которому обратился API-шлюз, должен опознать субъекта, выполня­ющего запрос. Он также должен проверить, был ли этот запрос аутентифицирован. Для этого при каждом обращении к сервису API-шлюз указывает токен. С помощью токена сервис проверяет подлинность запроса и извлекает информацию о субъекте. API-шлюз может выдавать этот токен и клиентам, ориентированным на сеансы, в этом случае он становится токеном сеанса.

Для API-клиентов последовательность событий выглядит так.

1. Клиент делает запрос, содержащий учетные данные.
2. API-шлюз аутентифицирует учетные данные, создает токен безопасности и пере­дает его сервису (-ам).

Клиенты, которые входят в систему, проходят через такую цепочку событий.

1. Клиент делает запрос на вход в систему, содержащий учетные данные.
2. API-шлюз возвращает токен безопасности.
3. Клиент включает токен безопасности в запрос на выполнение операции.
4. API-шлюз проверяет токен безопасности и направляет запрос к сервису (-ам).

![Untitled](Untitled%202.png)

### Преимущества

- Идентификация запрашивающего лица безопасно передается по системе.
- Благодаря такому централизованному подходу мы можем сосредоточиться на одном участке приложения, что существенно снижает риск возникновения уязвимостей.
- За работу с разными механизмами аутентификации отвечает лишь API-шлюз. Сервисы ограждены от всех этих нюансов.
- Сервисы могут проверить, имеет ли запрашивающая сторона полномочия на выполнение операции.

### Недостатки

-