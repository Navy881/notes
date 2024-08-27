# OpenVPN

https://serverspace.ru/support/help/openvpn-ubuntu-20-04/

## Установим и настроим OpenVPN

Для установки и последующей настройки пакетов, требуемых при запуске OpenVPN, будет использован соответствующий скрипт. Вам следует предоставить ему корректный IP-адрес сервера.

Загрузим данный скрипт:

`wget https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh`

Далее необходимо сделать его исполняемым:

`chmod +x openvpn-install.sh`

А затем запустить:

`./openvpn-install.sh`

Некоторые из параметров по умолчанию оптимальны – просто подтвердите их. Единственное, что требует проверки и возможного редактирования – публичный IP. Остальное редактируйте только в случае знания и понимания желаемого варианта установки.

![https://serverspace.io/wp-content/uploads/2020/12/wxonk1x-600x475.png](https://serverspace.io/wp-content/uploads/2020/12/wxonk1x-600x475.png)

Последним шагом укажите имя клиента и сделайте выбор – необходим ли пароль для защиты конфигурации или нет. Из соображений безопасности  рекомендуем установить его.

После завершения процесса сделаем проверку – прослушиваются ли входящие подключения.

`ss -tupln | grep openvpn`

![https://serverspace.io/wp-content/uploads/2020/12/pcdijfh.png](https://serverspace.io/wp-content/uploads/2020/12/pcdijfh.png)

## Добавление и удаление клиентов

Для добавления / удаления клиентов, а также удаления OpenVPN необходимо вновь запустить скрипт и выбрать подходящий вариант.

`./openvpn-install.sh`

Результат:

![https://serverspace.ru/wp-content/uploads/2021/05/5258977f45.jpg](https://serverspace.ru/wp-content/uploads/2021/05/5258977f45.jpg)

![Untitled](OpenVPN/Untitled.webp)

## Подключим клиент

Для отображения процесса подключения клиента отлично подойдет альтернативная машина Ubuntu. Аналогично можно настроить и другие Linux-системы или же загрузить Windows: [https://openvpn.net/community-downloads/](https://openvpn.net/community-downloads/)

![https://serverspace.ru/wp-content/uploads/2021/05/98b8536922.jpg](https://serverspace.ru/wp-content/uploads/2021/05/98b8536922.jpg)