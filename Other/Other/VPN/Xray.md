# Xray

https://github.com/XTLS/Xray-core?tab=readme-ov-file

[https://habr.com/ru/articles/731608/](https://habr.com/ru/articles/731608/)

https://github.com/EvgenyNerush/easy-xray/blob/main/README.ru.md

# Project X

[https://xtls.github.io/ru/document/](https://xtls.github.io/ru/document/)

https://xtls.github.io/en/document/install.html#install-script



# 1. Обеспечение безопастности сервера
	- Изменение порта SSH
	- Создание нового пользователя (u1)
	- Запрет удалённого подключения по SSH для пользователя root
	- Настройка аутентификации по SSH-ключам и запрет аутентификации по паролю

# 2. Настройка nginx на VPS
	Добавляем новый сервер, который будет прослушивать локальный порт и отдавать файлы сайта:
	```json
	server {
		listen 127.0.0.1:8081;
		root /home/u1/www/webpage;
		index index.html;
		add_header Strict-Transport-Security "max-age=63072000" always;
	}
	```

# 3. Получение SSL-сертификата

	## 3.1. Установка acme.sh
	Запустите скрипт установки:
	`wget -O -  https://get.acme.sh | sh`

	Сделайте команду acme.sh доступной:
	`. .bashrc`

	Включите автоматическое обновление acme.sh:
	`acme.sh --upgrade --auto-upgrade`

	## 3.2. Тестовый запрос сертификата
	`acme.sh --issue --server https://acme-staging-v02.api.letsencrypt.org/directory -d bsikpg.duckdns.org -w /usr/share/nginx/html --keylength ec-256 --debug`


	## 3.3. Запрос настоящего сертификата
	Дать доступ для пользователя u1 на запись /usr/share/nginx/html/.well-known/acme-challenge/
	`sudo chown -R u1:u1 /usr/share/nginx/html/.well-known/acme-challenge/`
	
	`acme.sh --set-default-ca --server letsencrypt`
	`acme.sh --issue -d bsikpg.duckdns.org -w /usr/share/nginx/html --keylength ec-256 --force`
	
	## 3.4. Установка сертификата
	Дать пользователю доступ на запись в /etc/letsencrypt/acme/bsikpg.duckdns.org/
	`sudo chown -R u1:u1 /etc/letsencrypt/acme/bsikpg.duckdns.org/`
	
	`acme.sh --installcert -d bsikpg.duckdns.org  --cert-file /etc/letsencrypt/acme/bsikpg.duckdns.org/cert.crt --key-file /etc/letsencrypt/acme/bsikpg.duckdns.org/cert.key --fullchain-file /etc/letsencrypt/acme/bsikpg.duckdns.org/fullchain.crt --ecc`
	
# 4. Настройка Xray на сервере
	[https://xtls.github.io/ru/document/level-0/ch07-xray-server.html](https://xtls.github.io/ru/document/level-0/ch07-xray-server.html)


	## 4.1. Установка Xray
	Скачиваем установочный скрипт:
	`wget https://github.com/XTLS/Xray-install/raw/main/install-release.sh`

	Запускаем установку:
	`sudo bash install-release.sh`

	После завершения установки удаляем скрипт:
	`rm ~/install-release.sh`

	## 4.2. Установка TLS-сертификата для Xray
	Чтобы избежать проблем с правами доступа при работе от имени непривилегированного пользователя, создадим папку для сертификатов в домашней директории пользователя vpsadmin:
	`mkdir ~/xray_cert`

	Используем команду --install-cert из acme.sh для установки (копирования) файлов сертификата:
	```
	acme.sh --install-cert -d bsikpg.duckdns.org --ecc \
           --fullchain-file ~/xray_cert/xray.crt \
           --key-file ~/xray_cert/xray.key
	```

	По умолчанию файл xray.key недоступен для чтения другим пользователям, поэтому нужно выдать права на чтение:
	`chmod +r ~/xray_cert/xray.key`

	Создаём файл скрипта (xray-cert-renew.sh):
	`nano ~/xray_cert/xray-cert-renew.sh`
	
	Копируем в него следующий код, заменив sub.yourdomain.com на своё доменное имя, и сохраняем файл:
	```
	#!/bin/bash

	/home/u1/.acme.sh/acme.sh --install-cert -d bsikpg.duckdns.org --ecc --fullchain-file /home/u1/xray_cert/xray.crt --key-file /home/u1/xray_cert/xray.key
	echo "Xray Certificates Renewed"

	chmod +r /home/u1/xray_cert/xray.key
	echo "Read Permission Granted for Private Key"

	sudo systemctl restart xray
	echo "Xray Restarted"
	```

	Делаем скрипт исполняемым:
	`chmod +x ~/xray_cert/xray-cert-renew.sh`

	Запускаем crontab -e, чтобы добавить задание на автоматическое выполнение xray-cert-renew.sh каждый месяц (не используйте sudo, так как мы добавляем задание для пользователя vpsadmin.):
	`crontab -e`

	Добавляем следующую строку в конец файла и сохраняем его:
	```
	# 1:00am, 1st day each month, run `xray-cert-renew.sh`
	0 1 1 * *   bash /home/u1/xray_cert/xray-cert-renew.sh
	```
	
	# 4.3. Настройка Xray
	Генерируем валидный UUID и сохраняем его:
	`xray uuid`
	
	Создаём папку для логов в домашней директории пользователя u1:
	`mkdir ~/xray_log`

	Создаём два файла для логов (логи доступа и логи ошибок):
	`touch ~/xray_log/access.log && touch ~/xray_log/error.log`
	
	По умолчанию Xray запускается от имени пользователя nobody, поэтому нужно дать другим пользователям права на запись в файлы логов:
	`chmod a+w ~/xray_log/*.log`

	Создаём файл конфигурации Xray с помощью nano:
	`sudo nano /usr/local/etc/xray/config.json`

	Копируем в него следующий код и вставляем сгенерированный ранее UUID в строку 61: "id": "".
	```json
	// ССЫЛКИ:
	// https://github.com/XTLS/Xray-examples
	// https://xtls.github.io/config/
	// Типичный конфигурационный файл, как для сервера, так и для клиента, состоит из 5 основных частей. Разберём их по полочкам:
	// ┌─ 1_log Настройки логирования - что и куда писать в лог (чтобы было проще искать ошибки)
	// ├─ 2_dns Настройки DNS - как выполнять DNS-запросы (защита от DNS-спуфинга, защита от слежки, предотвращение маршрутизации трафика на китайские серверы и т. д.)
	// ├─ 3_routing Настройки маршрутизации - как обрабатывать трафик (фильтрация рекламы, разделение трафика для разных стран)
	// ├─ 4_inbounds Настройки входящих подключений - какой трафик может поступать на Xray
	// └─ 5_outbounds Настройки исходящих подключений - куда направлять трафик, исходящий от Xray
	{
	  // 1_Настройки логирования
	  "log": {
		"loglevel": "warning", // Уровень детализации логов: "none", "error", "warning", "info", "debug" (от меньшего к большему)
		"access": "/home/u1/xray_log/access.log", // Файл для записи логов доступа
		"error": "/home/u1/xray_log/error.log" // Файл для записи логов ошибок
	  },
	  // 2_Настройки DNS
	  "dns": {
		"servers": [
		  "https+local://1.1.1.1/dns-query", // Используем DoH-сервер 1.1.1.1 в первую очередь. Это снижает скорость, но защищает от слежки со стороны интернет-провайдера
		  "localhost"
		]
	  },
	  // 3_Настройки маршрутизации
	  "routing": {
		"domainStrategy": "IPIfNonMatch",
		"rules": [
		  // 3.1 Предотвращение проблем с локальной маршрутизацией: атаки на внутреннюю сеть, неправильная обработка локальных адресов и т. д.
		  {
			"type": "field",
			"ip": [
			  "geoip:private" // Условие: адреса из списка "private" в файле geoip (локальные адреса)
			],
			"outboundTag": "block" // Действие: отправить трафик на исходящее подключение "block" (блокировка)
		  },
		  {
			// 3.2 Предотвращение прямого подключения к китайским серверам
			"type": "field",
			"ip": ["geoip:cn"],
			"outboundTag": "block"
		  },
		  // 3.3 Блокировка рекламы
		  {
			"type": "field",
			"domain": [
			  "geosite:category-ads-all" // Условие: домены из списка "category-ads-all" в файле geosite (рекламные домены)
			],
			"outboundTag": "block" // Действие: отправить трафик на исходящее подключение "block" (блокировка)
		  }
		]
	  },
	  // 4_Настройки входящих подключений
	  // 4.1 Здесь указан только один простейший входящий прокси-сервер vless+xtls, так как это самый производительный режим Xray. При необходимости вы можете добавить другие прокси-серверы, используя этот шаблон.
	  "inbounds": [
		{
		  "port": 8443,  // Отдельный порт, т.к. 443 занят nginx 
		  "protocol": "vless",
		  "settings": {
			"clients": [
			  {
				"id": "", // Укажите свой UUID
				"flow": "xtls-rprx-vision",
				"level": 0,
				"email": "u1@yourdomain.com"
			  }
			],
			"decryption": "none",
			"fallbacks": [
			  {
				"dest": 8081 // Перенаправлять на порт 8081 по умолчанию
			  }
			]
		  },
		  "streamSettings": {
			"network": "tcp",
			"security": "tls",
			"tlsSettings": {
			  "alpn": "http/1.1",
			  "certificates": [
				{
				  "certificateFile": "/home/u1/xray_cert/xray.crt",
				  "keyFile": "/home/u1/xray_cert/xray.key"
				}
			  ]
			}
		  }
		}
	  ],
	  // 5_Настройки исходящих подключений
	  "outbounds": [
		// 5.1 Первое исходящее подключение - это правило по умолчанию. freedom - это прямое подключение (VPS и так находится во внешней сети)
		{
		  "tag": "direct",
		  "protocol": "freedom"
		},
		// 5.2 Правило блокировки. Протокол blackhole отправляет трафик в никуда (блокирует его)
		{
		  "tag": "block",
		  "protocol": "blackhole"
		}
	  ]
	}
	```
	
	## 4.4. Запуск Xray
	`sudo systemctl start xray`

	Для проверки состояния сервиса используем следующую команду:
	`sudo systemctl status xray`


	## 4.5. Docker
	[https://hub.docker.com/r/teddysun/xray](https://hub.docker.com/r/teddysun/xray)
	`docker pull teddysun/xray`

	Для Linux
	`docker run -d -p 9000:9000 --name xray --restart=always -v /etc/xray:/etc/xray teddysun/xray`

	Для Windows
	`docker run -d -p 9000:9000 --name xray --restart=always -v C:\Users\User\etc\xray:/etc/xray teddysun/xray`



# 4. Настройка Xray на клиенте
	[https://xtls.github.io/ru/document/level-0/ch08-xray-clients.html](https://xtls.github.io/ru/document/level-0/ch08-xray-clients.html)

	Скачайте последнюю версию xray-core для вашей платформы из [репозитория на GitHub](https://github.com/XTLS/Xray-core/releases) и распакуйте архив в удобное место.
	
	Создайте пустой файл конфигурации `config.json` в той же папке.
	[Справочник по конфигурации](https://xtls.github.io/ru/config/)
	```json
	// ССЫЛКИ:
	// https://github.com/XTLS/Xray-examples
	// https://xtls.github.io/config/

	// Типичный конфигурационный файл, как для сервера, так и для клиента, состоит из 5 основных частей. Разберём их по полочкам:
	// ┌─ 1_log          Настройки логирования - что и куда писать в лог (чтобы было проще искать ошибки)
	// ├─ 2_dns          Настройки DNS - как выполнять DNS-запросы (защита от DNS-спуфинга, защита от слежки, предотвращение маршрутизации трафика на китайские серверы и т. д.)
	// ├─ 3_routing      Настройки маршрутизации - как обрабатывать трафик (фильтрация рекламы, разделение трафика для разных стран)
	// ├─ 4_inbounds     Настройки входящих подключений - какой трафик может поступать на Xray
	// └─ 5_outbounds    Настройки исходящих подключений - куда направлять трафик, исходящий от Xray

	{
	  // 1_Настройки логирования
	  // В этом примере я закомментировал настройки файлов логов, потому что в Windows, macOS и Linux используются разные пути. Укажите свои пути.
	  "log": {
		// "access": "/home/local/xray_log/access.log",    // Файл для записи логов доступа
		// "error": "/home/local/xray_log/error.log",    // Файл для записи логов ошибок
		"loglevel": "warning" // Уровень детализации логов: "none", "error", "warning", "info", "debug" (от меньшего к большему)
	  },

	  // 2_Настройки DNS
	  "dns": {
		"servers": [
		  // 2.1 Запросы к зарубежным доменам отправляем на зарубежный DNS-сервер
		  {
			"address": "1.1.1.1",
			"domains": ["geosite:geolocation-!cn"]
		  },
		  // 2.4 Если все предыдущие DNS-серверы не ответили, используем локальный DNS-сервер
		  "localhost"
		]
	  },

	  // 3_Настройки маршрутизации
	  // Маршрутизация позволяет перенаправлять трафик, соответствующий определённым условиям, на определённое исходящее подключение (см. раздел 5).
	  "routing": {
		"domainStrategy": "IPIfNonMatch",
		"rules": [
		  // 3.1 Блокировка рекламных доменов
		  {
			"type": "field",
			"domain": ["geosite:category-ads-all"],
			"outboundTag": "block"
		  },
		  // 3.2 Прямое подключение для российских доменов
		  {
			"type": "field",
			"domain": [
			  "domain:ru",
			  "domain:рф",
			  "domain:su"
			],
			"outboundTag": "direct"
		  },
		  // 3.3 Проксирование трафика на зарубежные домены
		  {
			"type": "field",
			"domain": [
			  "domain:!ru",
			  "domain:!рф",
			  "domain:!su"
			],
			"outboundTag": "proxy"
		  }
		  // 3.6 Правило по умолчанию
		  // В Xray любой трафик, который не соответствует ни одному из правил маршрутизации, отправляется на первое исходящее подключение (см. раздел 5.1). Поэтому важно разместить настройки прокси-сервера на первом месте.сте.
		]
	  },

	  // 4_Настройки входящих подключений
	  "inbounds": [
		// 4.1 Обычно используется протокол SOCKS5 для локального перенаправления трафика
		{
		  "tag": "socks-in",
		  "protocol": "socks",
		  "listen": "127.0.0.1", // Адрес, на котором будет слушать SOCKS5-сервер
		  "port": 10800, // Порт, на котором будет слушать SOCKS5-сервер
		  "settings": {
			"udp": true
		  }
		},
		// 4.2 Некоторые приложения не поддерживают SOCKS. Для них можно использовать HTTP-прокси
		{
		  "tag": "http-in",
		  "protocol": "http",
		  "listen": "127.0.0.1", // Адрес, на котором будет слушать HTTP-сервер
		  "port": 10801 // Порт, на котором будет слушать HTTP-сервер
		}
	  ],

	  // 5_Настройки исходящих подключений
	  "outbounds": [
		// 5.1 Настройки прокси-сервера
		// Этот раздел должен быть первым, как уже было сказано в разделе 3.6. Все правила по умолчанию будут использовать эти настройки.
		{
		  "tag": "proxy",
		  "protocol": "vless",
		  "settings": {
			"vnext": [
			  {
				"address": "bsikpg.duckdns.org", // Замените на доменное имя вашего сервера
				"port": 8443,
				"users": [
				  {
					"id": "", // Должен совпадать с идентификатором на сервере
					"flow": "xtls-rprx-vision",
					"encryption": "none",
					"level": 0
				  }
				]
			  }
			]
		  },
		  "streamSettings": {
			"network": "tcp",
			"security": "tls",
			"tlsSettings": {
			  "serverName": "bsikpg.duckdns.org", // Замените на доменное имя вашего сервера
			  "allowInsecure": false, // Запретить использование недоверенных сертификатов
			  "fingerprint": "chrome" // Использовать uTLS для подмены отпечатка браузера Chrome / Firefox / Safari или случайный отпечаток
			}
			//"httpSettings": {
			//	"path": "/ray"  // Указываем путь /ray для маршрутизации через Nginx
			//}
		  }
		},
		// 5.2 Прямое подключение
		// Используется, если в настройках маршрутизации указан тег "direct"
		{
		  "tag": "direct",
		  "protocol": "freedom"
		},
		// 5.3 Блокировка трафика
		// Используется, если в настройках маршрутизации указан тег "block"
		{
		  "tag": "block",
		  "protocol": "blackhole"
		}
	  ]
	}
	```
	
	**Запуск**

	`.\xray.exe run -c config.json`

	**GUI клиент для Windows**
	[https://github.com/EvgenyNerush/easy-xray/blob/main/V2RayN.ru.md](https://github.com/EvgenyNerush/easy-xray/blob/main/V2RayN.ru.md)