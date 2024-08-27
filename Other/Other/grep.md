# grep

```bash
grep -P 'apple|Plan removed. Plan id:' /var/log/remote/backend/zvooq.log-2022-03-08

grep -P 'google|Plan removed. Plan id:' /var/log/remote/backend/zvooq.log-2022-03-04

grep 'Create pending subscription: google.zvuk.prime.1month.renewable.199.trial30d, id: 689450135' /var/log/remote/backend/zvooq.log-2022-03-09

grep '459439481' /var/log/remote/backend/zvooq.log-2022-03-07

grep "u'original_transaction_id': u'2000000003156336'" /var/log/remote/backend/zvooq.log-2022-03-03
grep -P "AppStore verification response:|452741343" /var/log/remote/backend/zvooq.log-2022-03-03

grep -P "331411190" /var/log/remote/backend/zvooq.log-2022-05-05

grep "u'expiration_intent': u'2'" /var/log/remote/backend/zvooq.log-2022-03-03 | grep "u'auto_renew_status': u'0'"

grep boo /var/log/remote/backend

grep -P 'sms handled' /var/log/remote/backend/zvooq.log-2022-08-15
```

Сохранение в файл

```bash
ssh aristov-gv@logcollector.zvq.me "grep -P 'sms handled' /var/log/remote/backend/zvooq.log-2022-08-15" > output.txt
```

Поиск по каталогу

```
grep -hnr 'Container(' src/Zvuk/. > containers.txt

-n            Show relative line number in the file
'yourString*' String for search, followed by a wildcard character
-r            Recursively search subdirectories listed
-h            Suppress the prefixing of file names on output
.             Directory for search (current directory)
```