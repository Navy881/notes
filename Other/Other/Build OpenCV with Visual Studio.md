# Build OpenCV with Visual Studio

Ролик: [https://www.youtube.com/watch?v=_fqpYLM6SCw&ab_channel=TheAIGuy](https://www.youtube.com/watch?v=_fqpYLM6SCw&ab_channel=TheAIGuy)

**Сборка OpenCV**

1. Скачать и установить Visual Studio
2. Скачать и установить CMake
3. Скачать исходники opnecv
4. Скачать исходники внешних модулей opnecv_contrib той же версии, что и исходники opencv
5. В корне системного диска создать каталог "opencv"
6. Распаковать исходники opnecv и opnecv_contrib в каталог "opencv"
7. Создать в каталоге "opencv" каталог "build"
8. Запустить CMake с UI
9. Указать в CMake путь до source code как путь к C:/opnecv/opnecv-4.5.0
10. Указать в CMake путь до build the binaries как путь к C:/opnecv/build
11. Нажать в CMake Configure и выбрать x64 (убедиться, что в качестве компилятора выставлен VS)
12. Подтрвердить выбор "Finish" (запуститься генерация)
13. Найти в списке сгенерированных зависимостей OPENCV_EXTRA_MODULES_PATH
и в значении указать путь до C:/opnecv/opnecv_contrib-4.5.0/modules
14. Нажать "Configure"
15. Повторять пока в списке зависимостей не исчезнуть красные строки
16. Нажать "Generate" (создадуться файлы в C:/opnecv/build)
17. Запустить Visual Studio от администратора
18. Выставить в VS режим Release x64
19. Открыть решение C:/opnecv/build/OpenCV.sln
20. В VS развернуть в обозревателе категорию CMakeTargets
21. ПКМ по ALL_BUILD -> Build (запустится сборка)
22. ПКМ по INSTALL -> Build (запустится установка)

**Подключение к VS**

1. ПКМ по проекту -> Properties
2. VC++ Directories -> Include Directories добавить C:/opnecv/build/install/include
3. VC++ Directories -> Library Directories добавить C:/opnecv/build/install/x64/vc16/lib
4. Linker -> Input -> Additional Dependendecies добавить использемые в проекты .lib
opencv_core450.lib
...
5. В папку проекту ProjectName/x64/Release закинуть .dll для каждой подключенной .lib