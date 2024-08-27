# Nginx

### **Установка Nginx**

```c
	3.1. Установка веб-сервера Nginx
	# sudo apt update
	# sudo apt install nginx

	3.2. Настройка файрвола
	Перед тем, как начать проверять работу Nginx, нам необходимо настроить наш файрвол для разрешения доступа к сервису. При установки Nginx регистрируется в сервисе файрвола ufw. Поэтому настройка доступа осуществляется достаточно просто.

	Для вывода настроек доступа для приложений, зарегистрированных в ufw, введём команду:
    	# sudo ufw app list
	В результате выполнения этой команды будет выведен список профилей приложений:
	Вывод
	Available applications:
  		Nginx Full
  		Nginx HTTP
  		Nginx HTTPS
  		OpenSSH

	Рекомендуется настраивать ufw таким образом, чтобы разрешать только тот трафик, который вы хотите разрешить в явном виде. Поскольку мы ещё не настроили SSL для нашего сервера, в этой статье мы разрешим трафик только для порта 80.
	Сделать это можно следующей командой:
    	# sudo ufw allow 'Nginx HTTP'
    	# sudo ufw allow 'Nginx HTTPS' для HTTPS

	Вы можете проверить изменения введя команду:
	# sudo ufw status
	В результате должен отобразиться вывод следующего вида:
	Вывод
	Status: active

	To                         Action      From
	--                         ------      ----
	OpenSSH                    ALLOW       Anywhere                  
	Nginx HTTP                 ALLOW       Anywhere                  
	OpenSSH (v6)               ALLOW       Anywhere (v6)             
	Nginx HTTP (v6)            ALLOW       Anywhere (v6)

	3.3. Настройка SSL	
	Создание каталога ssl
	# sudo mkdir /etc/nginx/ssl
	
	Создание ключи и сертификата
	# sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt

	3.4. Проверка работы веб-сервера
	После завершения процесса установки Ubuntu 18.04 запустит Nginx автоматически. Таким образом веб-сервер уже должен быть запущен.
	Мы можем убедиться в этом выполнив следующую команду:
	# systemctl status nginx

	Для этого мы можем проверить, отображается ли веб-страница Nginx, доступная по умолчанию при вводе доменного имени или IP адреса сервера. Если вы не 		знаете публичного IP адреса сервера, вы можете найти этот IP адрес несколькими способами.

	Попробуйте набрать эту команду в терминале вашего сервера:
	# ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
	В результате будет выведено несколько IP адресов. Попробуйте вставить каждый из них в браузер.

	Другим способом определить свой IP адрес будет проверка, как ваш сервер виден из Интернета:
    	# curl -4 icanhazip.com
	Наберите полученный IP адрес или доменное имя в вашем веб-браузере.
	http://IP_адрес_вашего_сервера
	Вы должны увидеть страницу Nginx по умолчанию.

	3.4. Управление процессом Nginx
	Для остановки веб-сервера используйте команду:
    	# sudo systemctl stop nginx

	Для запуска остановленного веб-сервера наберите:
    	# sudo systemctl start nginx

	Для перезапуска веб-сервера можно использовать следующую команду:
    	# sudo systemctl restart nginx

	Если вы вносите изменения в конфигурацию Nginx, часто можно перезапустить его без закрытия соединений. Для этого можно использовать следующую команду:
    	# sudo systemctl reload nginx

	По умолчанию Nginx настроен на автоматический старт при запуске сервера. Если такое поведение веб-сервера вам не нужно, вы можете отключить его следующей командой:
    	# sudo systemctl disable nginx

	Для повторного включения запуска Nginx при старте сервера введите:
    	# sudo systemctl enable nginx

	Для проверки состояния запущенного Nginx введите:
    	# sudo systemctl status nginx
```

### Настройка Nginx

```c
# sudo nano /etc/nginx/sites-available/app_name
	
	Вставляем
	server {
    		listen 80;
    		server_name server_domain_or_IP;

    		location / {
        		include         uwsgi_params;
        		uwsgi_pass      0.0.0.0:5000;
    		}
	}
	
	server {
		listen          443 ssl;
		server_name     server_domain_or_IP;
		access_log      /var/log/nginx/example.com_access.log combined;
		error_log       /var/log/nginx/example.com_error.log error;

		ssl_certificate         /etc/nginx/ssl/nginx.crt;
		ssl_certificate_key     /etc/nginx/ssl/nginx.key;

		location / {
			include         uwsgi_params;
			uwsgi_pass      0.0.0.0:5000;

			proxy_set_header   Host              $http_host;
			proxy_set_header   X-Real-IP         $remote_addr;
			proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
		}

	}

	server_domain_or_IP - доименное имя сервера или IP
	uwsgi_pass - ip и порт uwsgi (0.0.0.0:5000) // старое описание: путь для socket из ini-файла для uwsgi в приложении

	Создаем ссылку
	# sudo ln -s /etc/nginx/sites-available/app_name /etc/nginx/sites-enabled
	
	Проверяем ошибки
	# sudo nginx -t
	# sudo service nginx configtest

	Перезагрузка Nginx
	# sudo service nginx restart
```

### SSL

[SSL сертификат](Nginx/SSL%20%D1%81%D0%B5%D1%80%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%82.md)

### Логи

Логи лежать по пути

```toml
**/var/log/nginx/access.log**
```

### Cache

Как очистить кэш:

1. Найти кэш по пути `/var/cache/nginx/`
2. Удалить кэш `-rf /var/cache/nginx/`
3. Перезапустить Nginx `sudo service nginx restart`