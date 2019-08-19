# Dialog API testing framework

Проект содержит фреймворк для написания тестов для Dialog API с использованием pytest

dialog gRPC API schema -  https://dialogs.github.io/api-schema/

## Работа с проектом на локальной машине:

> Подробная информация о том как начать работу с автотестами - в спейсе QA: https://confluence.transmit.im/display/QA/Automation+Testing

1. Установить Python 3.x (https://www.python.org/). На данный момент гарантирована работа на версии 3.7.
2. Клонировать репозиторий:
    ```
    git clone https://bitbucket.transmit.im/scm/autt/server-test-suites.git
    ```
3. Перейти в папку проекта
    ```
    cd server-test-suites/
    ```
4. Установить необходимые зависимости:
    ```
    pip install -r requirements.txt
    ```
    

## Быстрый запуск тестов:
Для запуска необходим установленный Python 3.x+

В environment variables окружения неоюходимо добавить переменные - 
```
    password    //пароль для тестовых юзеров ( tester[1-10] )
```
тесты, использующие dashboard, так же потребуют:
```
    admin_password  //пароль для пользователя, с правами администратора 
    admin_username  //имя пользователя, c правами администратора
```

1. Клонировать репозиторий:
    ```
    git clone https://bitbucket.transmit.im/scm/autt/server-test-suites.git
    ```
2. Перейти в папку проекта
    ```
    cd server-test-suites/
    ```
3. Утанавливаем tox:
    ```
    pip install tox
    ```
4. Запускаем тесты на указанном эндпоинте:
    ```
    tox -- --ep=endpointname.transmit.im
    ```
    

## Структура проекта:

* **tests_functional** - набор стабильных smoke-тестов ( запускается на CI )
* **tests_unstable** - тесты, требующие доработки. Не предназначены для использования в CI. 
* **tests_api_methods** - тесты отдельных методов Dialog API (WIP)
* **sdk_testing_framework** -  фреймворк для работы с Dialog API
* **tests_.../conftest.py** - содержит фикстуры для подготовки тестовых данных (для каждого тестового набора - свой)
* **pytest.ini** - стандартный файл натроек pytest 
* **logs** - папка для отчетов junit и Allure отчетов
* **shared** - инструменты для генерации данных, работы с файлами, работы с админкой ( graphQL запросы в Dialog dashboard )
* **jenkinsfile** - конфигурация запуска в CI 
* **tox.ini** - основной конфигурационный файл 

## Структура запроса к API
To Do


## Логгирование:
* Для включения логгирования необходимо в файле pytest.ini выставить:
    ```
    log_cli = true
    ```
* Уровни логгирования задаются в параметре ```log_cli_level```. Доступные значения:
    * INFO - отображаются информационные логи, предупреждения и ошибки
    * WARNING - отображаются предупреждения и ошибки
    * ERROR - отображаются только ошибки
    * DEBUG - отображаются все логи (включая стандартные в pytest)