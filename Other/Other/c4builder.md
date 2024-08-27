# c4builder

❗ [https://structurizr.com/](https://structurizr.com/)

[https://adrianvlupu.github.io/C4-Builder/#/?id=overview](https://adrianvlupu.github.io/C4-Builder/#/?id=overview)

Install npm on Mac [https://treehouse.github.io/installation-guides/mac/node-mac.html](https://treehouse.github.io/installation-guides/mac/node-mac.html)

Install c4builder Install [https://adrianvlupu.github.io/C4-Builder/#/?id=overview](https://adrianvlupu.github.io/C4-Builder/#/?id=overview) `npm i -g c4builder`

# **Локально**

Установка на Ubuntu:

```bash
Install Java
sudo apt install default-jre
sudo apt install default-jdk

Install Node.js (https://github.com/nodesource/distributions/blob/master/README.md)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - &&\
sudo apt-get install -y nodejs

Install GraphViz
sudo apt install graphviz

Install c4builder
sudo npm i -g c4builder
```

1. Переход в каталог проекта
2. Запуск `c4builder site`
    
    ```
    c4builder --help
    
    Options:
      -V, --version   output the version number
      new             create a new project from template
      config          change configuration for the current directory
      list            display the current configuration
      reset           clear all configuration
      site            serve the generated site
      -w, --watch     watch for changes and rebuild
      docs            a brief explanation for the available configuration options
      -p, --port <n>  port used for serving the generated site
      -h, --help      output usage information
    ```
    
3. Настройки:
    - ? **Project Name** arch
    - ? **HomePage Name** Overview
    - ? **Root documentation folder** src
    - ? **Destination folder** docs
    - ? **Compilation format:** Generate website
    - ? **Change the default docsify theme?** //unpkg.com/docsify/lib/themes/vue.css
    - ? **Support search on navbar?** true
    - ? **Include a repository url?**
    - ? **Path to a specific Docsify template?**
    - ? **Change the default serve port?** 3000
    - ? **PlantUML version:** latest (compatible with plantuml online server)
    - ? **Compilation format:** Include breadcrumbs, Place diagrams before text, Embed SVG Diagram, Generate diagram images locally
    - ? **PlantUML Server URL** https://www.plantuml.com/plantuml
    - ? **Diagram Image Format** svg
    - ? **Change the default charset** UTF-8
4. Переход [http://localhost:3000/](http://localhost:3000/)

**Настройка nginx**

sudo nano /etc/nginx/sites-available/app_name

```bash
server {
                listen 80;
                server_name ip_or_domain;

                location /c4/ {
                        proxy_pass  http://127.0.0.1:3000/;
												// proxy_pass  http://0.0.0.0:5001/; // for docker
                }
        }
```

# Docker

**Структура репозитория:**

project_dir

src

pumls

mds

other dirs

.c4builder

Docerfile

**Dockerfile** (на основе [https://github.com/adrianvlupu/C4-Builder/blob/master/Dockerfile](https://github.com/adrianvlupu/C4-Builder/blob/master/Dockerfile))

```bash
FROM openjdk:11

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get update && apt-get install -y nodejs graphviz chromium xvfb

RUN npm i -g c4builder

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root

# Copy local directory to workdir
COPY ./project_dir.
    
# ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
#     PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium.sh

CMD /bin/bash -c "c4builder site"
```

**Порядок действий**

1. Скчать репозиторий на локальную машину
2. Перейти в каталог проекта
3. Запуститьв `c4builder site`
4. В итоге создадуться файл конфигурации .c4builder и директория /docs
Пример .c4builder:
    
    ```json
    {
    	"projectName": "c4_sample",
    	"homepageName": "Overview",
    	"rootFolder": "src",
    	"distFolder": "docs",
    	"generateMD": false,
    	"generatePDF": false,
    	"generateCompleteMD": false,
    	"generateCompletePDF": false,
    	"generateWEB": true,
    	"webTheme": "//unpkg.com/docsify/lib/themes/vue.css",
    	"supportSearch": true,
    	"repoUrl": "",
    	"docsifyTemplate": "",
    	"webPort": "5001",
    	"plantumlVersion": "latest",
    	"includeBreadcrumbs": true,
    	"includeLinkToDiagram": false,
    	"diagramsOnTop": true,
    	"embedDiagram": true,
    	"excludeOtherFiles": false,
    	"generateLocalImages": true,
    	"plantumlServerUrl": "https://www.plantuml.com/plantuml",
    	"diagramFormat": "svg",
    	"charset": "UTF-8",
    	"hasRun": true,
    	"checksums": [
    		"18463badf26acc0184d1fcaab3457d3ddb5ba54bf5c913229f0ebf9856e98559"
    	]
    }
    ```
    
5. Удалить директорию /docs
6. Внести изменения в репозиторий
7. На удаленной машине скачать резиторий
8. Создать образ `sudo docker build -t image_name`
9. Запустить контейнер `sudo docker run --name container_name -d --rm -p 5001:5001 image_name`