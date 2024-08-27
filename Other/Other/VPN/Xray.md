# Xray

https://github.com/XTLS/Xray-core?tab=readme-ov-file

[https://habr.com/ru/articles/731608/](https://habr.com/ru/articles/731608/)

https://github.com/EvgenyNerush/easy-xray/blob/main/README.ru.md

# Project X

[https://xtls.github.io/ru/document/](https://xtls.github.io/ru/document/)

https://xtls.github.io/en/document/install.html#install-script

## Настройка сервера

[https://xtls.github.io/ru/document/level-0/ch07-xray-server.html](https://xtls.github.io/ru/document/level-0/ch07-xray-server.html)

### Docker

[https://hub.docker.com/r/teddysun/xray](https://hub.docker.com/r/teddysun/xray)

`docker pull teddysun/xray`

Конфигурация сервера `config.json`

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
    "access": "/home/vpsadmin/xray_log/access.log", // Файл для записи логов доступа
    "error": "/home/vpsadmin/xray_log/error.log" // Файл для записи логов ошибок
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
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [
          {
            "id": "", // Укажите свой UUID
            "flow": "xtls-rprx-vision",
            "level": 0,
            "email": "vpsadmin@yourdomain.com"
          }
        ],
        "decryption": "none",
        "fallbacks": [
          {
            "dest": 80 // Перенаправлять на порт 80 по умолчанию
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
              "certificateFile": "/home/vpsadmin/xray_cert/xray.crt",
              "keyFile": "/home/vpsadmin/xray_cert/xray.key"
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

Для Linux
`docker run -d -p 9000:9000 --name xray --restart=always -v /etc/xray:/etc/xray teddysun/xray`

Для Windows

`docker run -d -p 9000:9000 --name xray --restart=always -v C:\Users\User\etc\xray:/etc/xray teddysun/xray`

## Настройка клиента

[https://xtls.github.io/ru/document/level-0/ch08-xray-clients.html](https://xtls.github.io/ru/document/level-0/ch08-xray-clients.html)

1. Скачайте последнюю версию xray-core для вашей платформы из [репозитория на GitHub](https://github.com/XTLS/Xray-core/releases) и распакуйте архив в удобное место.
2. Создайте пустой файл конфигурации `config.json` в той же папке.

Конфигурация клиента `config.json`

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
      // 2.2 Запросы к китайским доменам отправляем на китайский DNS-сервер и ожидаем получить китайский IP-адрес. Если адрес не китайский, используем следующий DNS-сервер
      {
        "address": "223.5.5.5",
        "domains": ["geosite:cn"],
        "expectIPs": ["geoip:cn"]
      },
      // 2.3 Резервный китайский DNS-сервер
      {
        "address": "114.114.114.114",
        "domains": ["geosite:cn"]
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
      // 3.2 Прямое подключение к китайским доменам
      {
        "type": "field",
        "domain": ["geosite:cn"],
        "outboundTag": "direct"
      },
      // 3.3 Проксирование трафика на зарубежные домены
      {
        "type": "field",
        "domain": ["geosite:geolocation-!cn"],
        "outboundTag": "proxy"
      },
      // 3.4 Трафик, который идёт на DNS-сервер 223.5.5.5, отправляем напрямую
      {
        "type": "field",
        "ip": ["223.5.5.5"],
        "outboundTag": "direct"
      },
      // 3.5 Прямое подключение к китайским IP-адресам
      {
        "type": "field",
        "ip": ["geoip:cn", "geoip:private"],
        "outboundTag": "direct"
      }
      // 3.6 Правило по умолчанию
      // В Xray любой трафик, который не соответствует ни одному из правил маршрутизации, отправляется на первое исходящее подключение (см. раздел 5.1). Поэтому важно разместить настройки прокси-сервера на первом месте.
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
            "address": "sub.yourdomain.com", // Замените на доменное имя вашего сервера
            "port": 443,
            "users": [
              {
                "id": "uuiduuid-uuid-uuid-uuid-uuiduuiduuid", // Должен совпадать с идентификатором на сервере
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
          "serverName": "sub.yourdomain.com", // Замените на доменное имя вашего сервера
          "allowInsecure": false, // Запретить использование недоверенных сертификатов
          "fingerprint": "chrome" // Использовать uTLS для подмены отпечатка браузера Chrome / Firefox / Safari или случайный отпечаток
        }
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

[Справочник по конфигурации](https://xtls.github.io/ru/config/)

**Запуск**

`.\xray.exe run -c config.json`

**GUI клиент для Windows**

[https://github.com/EvgenyNerush/easy-xray/blob/main/V2RayN.ru.md](https://github.com/EvgenyNerush/easy-xray/blob/main/V2RayN.ru.md)