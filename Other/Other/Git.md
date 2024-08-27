# Git

**Авторизация**
git config --global [user.name](http://user.name/) Navy881
git config --global user.email [ag881.pst@gmail.com](mailto:ag881.pst@gmail.com)

1. Скачивание репозитория:
git clone [https://github.com/%user_login%/%repo_name%.git](https://github.com/%25user_login%25/%25repo_name%25.git).
2. Переход в репозиторий:
cd %repo_name%
3. Добавление отредактированного файла:
git add %file_name%
git add -A stages all changes
git add . stages new files and modifications, without deletions
git add -u stages modifications and deletions, without new files
git add <path>/.  (все файлы в каталоге)
4. Проверка ветки статуса обновлений:
git status
5. Коммит изменений с комментарием:
git commit -m "комментарий"
6. Историю изменений:
git log
7. Добавление изменений в мастер-ветку:
git push -u origin main
8. Обновление локального репозитория из мастер-ветке:
git pull origin main

**Создание отдельной ветки**

1. Создание ветки git checkout -b new_branch_name
2. Сохранение ветки git push origin new_branch_name
3. Добавление изменений в ветку git add
    1. Удаление изменений из ветки git reset
4. Коммит изменений с комментарием git commit -m "комментарий"
5. Добавление изменений в ветку git push -u origin new_branch_name
6. Создание на сайте pull request в main ветку

**Обновление локального репозитория**

1. Коммит изменения в своей ветке
2. Переход на основную ветку git checkout main
3. Получение изменений из основной ветки git pull origin main
4. Переход в свою ветку git checkout new_branch_name
5. Слияние изменений из основной ветку git merge main
press "i" (i for insert)
write your merge message
press "esc" (escape)
write ":wq" (write & quit)
then press enter

**Подтягивание всех удалённых веток**
git fetch --all

**Удаление файла из отслеживания**
git rm --cached <название файла>

git rm -r --cached <название каталога>/. 

**Переход на другую ветку с перезаписью изменений**
git checkout -f <название ветки>

**Как перезаписать локальные файлы c "git pull"?**
Важно: Если у вас есть какие-либо локальные изменения, они будут потеряны (если они отслеживаются). Кроме того, с опцией --hard или без нее все локальные коммиты, которые не были отправлены, будут потеряны.
Если у вас есть какие-либо файлы, которые не отслеживаются Git (например, загруженный пользовательский контент), эти файлы не будут затронуты.
Сначала запустите выборку, чтобы обновить все ссылки origin/<branch> до последней версии:
git fetch --all

Создайте резервную копию вашей текущей ветки:
git branch backup-master

Тогда у вас есть два варианта:
git reset --hard origin/master
ИЛИ если вы находитесь в какой-то другой ветке:
git reset --hard origin/<branch_name>

Список локальных веток
git branch

Список удаленных веток
git branch -r

Список всех веток
git branch -a

Push to remote branch If you are on a detached head

`git push origin HEAD:name-of-your-branch`

**Откат последнего коммита на удалённом репозитории**

Переход на предыдущий коммит

`git reset --hard {commit-hash}`

Пуш изменений в удалённый репозиторий

`git push origin {branch-name} -f`

Инцициализация локального резитория

`git init --initial-branch=main`

**Подключение удалённого репозитория к локальному**

`git remote add origin https://github.com/harishrajora805/myFirstRepo.git`

Установление связи локальной ветки и удалённой ветки

`git branch --set-upstream-to=<внешний-репозиторий>/<внешняя-ветка> <локальная-ветка>`

`git branch --set-upstream-to=origin/main main`

**Обновление ветки до master**

1. Получите последние изменения из удаленной ветки master: 
`git pull origin master`
2. Убедитесь, что вы находитесь в нужной локальной ветке, например, ветке develop:
`git checkout develop`
3. Объедините изменения из ветки master в вашу локальную ветку:
`git merge master`
4. Выход из ввода `:wq`
5. Разрешите конфликты, если они возникли.
6. Закоммитьте изменения:
`git commit -m "Merge from master"`
7. Отправьте изменения в удаленную ветку:
`git push origin develop`
    
    

**Удалить локальную ветку**

`git branch -D local_branch_name`

**Изменить автора коммита**

`git commit --amend --reset-author`