# Outline VPN

[https://github.com/Jigsaw-Code/outline-server](https://github.com/Jigsaw-Code/outline-server)

[https://github.com/Jigsaw-Code/outline-ss-server](https://github.com/Jigsaw-Code/outline-ss-server)

[https://gist.github.com/JohnyDeath/3f93899dc78f90cc57ae52b41ea29bac](https://gist.github.com/JohnyDeath/3f93899dc78f90cc57ae52b41ea29bac)

[https://github.com/Jigsaw-Code/outline-server/blob/master/src/server_manager/install_scripts/install_server.sh](https://github.com/Jigsaw-Code/outline-server/blob/master/src/server_manager/install_scripts/install_server.sh)

[https://ipv6.rs/tutorial/OpenSUSE_Latest/Outline_Server/](https://ipv6.rs/tutorial/OpenSUSE_Latest/Outline_Server/)

# Установка Outline VPN на Ubuntu 20.04

Outline VPN - это бесплатный инструмент с открытым исходным кодом, позволяющий развернуть собственную VPN на Вашем собственном сервере или на машине облачного провайдера. Подробную информацию Вы можете узнать [здесь](https://getoutline.org/ru/) и [здесь](https://en.wikipedia.org/wiki/Outline_VPN).

В своем составе имеет как графические инструменты, так и средства работы через командную строку. Позволяет использовать VPN как на настольных компьютерах, так и на мобильных устройствах.

## Прежде чем начать

Вам нужен сервер. Да, его нужно арендовать, учитывая его местоположение. Например, если Вам нужно получать доступ к ресурсам, которые недоступны в текущем местоположении, но доступны, например, в Канаде, то смело арендуйте виртуальную машину в AWS, Digital Ocean или любом другом месте.

Для простых задач, например открытие сайтов, обмена текстовыми сообщениями в мессенджерах и т.д., подойдет хост с минимальными ресурсами:

- 1 ядро CPU.
- 1 ГБ RAM (можно и меньше).
- 10 GB HDD для файлов ОС в основном.

Стоимость аренды такого сервера от 3$ до 5$ в месяц, плюс-минус. По необходимости ресурсов можно добавлять поболее. Операционная система - Ubuntu 20.04, т.к. инструкция именно для нее.

Как арендовать виртуальную машину тут рассматривать не будем, все зависит от провайдера.

## Начальная настройка сервера

И так, виртуальная машина арендована, доступ к ней по SSH имеется, Ubuntu установлена. Далее устанавливаем последние обновления.

`sudo apt update`

`sudo apt upgrade`

Сделайте перезагрузку машины после этого, если есть необходимость после установки обновлений.

Сразу настроим брэндмауэр, чтобы защитить машину от несанкционированного доступа.

`sudo ufw allow 443/tcp`

`sudo ufw allow 8080/tcp`

Открываем доступ через SSH.

`sudo ufw allow 22/tcp`

Если у Вас статический IP, то для безопасности доступ по SSH можно разрешить только для него.

`sudo ufw allow from <ВашПостоянныйIP> to any port 22`

+

As the script may say,

> If you have connection problems, it may be that your router or cloud provider
blocks inbound connections, even though your machine seems to allow them.
> 
> - If you plan to have a single access key to access your server make sure
> ports 41429 and are open for TCP and UDP on
> your router or cloud provider.
> - If you plan on adding additional access keys, you’ll have to open ports
> 1024 through 65535 on your router or cloud provider since the Outline
> Server may allocate any of those ports to new access keys.

So, You may need to allow connections by

`sudo ufw allow 1024:65535/tcp`

`sudo ufw allow 1024:65535/udp` (Под вопросом)

И включаем брэндмауэр.

`sudo ufw enable`

Отлично! Машина защищена. Идем дальше.

## Установка Outline Server

Для установки воспользуемся готовыми скриптами из проекта [outline-server](https://github.com/Jigsaw-Code/outline-server) компании Jigsaw.

Скрипт находится по адресу:

```
https://github.com/Jigsaw-Code/outline-server/blob/master/src/server_manager/install_scripts/install_server.sh
```

Для установки достаточно выполнить следующую команду.

<aside>
💡 Обязательно от пользователями с правами на docker. У меня это root

</aside>

`sudo wget -qO- https://raw.githubusercontent.com/Jigsaw-Code/outline-server/master/src/server_manager/install_scripts/install_server.sh | bash`

Будет установлен Docker и службы самого Outline, а также все зависимости. При необходимости Вы можете установить Docker самостоятельно перед запуском скрипта.

`sudo curl https://get.docker.com | sh`

Когда скрипт закончит, то выведет примерно такое содержимое.

```json
{
  "apiUrl": "https://0.0.0.0:0000/XXXXXXXXXXXX",
  "certSha256": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

Сохраните это себе на будущее. По факту сервер Outline VPN уже установлен и нам лишь нужно его настроить для своих нужд.

## Клиент для управления сервером

Управление серверном VPN, в т.ч. раздача доступов, осуществляется с помощью [Outline Manager](https://getoutline.org/ru/get-started/#step-1), доступной для Windows, Max и Linux.

При запуске нужно добавить сервер и выбрать "Настроить Outline где угодно". Появится инструкция по установке с помощью скрипта, который мы ранее запускали. А после поле для ввода ключа и адреса, который Вы до этого сохранили.

После этого у Вас появится доступ к управлению сервером.

## Добавляем ключ

В Outline Manager добавляем новый ключ в управлении сервером. Программа покажет [ссылку на инструкцию](https://github.com/Jigsaw-Code/outline-client/blob/master/docs/invitation-instructions.md) и сам ключ в виде строки:

`ss://XXXXXXXXXXXX@9.9.9.9:0/?outline=1`

Скопируйте этот ключ, он понадобиться при запуске клиента Outline.

## Клиент для подключения

И последний шаг - установка [клиента для подключения](https://getoutline.org/ru/get-started/#step-3). Есть приложения для Android, Windows, Chrome, iOS, MacOS, Linux.

При первом запуске нужно нажать "Добавить сервер" и вставить полученный выше ключ.

Готово!