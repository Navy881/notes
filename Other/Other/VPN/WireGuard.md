# WireGuard

# Установка

1. Зайти на сервер по ssh
2. `sudo -i`
3. Обновить список пакетов
    1. `apt update`
    2. `apt upgrade`
4. Установить WireGuard `apt install wireguard`
5. Сгенерировать пару ключей для сервера `wg genkey | tee /etc/wireguard/privatekey | wg pubkey | tee /etc/wireguard/publickey`
6. Созать конфиг сервера `nano /etc/wireguard/wg0.conf`
    
    ```bash
    ## Set Up WireGuard VPN on Ubuntu By Editing/Creating wg0.conf File ##
    [Interface]
    ## My VPN server private IP address ##
    Address = 10.0.0.1/24
    
    ## My VPN server port ##
    ListenPort = 41194
    
    ## VPN server's private key i.e. /etc/wireguard/privatekey ##
    PrivateKey = <SERVER-PRIVATE-KEY>
    
    PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
    ```
    
    - **PrivateKey** — ****прописываем содержимое из файла **/etc/wireguard/privatekey**.
    - **ListenPort** — можно подставить другое значение, если вы не хотите использовать номер порта по умолчанию.
    - **Address** — это адрес сервера при соединении по VPN.
    - **PostUp** и **PostDown** — команды которые будут выполняться при активации и деактивации сетевого 
    интерфейса eth0. Это команды для файрволла включающие форвардинг пакетов.
    
    <aside>
    💡 Так же не забудьте подставить вместо **eth0** название вашего сетевого интерфейса, если он отличается.
    Узнать названия сетевых интерфейсов можно командой: `ip a`
    
    </aside>
    
7. Включить поддержку IP форвардинга. Для этого открыть файл **sysctl.conf** `nano /etc/sysctl.conf`
8. Найти и разкомментировать в нём строчку **net.ipv4.ip_forward=1** (убирать перед ней символ #).
9. Перезапускаем сервис, чтобы применить настройки `sysctl -p`
10. Включить через **systemctl** демон WireGuard `systemctl enable wg-quick@wg0.service`
11. Запустить WireGuard `systemctl start wg-quick@wg0.service`
12. Проверить работу `systemctl status wg-quick@wg0.service`

# Добавление клиента

1. Сгенерить на клиента ключи `wg genkey | tee /etc/wireguard/{clientname}_privatekey | wg pubkey | tee /etc/wireguard/{clientname}_publickey` ИЛИ взять ключи сгенерированные прямо на клиенте
2. Открыть на сервере конфиг `nano /etc/wireguard/wg0.conf` и добавить новый Peer
    
    ```bash
    [Peer]
    PublicKey = <CLIENT-PUBLIC-KEY>
    AllowedIPs = 10.0.0.2/32
    ```
    
    - **PublicKey** — ****подставить публичнй включ клиента **(**/etc/wireguard/{clientname}_publickey).
    - **AllowedIPs** — ips клиента из диапозона.
3. Перезапустить в **systemd** сервис WireGuard `systemctl restart wg-quick@wg0`
4. Создать конфиг для клиента:
    
    ```bash
    [Interface]
    PrivateKey = <CLIENT-PRIVATE-KEY>
    Address = <CLIENT-ALLOWED-IPS>  
    DNS = 1.1.1.1, 8.8.8.8
    
    [Peer]
    PublicKey = <SERVER-PUBLIC-KEY>
    AllowedIPs = 0.0.0.0/1, 128.0.0.0/1
    Endpoint = <SERVER-IP>:<SERVER-PORT>
    PersistentKeepalive = 20
    ```
    
    - **PrivateKey** — ****приватный ключ клиента (/etc/wireguard/clientname_privetkey).
    - **Address** — адрес клиента при соединении по VPN. Прописать тот же адрес, что и в **wg0.conf** для этого клиента (пример, 10.0.0.2/32).
    - **DNS** — адреса DNS.
    - **PublicKey** — ****подставить публичнй включ сервера из /etc/wireguard/publickey.
    - **AllowedIPs** — ip адреса с которых разрешено подключатся к серверу. Если оставить все нули, то весь трафик с компьютера будет идти через WireGuard.
    - **Endpoint** — ip вашего сервера и порт для подключения, который вы указали в настройках.
    - **PersistentKeepalive** —  ****указывает через сколько секунд посылать пакеты на сервер, служит для поддержания соединения.
5. Скачать клиент [https://www.wireguard.com/install/](https://www.wireguard.com/install/)
6. Подставить конфиг для клиента и подключиться.
7. Провека подключения клиента на сервере команда: `wg`.