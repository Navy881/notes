# ssh

[sftp](ssh/sftp.md)

## **Настройка ключей SSH**

### Генерация SSH ключей на клиенте Windows

[https://winitpro.ru/index.php/2019/11/13/autentifikaciya-po-ssh-klyucham-v-windows/](https://winitpro.ru/index.php/2019/11/13/autentifikaciya-po-ssh-klyucham-v-windows/)

На клиентском, компьютере, с которого вы будет подключаетесь к удалённому серверу Windows с OpenSSH, вам нужно сгенерировать пару ключей (открытый и закрытый). Закрытый ключ хранится на клиенте (не отдавайте его никому!), а открытый ключ нужно скопировать в файл **authorized_keys** на SSH сервере. Чтобы сгенерировать SSH ключи на клиенте Windows, вы должны установить [клиент OpenSSH](https://winitpro.ru/index.php/2020/01/22/vstroennyj-ssh-klient-windows/).

В Windows 10/11 и Windows Server 2019/2022 клиент OpenSSH устанавливается как отдельный встроенный компонент с помощью PowerShell:

`Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0`

Запустите обычную (непривилегированную сессию PowerShell) и сгенерируйте пару ED25519 ключей:

`ssh-keygen -t ed25519`

<aside>
❗ По умолчанию утилита ssh-keygen генерирует ключи RSA 2048. В настоящий момент вместо RSA ключей рекомендуется использовать именно ED25519.

</aside>

Утилита попросит вас указать пароль для защиты закрытого ключа. Если вы укажете пароль, то каждый раз при 
спользовании этого ключа для SSH авторизации, вы должны будете вводить этот пароль. Я не стал указывать пароль для ключа (не рекомендуется).

![https://winitpro.ru/wp-content/uploads/2019/11/windows-ssh-keygen-generaciya-pary-ssh-kluchey.jpg](https://winitpro.ru/wp-content/uploads/2019/11/windows-ssh-keygen-generaciya-pary-ssh-kluchey.jpg)

```
Generating public/private ed25519 key pair. Enter file in which to save the key (C:\Users\myuser/.ssh/id_ed25519):

Enter passphrase (empty for no passphrase): Enter same passphrase again: Your identification has been saved in C:\Users\myuser/.ssh/id_ed25519. Your public key has been saved in C:\Users\myuser/.ssh/id_ed25519.pub. The key fingerprint is: SHA256:C2wXeCQSUcJyq0 myuser@computername The key's randomart image is: +--[ED25519 256]--+ | ..*O=..o. | +----[SHA256]-----+
```

Утилита ssh-keygen создаст каталог **.ssh** в профиле текущего пользователя Windows (%USERPROFILE%\.ssh) и сгенерирует 2 файла:

- `id_ed25519` – закрытый ключ (если вы сгенерировали ключ типа RSA, файл будет называться `id_rsa`)
- `id_ed25519.pub` – публичный ключ (аналогичный RSA ключ называется `id_rsa.pub`)

### **Копирование открытого ключа на сервер Ubuntu** вручную

[https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04-ru](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04-ru)

Мы вручную добавим содержимое вашего файла `id_rsa.pub` в файл `~/.ssh/authorized_keys` на удаленном компьютере.

Чтобы вывести содержимое ключа `id_rsa.pub`, введите на локальном компьютере следующую команду:

```bash
cat ~/.ssh/id_rsa.pub
```

Вы увидите содержимое ключа, которое должно выглядеть следующим образом:

```bash
Output
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCqql6MzstZYh1TmWWv11q5O3pISj2ZFl9HgH1JLknLLx44+tXfJ7mIrKNxOOwxIxvcBF8PXSYvobFYEZjGIVCEAjrUzLiIxbyCoxVyle7Q+bqgZ8SeeM8wzytsY+dVGcBxF6N4JS+zVk5eMcV385gG3Y6ON3EG112n6d+SMXY0OEBIcO6x+PnUSGHrSgpBgX7Ks1r7xqFa7heJLLt2wWwkARptX7udSq05paBhcpB0pHtA1Rfz3K2B+ZVIpSDfki9UVKzT8JUmwW6NNzSgxUfQHGwnW7kj4jp4AT0VZk3ADw497M2G/12N0PPB5CnhHf7ovgy6nL1ikrygTKRFmNZISvAcywB9GVqNAVE+ZHDSCuURNsAInVzgYo9xgJDW8wUw2o8U77+xiFxgI5QSZX3Iq7YLMgeksaO4rBJEa54k8m5wEiEE1nUhLuJ0X/vh2xPff6SQ1BL/zkOhvJCACK6Vb15mDOeCSq54Cr7kvS46itMosi/uS66+PujOO+xt/2FWYepz6ZlN70bRly57Q06J+ZJoc9FfBCbCyYH7U/ASsmY095ywPsBo1XQ9PqhnN1/YOorJ068foQDNVpm146mUpILVxmq41Cj55YKHEazXGsdBIbXWhcrRf4G2fJLRcGUr9q8/lERo9oxRm5JFX6TCmj6kmiFqv+Ow9gI0x8GvaQ== demo@test
```

Получите доступ к удаленному хосту с использованием любого доступного метода.

После получения доступа к учетной записи на удаленном сервере убедитесь, что каталог `~/.ssh` существует. При необходимости эта команда создаст директорию, а если она уже существует, команда ничего не сделает:

```bash
mkdir -p ~/.ssh
```

Теперь вы можете создать или изменить файл `authorized_keys` в этой директории. Вы можете добавить содержимое файла `id_rsa.pub` в конец файла `authorized_keys` и при необходимости создать его с помощью этой команды:

```bash
echo public_key_string >> ~/.ssh/authorized_keys
```

В вышеуказанной команде замените `public_key_string` результатами команды `cat ~/.ssh/id_rsa.pub`, выполненной на локальном компьютере. Она должна начинаться с `ssh-rsa AAAA...`.

Наконец, нужно убедиться, что директория `~/.ssh` и файл `authorized_keys` имеют соответствующий набор разрешений:

```bash
chmod -R go= ~/.ssh
```

При этом будут рекурсивно удалены все разрешения «group» и «other» для директории `~/.ssh/`.

Если вы используете учетную запись **root** для настройки ключей учетной записи пользователя, важно учитывать, что директория `~/.ssh` принадлежит пользователю, а не пользователю **root**:

```bash
chown -Rsammy:sammy ~/.ssh
```

В этом обучающем модуле мы используем имя пользователя sammy, но вы можете заменить его в вышеприведенной команде другим используемым вами именем.

### Аутентификация сервере Ubuntu с помощью ключей SSH

Если вы успешно выполнили одну из вышеописанных процедур, вы сможете войти на удаленный хост *без* пароля учетной записи для удаленного хоста.

Базовый процесс выглядит аналогично:

```bash
ssh username@remote_host
```

Если вы подключаетесь к этому хосту первый раз (если вы используете указанный выше последний метод), вы сможете увидеть следующее:

```bash
Output
The authenticity of host '203.0.113.1 (203.0.113.1)' can't be established.
ECDSA key fingerprint is fd:fd:d4:f9:77:fe:73:84:e1:55:00:ad:d6:6d:22:fe.
Are you sure you want to continue connecting (yes/no)?yes
```

Это означает, что ваш локальный компьютер не распознает удаленный хост. Введите «yes» и нажмите `ENTER`, чтобы продолжить.

Если вы не указывали пароль для своего закрытого ключа, вы войдете в систему немедленно. Если вы указали пароль закрытого ключа при создании ключа, вам будет предложено ввести его сейчас (для безопасности вводимые символы не будут отображаться в сеансе терминала). После аутентификации в оболочке откроется новый сеанс с настроенной учетной записью на сервере Ubuntu.

## Подключение через алиасы хоста

На машине-клиенте в `.ssh/` нужно создать файл в `config` и там прописать псевдонимы для подключений.

**.ssh/config**

```sql
Host vps
  User u1
  Hostname 31.172.71.120

Host k3s
  User root
  Hostname 192.168.1.73
```

Теперь вместе `ssh u1@31.172.71.120` можно использовать `ssh vps`.