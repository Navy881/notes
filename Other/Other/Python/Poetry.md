# Poetry

[https://python-poetry.org/](https://python-poetry.org/)

[https://python-poetry.org/docs/cli/](https://python-poetry.org/docs/cli/)

[https://habr.com/ru/articles/593529/](https://habr.com/ru/articles/593529/)

Poetry - это инструмент для управления зависимостями в Python проектах (аналог встроенного pip). Идея реализации данного инструмента пришла его создателю в связи с тем, что различные способы менеджмента пакетов (requirements.txt, setup.cfg, MANIFEST.ini и другие) показались создателю Poetry не очень-то удобными.

В poetry нет необходимости активировать виртуальное окружение, достаточно лишь зайти в папку с проектом и начинать пользоваться командами. Poetry сам найдет нужное окружение. Также в poetry можно менять версию python без необходимости менять старое виртуальное окружение.

## **Установка**

Установить poetry на windows можно либо при помощи pip:

```
pip install poetry
```

Либо более гибким вариантом через powershell:

```
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

## **pyproject.toml**

Главный файл для poetry - это pyproject.toml. Все данные о проекты должны быть записаны в нём. При установке пакетов poetry берёт данные из этого файла и формирует файл с зависимостями poetry.lock (если уже есть готовый файл poetry.lock, то данные будут браться из него). Toml файл состоит из нескольких блоков, каждый из которых имеет свои особенности, рассмотрим данные блоки:

**[tool.poetry]** - содержит основную информацию о проекте, такую как:

- name - имя проекта
- version - версия проекта
- description - описание проекта
- license - лицензия проекта
- authors - список авторов проекта в формате name <email>
- maintainers - список менторов проекта формате name <email>
- readme - readme файл проекта в формате README.rst или README.md
- homepage - URL сайта проекта
- repository - URL репозитория проекта
- documentation- URL документации проекта
- keywords - список ключевых слов проекта (макс: 5)
- classifier - список PyPI классификаторов
- packages = [{include = "a_project"}]
    
    <aside>
    💡 Убрать, иначе не будет работать с Docker.
    Будет ошибка `...does not contain any element`.
    
    </aside>
    

**[tool.poetry.dependencies]** - содержит описание всех зависимостей проекта. Каждая зависимость должна иметь название с указанием версии, также присутствует возможность скачать проекта с github с указанием ветки/версии/тэга, например:

- requests = "^2.26.0"
- requests = { git = "[https://github.com/requests/requests.git"](https://github.com/requests/requests.git%22) }
- requests = { git = "[https://github.com/kennethreitz/requests.git"](https://github.com/kennethreitz/requests.git%22), branch = "next" }
- numpy = { git = "[https://github.com/numpy/numpy.git"](https://github.com/numpy/numpy.git%22), tag = "v0.13.2" }

**[tool.poetry.scripts]** - в данном разделе можно описать различные сценарии или скрипты, которые будут выполняться при установке пакетов или при запуске приложения. Например:

- poetry = 'poetry.console:run'
- main-run = 'new_proj.main:run' (после чего достаточно запустить `poetry main-run` и будет выполнен запуск функции run в файле new_prof/main.py)

**[tool.poetry.extras]** - в данном блоке описываются группы зависимостей, которые можно устанавливать отдельно:

```toml
[tool.poetry.dependencies]
psycopg2 = { version = "^2.7", optional = true }
pymysql = { version = "1.0.2", optional = true }
[tool.poetry.extras]
mysql = ["pymysql"]
pgsql = ["psycopg2"]
```

Далее зависимости можно установить двумя способами:

```
poetry install --extras "mysql pgsql"
poetry install -E mysql -E pgsql
```

**[tool.poetry.urls]** - помимо основных URL, указанных в [tool.poetry], можно указывать свои URL:

- "Bug Tracker" = "[https://github.com/python-poetry/poetry/issues"](https://github.com/python-poetry/poetry/issues%22)

Пример данных в pyproject.toml

```toml
[tool.poetry]
name = "new_proj"
version = "0.1.0"
description = "My description"
authors = ["Daniil Gorbenko <dani.gorbenko@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.10"
pygame = "^2.1.0"
icecream = "^2.1.1"
requests = "^2.26.0"
psycopg2 = { version = "^2.7", optional = true }
pymysql = { version = "1.0.2", optional = true }

[tool.poetry.dev-dependencies]
Pympler = "^0.9"

[tool.poetry.urls]
"Bug Tracker" = "https://github.com/python-poetry/poetry/issues"

[tool.poetry.scripts]
run-main = "new_proj.main:main_def"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

## **Основные методы**

### new

Чтобы создать новый проект с помощью Poetry, достаточно выполнить **poetry new <название папки с проектом>**. После чего создастся папка с названием вашего проекта, в этой папке будет лежать файл pyproject.toml.

```bash
poetry new new_project
```

### init

Чтобы сделать пакетным менеджером poetry в уже имеющемся проекте, достаточно выполнить:

```
poetry init
```

Далее будет предложено заполнить немного основной информации о проекте.

Метод может принимать некоторые необязательные параметры:

- -name: имя проекта
- -description: описание проекта
- -author: имя автора
- -python: совместимые версии Python
- -dependency: требуемый пакет с версией пакета
- -dev-dependency: требования к разработке

После чего в проекте появится файл pyproject.toml, в котором вручную можно изменить любые данные.

### install

Чтобы установить зависимости проекта достаточно выполнить команду:

```
poetry install
```

Poetry считывает данные из pyproject.toml, строит дерево зависимостей проекта, разрешая проблемы с версиями зависимостей, и устанавливает все пакеты. Однако, если в проекте уже есть файл poetry.lock, то будут использоваться точные версии из этого файла.

Метод может принимать параметры:

- -remove-untracked: удалит старые пакеты, которые больше не используются в проекте
- -no-dev: dev пакеты не будут устанавливаться

### update

Чтобы обновить версии зависимостей (тем самым обновив файл poetry.lock) достаточно выполнить:

```
poetry update
```

Также есть возможность обновить лишь определенные пакеты:

```
poetry update icecream pygame
```

Метод может принимать дополнительные параметры:

- -no-dev : игнорирует обновление dev пакетов
- -lock : не устанавливает и не обновляет пакеты, а только обновляет файл poetry.lock

### add

Чтобы добавить новую библиотеку достаточно выполнить:

```
poetry add pygame
```

Можно указывать версию пакета:

```
poetry add "pygame>=2"
poetry add pygame@^2
poetry add git+https://github.com/aiogram/aiogram.git@dev-3.x
```

Можно передать параметры:

- -dev (-D): установит пакет в качестве dev зависимости
- -path: путь к пакету (если пакет лежит локально)
- -lock : не устанавливает зависимости, а только обновляет файл poetry.lock

### remove

Чтобы удалить зависимость достаточно выполнить:

```
poetry remove pygame
```

Дополнительно можно передать параметры:

- -dev : удалит пакет из dev зависимостей

### show

Чтобы посмотреть зависимости проекта достаточно выполнить:

```
poetry show
```

Если необходимо посмотреть информацию о конкретном пакете:

```
poetry show pygame
```

Посмотреть дерево зависимостей проекта можно при помощи:

```
poetry show --tree
```

Также можно передать параметры:

- -tree: список зависимостей в виде дерева
- -latest (-l): показать последние версии проектов
- -outdated (-o): показать последние версии только для устаревших пакетов

### run

Чтобы запустить проект достаточно выполнить:

```
poetry run python <имя python файла>
poetry run python main.py
poetry run <имя скрипта, описанного в [tool.poetry.scripts]>
poetry run main-run
```

### shell

Команда запустит виртуальную среду и покажет путь к ней.

```toml
poetry shell

> Spawning shell within C:\Users\User\AppData\Local\pypoetry\Cache\virtualenvs\aiogram-bot-G2yQvqY1-py3.8
> PowerShell 7.3.6
```

### env

Команда для переключения версии Python для Poetry.

```java
poetry env use python3.9
```

## Версии зависимостей

При установке пакета можно указать точную версию проекта, например:

```toml
[tool.poetry.dependencies]
pygame = "2.1.0"
```

Но иногда есть необходимость указать диапазон версий пакета, чтобы получать обновления, в таком случае есть несколько способов указать диапазон:

```toml
[tool.poetry.dependencies]
pygame = "^2.1"
pygame = "~2.1"
pygame = "2.1.*"
pygame = "*"
```

Вот какие диапазоны принимают данные префиксы версий:

| Зависимость | Минимальная версия | Максимальная версия |
| --- | --- | --- |
| ^1.2.3 | >=1.2.3 | <2.0.0 |
| ^1.2 | >=1.2.0 | <2.0.0 |
| ^1 | >=1.0.0 | <2.0.0 |
| ^0.2.3 | >=0.0.3 | <0.0.4 |
| ~1.2.3 | >=1.2.3 | <1.3.0 |
| ~1.2 | >=1.2.0 | <1.3.0 |
| ~1 | >=1.0.0 | <2.0.0 |
| * | >=0.0.0 | - |
| 1.* | >=1.0.0 | <2.0.0 |
| 1.2.* | >=1.2.0 | <1.3.0 |