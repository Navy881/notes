# Linux terminal command

`sudo apt**-**get clean`

Команда очищает локальный репозиторий от извлеченных файлов пакетов, оставшихся в каталоге `/var/cache`. 

`sudo apt**-**get autoclean`

Команда очищает локальный репозиторий от извлеченных файлов пакетов, но удаляет только те файлы, которые больше не могут быть загружены и практически бесполезны. 

`sudo apt**-**get autoremove`

Параметр удаляет пакеты, которые были установлены автоматически, поскольку они требовались для некоторых других пакетов, но после удаления этих пакетов они больше не нужны. 

Копирование файла

`cp file.doc newfile.doc`