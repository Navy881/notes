# SSL сертификат

<aside>
❗ [Туториал](https://www.dmosk.ru/miniinstruktions.php?mini=nginx-ssl)

</aside>

## Получение бесплатного SSL сертификата Let's Encrypt

[https://www.dmosk.ru/miniinstruktions.php?mini=get-letsencrypt](https://www.dmosk.ru/miniinstruktions.php?mini=get-letsencrypt)

### П**олучение сертификата**

```bash
sudo certbot certonly --webroot --agree-tos --email post-U@bk.ru --webroot-path /usr/share/nginx/html/ -d bsikpg.duckdns.org -d [www.](http://www.dmosk.ru/)bsikpg.duckdns.org
```

*где:*

- ***certonly** — запрос нового сертификата;*
- ***webroot** — проверка будет выполняться на основе запроса к корню сайта;*
- ***agree-tos** — даем согласие на лицензионное соглашение;*
- ***email** — почтовый адрес администратора домена;*
- ***webroot-path** — каталог в системе Linux, который является корневым для сайта;*
- ***d** — перечисление доменов, для которых запрашиваем сертификат.*

После успешного выполнения команды, сертификаты будут созданы в каталоге

**/etc/letsencrypt/archive/bsikpg.duckdns.org**, 

а также [симлинки](https://www.dmosk.ru/terminus.php?object=symlink) на них в каталоге

**/etc/letsencrypt/live/bsikpg.duckdns.org**. 

При настройке приложений, стоит указывать пути до симлинков, так как при обновлении файлы в первом каталоге будут меняться, во втором — нет. Публичный ключ будет с именем **cert.pem**, а приватный — **privkey.pem**.

### **Автоматическое продление**

Смотрим полный путь до скрипта certbot:

```bash
which certbot
```

Открываем на редактирование [cron](https://www.dmosk.ru/terminus.php?object=cron) и добавляем следующее:

```bash
crontab -e
```

> Если система вернет ошибку crontab: command not found, устанавливаем пакет cron:
> 
> 
> apt install cron
> 

```bash
0 0 * * 1,4 /usr/bin/certbot renew --noninteractive
```

** в данном примере проверка и продление сертификата будет выполняться по понедельникам и четвергам (**1,4**) в 00:00. **/usr/bin/certbot** или **/bin/certbot** — путь, который мне выдала команда **which certbot**.*

Стоит иметь ввиду, что многие приложения, использующие сертификат, потребуют перезапуска, чтобы перечитать его. Поэтому хорошей идеей будет не просто обновлять сертификат, но и перезапускать сервис, который  использует сертификат. Например, для NGINX:

```bash
systemctl reload nginx
```

Однако, нам нужно, чтобы это происходило автоматически. Для этого открываем файл:

```bash
sudo nano /etc/letsencrypt/cli.ini
```

И добавляем строку:

```bash
...
deploy-hook = systemctl reload nginx
```

### (!!! Ипользуется) Получение сертификата на все поддомены

**Для [*bsikpg.duckdns.org](http://bsikpg.duckdns.org)* сейчас используется этот способ.**

Получение сертификата

```bash
sudo certbot certonly --manual --agree-tos --email post-U@bk.ru --server https://acme-v02.api.letsencrypt.org/directory --preferred-challenges=dns -d bsikpg.duckdns.org -d *.bsikpg.duckdns.org
```

** обратим внимание на 2 детали: 1) мы добавили опцию **server**, чтобы указать, на каком сервере Let's Encrypt должна проходить проверка DNS; 2) мы получаем сертификат как для ***.bsikpg.duckdns.org**, так и самого **bsikpg.duckdns.org**, так как первое не включает второго.*

... система попросит создать TXT-запись в DNS, который обслуживает наш домен:

```bash
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please deploy a DNS TXT record under the name
_acme-challenge.dmosk.ru with the following value:

DN8ovKFJ0leLQV9ofZ81mYKxojwIaed5g6f0bXZCYiI

Before continuing, verify the record is deployed.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

*в данном примере система попросила создать TXT-запись **_acme-challenge.dmosk.ru** со значением **DN8ovKFJ0leLQV9ofZ81mYKxojwIaed5g6f0bXZCYiI**.*

Заходим в панель управления DNS и создаем нужную запись.

Для duckdns [https://www.duckdns.org/spec.jsp](https://www.duckdns.org/spec.jsp)

Вызвать через браузер

`https://www.duckdns.org/update?domains=bsikpg.duckdns.org&token=5d2f7c15-9793-48eb-8ae2-af0ae6847f89&txt=WrEFZBE8Dw0aHvUnMPWPyWM3qYIqEEPHmatT0-XRxG0`

<aside>
❗ Не торопимся нажимать Enter — после настройки DNS нужно немного времени (пару минут), чтобы настройка применилась. Проверить появление записи можно командой с рабочего компьютера:

</aside>

`nslookup -type=txt _acme-challenge.bsikpg.duckdns.org 8.8.8.8`

Как только видим, что настройки применились, нажимаем **Enter**.

Если все сделали правильно, то увидим:

```bash
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/bsikpg.duckdns.org-0001/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/bsikpg.duckdns.org-0001/privkey.pem
   Your cert will expire on 2023-06-12. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```

... сертификат получен.

`/etc/letsencrypt/live/bsikpg.duckdns.org-0001/fullchain.pem`

`/etc/letsencrypt/live/bsikpg.duckdns.org-0001/privkey.pem`

## **Использование всей цепочки сертификатов**

```bash
server {
        listen 443 ssl;
        server_name bsikpg.duckdns.org;
    
        ssl_certificate         /etc/letsencrypt/live/bsikpg.duckdns.org-0001/fullchain.pem;
		    ssl_certificate_key     /etc/letsencrypt/live/bsikpg.duckdns.org-0001/privkey.pem;

        ...
}
```

** обратите внимание, что мы указали путь до файла **fullchain.pem**, в котором должны находиться последовательности, как для домена, так и центров сертификации.*