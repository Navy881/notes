# sftp

**Использование SFTP для безопасной передачи файлов с удаленного сервера**

[https://www.digitalocean.com/community/tutorials/sftp-ru](https://www.digitalocean.com/community/tutorials/sftp-ru)

**Подключение через SFTP**

`sftp sammy@your_server_ip_or_remote_hostname`

**Передача файлов с помощью SFTP с удалённой машины, к которой подключились по sftp**

`get remoteFile`

`get remoteFile localFile`

**Передача локальных файлов в удаленную систему, к которой подключились по sftp**

`cd`  в целевую директорию

`put localFile`

`put /Users/aristov-gv/my_repos/navy881/sweet_cash/local.env /home/u1/navy881/sweet_cash/local.env`