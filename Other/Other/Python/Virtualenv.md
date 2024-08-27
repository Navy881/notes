# Virtualenv

1. Установка `pip install virtualenv`
2. Создание виртуальной среды `virtualenv venv` или `python3 -m venv venv`
3. Запуск среды
    1. Linux, MacOS: `source venv/bin/activate`
    2. Windows:
    Предварительно в PowerShell выполнить команды:
    `Set-ExecutionPolicy Unrestricted -Scope Process
    Set-ExecutionPolicy Unrestricted -Force`
    потом:
     `.\venv\Scripts\activate`