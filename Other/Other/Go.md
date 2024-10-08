# Go

[http://golang-book.ru/](http://golang-book.ru/)

# Синтаксис

## Package

`package main`

Это называется «определением пакета». Любая Go программа должна начинаться с определения имени пакета. Не забудьте включать эту строку в программы, которые вы пишете.

## import

`import "fmt"`

Ключевое слово `import` позволяет подключить сторонние пакеты для использования их функциональности в нашей программе. Пакет `fmt` (сокращение от format) реализует форматирование для входных и выходных данных. 

## main()

Эта функция будет вызываться сама при запуске программы.

## godoc

Go — очень хорошо документированный язык. Команда `godoc` очень полезна для начала поиска ответов на возникающие вопросы.

`godoc fmt Println`

## **Типы данных**

# Создание проекта

## Инициализация проекта

`go mod init {catalog mame}`

Команда go mod инициализирует новый Go-проект в указанном рабочем каталоге. Команда также создает в каталоге файл go.mod для управления зависимостями вашего проекта.

Добавление зависимых модулей и go.sum

`go mod tidy`

## Установка пакета

`go get github.com/gorilla/mux`

Установка сторонней зависимости.

## Запуск приложения

`go run main.go`

Запуск приложения через  файл `main.go`