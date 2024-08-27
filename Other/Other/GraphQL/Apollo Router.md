# Apollo Router

# Локальное разворачивание

1. Зависимости (нужно установить)
    1. rust (> `1.72`)
    2. [protoc](https://grpc.io/docs/protoc-installation/)
    3. [cmake](https://cmake.org/).
2. Перезапустить терминал
3. Клонировать репозиторий https://github.com/apollographql/router
4. Перейти в проект `cd router`
5. Далее по инструкции [https://github.com/apollographql/router/blob/HEAD/DEVELOPMENT.md](https://github.com/apollographql/router/blob/HEAD/DEVELOPMENT.md)
    1. Настройка githooks `git config --local core.hooksPath .githooks/`
    2. Сборка проекта `cargo build --all-targets`
    3. Запуск внешних сервисов, таких как Jaeger и Redis.
        1. Запустить Docker
        2. `docker-compose up -d`
    4. Запустить Apollo Router `cargo run -- --dev -s ./examples/graphql/supergraph.graphql -c apollo-router/router.yaml`
        
        <aside>
        💡 Запуск Apollo Router с флагом `--dev` включает режим разработки, который открывает Apollo Sandbox, чтобы вы могли выполнять запросы к Apollo Router.
        
        </aside>
        

# Добавление плагина

[https://www.apollographql.com/docs/router/customizations/native/](https://www.apollographql.com/docs/router/customizations/native/)

1. В plugins/ создается файл с кодом плагина plugin_name.rs
2. Для объявления плагина в файл plugins/mod.rs  добавляется `mod plugin_name;`
3. В router.yaml добавляется конфигурация плагина 
    
    ```yaml
    plugins:
      router.validation:  # Название группы плагина и самого плагина
        no: config  # apollo have an error if there is no config :(
      router.hello_world:
        name: "Biba"  # Значение для настройки конфигурации плагина
    ```
    
4. Пересобрать проект

# Добавление rhai-скрипта

[https://www.apollographql.com/docs/router/customizations/rhai/](https://www.apollographql.com/docs/router/customizations/rhai/)

[https://www.apollographql.com/docs/router/customizations/rhai-api/](https://www.apollographql.com/docs/router/customizations/rhai-api/)

1. В plugins/rhai/scripts создается файл с кодом плагина rhai_module.rhai
2. Добавления вызова функций скрипта в main.rhai
3. В router.yaml добавляется конфигурация плагина 
    
    ```yaml
    rhai:
      scripts: apollo-router/src/plugins/rhai/scripts
      main: main.rhai
    ```
    
4. Пересобрать проект