# Docker

[Шпаргалка по Docker](https://habr.com/ru/companies/flant/articles/336654/)

### **Обновление Docker на Linux**

1. Остановите текущий Docker-демон:
`sudo systemctl stop docker`
2. Удалите текущую версию Docker:
`sudo apt-get remove docker docker-engine docker.io containerd runc`
3. Установите зависимости, необходимые для установки Docker:
`sudo apt-get update`
`sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common`
4. Добавьте официальный ключ GPG Docker:
`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`
5. Добавьте репозиторий Docker в список источников пакетов:
`sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable”`
6. Обновите список пакетов и установите Docker:
`sudo apt-get update`
`sudo apt-get install docker-ce docker-ce-cli containerd.io`
7. Проверьте версию Docker, чтобы убедиться, что установка прошла успешно:
`docker --version`

### **Создание развертывания docker-контейнера для приложения**

1. Установка Docker
2. Создание Dockerfile
3. Сборка docker-образа > `docker build -t "image_tag_name" .` (. указание на путь каталога)
4. Просмотр созданных образов > `docker images`
5. Запуск образа > `docker run --name "container_name" -d --rm -p 8080:8080 "image_tag_name"`
-d - запуск контейнера в фоне без блокировки терминала
--rm - контейнер будет автоматически удален после выполнения или остановки
-p - проброс портов порт машины:порт контейнера
-e - значение переменной окружения (пример: -e TZ=Europe/Moscow)
-v - монтирование локальных каталогов (абсолютный путь до локального каталога/наименование volume:путь до каталога в контейнере)
6. Просмотр запущенных контейнеров > `docker ps`
7. Просмотр всех контейнеров > `docker ps -a`
8. Остановка контейнера > `docker stop "container_name/container_id"`
9. Удаление конкретного контейнера > `docker rm "container_name/container_id"`
10. Удаление всех контейнеров > `docker rm $(docker ps -a -q)` (-q - вывести id контейнеров)
11. Просмотр docker volume > `docker volume ls`
12. Создание docker volume > `docker volume create "volume_name"`
13. Удаление docker-образа > `docker rmi "image_name/image_id"`
14. Удаление всех docker-образов > `docker rmi $(docker images -q)`
15. Удаление всех volumes > `docker volume rm $(docker volume ls -q)`

### Docker-compose

1. Установть Docker
2. В репозитории создать и заполнить Dockerfile
3. В репозитории создать и заполнить docker-compose.yml
4. ОПЦИОНАЛЬНО. Для указания пути к файлу Compose, не находящемуся в текущем каталоге, можно использовать флаг -f  `docker-compose -f /path/to/docker-compose.yml`
5. Собрать образы и запустить контейнеры `docker-compose up -d --build`
    
    ```bash
    docker-compose up --force-recreate --build -d
    docker-compose --env-file local.env up -d --build  (c env)
    docker-compose -f docker-compose.full.yml --profile dev up -d --build hobbies
    docker image prune -f
    ```
    
6. Рестарт контейнеров `docker-compose restart`
7. Остановка контенйров `docker-compose down`
8. Удаление всех контейнеров `docker rm -f $(docker ps -a -q)`
9. Удаление всех volumes `docker volume rm $(docker volume ls -q)`
    1. `docker-compose down --volumes`
10. Рестарт контейнеров `docker-compose up -d --build`

### Docker-hub

1. Зарегистрироваться на docker-hub
2. Авторизация в docker-hub > `docker login`
3. Сборка docker-образа > `docker build -t docker-hub_username/"image_tag_name" .`
4. Отправка обзара в docker-hub > `docker push docker-hub_username/"image_tag_name"`

### Другие команды

- Запуск `docker-compose up -d`
- Остановка `docker-compose stop`
- Создание образа `docker build -t myimage .`
- Просмотр образов `docker images`
- Просмотр volume `docker volume ls`
- Запуск контейнера `docker run -d -p 5000:5000 myimage`
- Просмотр запущенных контейнеров `docker ps`
- Перезагрузка контейнера `docker restart container_id`
- Остановка контейнера `docker stop container_id`
- Удаление контейнера `docker rm container_id`
- Получить ip контейнера
`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id`
- Запустить SQL в контейнере c PostrgeSQL `psql -U postgres`

Чтобы удалить все остановленные контейнеры и неиспользуемые образы (а не только образы, не связанные с контейнерами)
`docker system prune -a`

Удалить все неиспользуемые образы

`docker image prune -f`

Удалить все неиспользуемые volume
`docker volume prune`

Очистить весь build cache

`docker builder prune`

Посмотреть логи контейнера
`docker logs container_name_or_ID`

Cмотреть логи контейнера в реальном времени

`docker logs --follow container_name_or_ID`

Запустить bash в контейнере
`docker exec -i -t CONTAINER_NAME bash`

`docker exec –it <имя контейнера> /bin/bash`

Запустить SQL в контейнере в 

`docker exec -i -t CONTAINER_NAME psql -U postgres`

Сделать dump БД из контейнера с PostgreSQL

`sudo docker exec -t CONTAINER_ID pg_dump -U username database > sweet_cash_dump.sql`

Рестарт всех контейнеров

`docker restart $(docker ps -q)`

Выход из контейнера

Ctrl+p затем Ctrl+q

Информация о контейнере

`sudo docker container inspect container_name_or_ID`

### Создание сети между контейнерами

Создание сети между контейнерами

`docker network create network_name`

Просмотр сети между контейнерами

`docker network inspect network_name`

Добавление контейнеров в сеть

`docker network connect network_name container_name_or_ID`

**Подключение к контейнеру**

`docker container attach container_name_or_ID`

**Копирование файла из контейнера на локальную машину**

`docker cp container-id:/code/logs.log ~/logs.log`

**Просмотр трафика к контейнеру**

`sudo tcpdump -i any -s 0 -l -w - port 5000 | strings`

где `5000` - порт контейнера

`docker run --name some-postgres -p 5000:5000 -e POSTGRES_PASSWORD=911911 -d postgres`