# Grafana

# Установка

Lightweight Docker container image using an [Alpine](https://alpinelinux.org/) base image.

`docker run -d --name=grafana -p 3000:3000 grafana/grafana-enterprise`

# Вход

Чтобы войти в Grafana в первый раз:

1. Откройте свой веб-браузер и перейдите на [http://localhost:3000](http://localhost:3000/) /.
HTTP-порт по умолчанию 3000, если только вы не настроили другой порт.
2. На странице входа введите логин `admin` и пароль `admin`.
3. Нажмите Войти. 
В случае успеха вы увидите приглашение сменить пароль.
4. Нажмите "ОК" в приглашении и измените свой пароль.

# Создание дашборда

1. Нажмите **New dashboard** под пунктом бокового меню **Dashboards**.
2. Выберите **Add an empty panel**.
3. Перейдите на вкладку **Query**.
4. Выберите data source `- Grafana --` и добавьте [query](https://grafana.com/docs/grafana/latest/panels-visualizations/query-transform-data/#add-a-query) с типом Random Walk.
5. Сохраните дашборд

# Добавление data source

1. Боковое меню → **Configuration → Data sources**
2. Нажать на **Add data source**
3. Выберите новый источник данных
4. Настройте источник данных, следуя инструкциям, специфичным для этого источника данных.

<aside>
💡 Для досутпа из docker-контейнера с Grafana в docker-контейнер БД необходимо настроить сеть между контейнерами [https://habr.com/ru/post/554190/](https://habr.com/ru/post/554190/)

[Docker](Docker.md)

</aside>