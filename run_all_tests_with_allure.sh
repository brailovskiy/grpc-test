#!/usr/bin/env bash

# Получаем пути до скрипта и текущий каталог
pathToScript="$(dirname "$0")"
currentPath=$(pwd)

# Делаем полный путь до скрипта в зависимости от того, откуда был вызван скрипт
# Нужно это потому, что "$(dirname "$0")" при вызове ./script_name.sh выдает "."
if [[ -f $currentPath/run_all_tests_with_allure.sh ]];
then
    path="$currentPath"
else
    path="$currentPath/$pathToScript"
fi

# Флаг allure_is_installed отвечает за информацию, установлен ли allure; по умолчанию - false
allure_is_installed=false

# Переход в домашнюю директорию
cd

# Проверка на наличие директории allure_bin/
if [[ -d allure_bin/ ]] ;
then
    cd allure_bin

# Если директория allure-2.7.0/ присутствует, выставляем флаг allure_is_installed в значение true
    if [[ -d allure-2.7.0/ ]] ;
    then
        echo "Allure is already installed"
        cd
        allure_is_installed=true
    else
        cd
    fi
# Если нет директории allure_bin/ создаем ее
else
    echo "Create directory allure_bin"
    mkdir ./allure_bin/
fi

# Проверяем значение флага allure_is_installed - если false, то скачиваем и распаковываем allure в ./allure_bin/
if [[ "$allure_is_installed" == false ]] ;
then
    cd /tmp

    if [[ -f allure-2.7.0.tgz ]] ;
    then
        echo "Remove allure archive and download it again"
        rm allure-2.7.0.tgz
        wget -O allure-2.7.0.tgz https://bintray.com/qameta/generic/download_file?file_path=io%2Fqameta%2Fallure%2Fallure%2F2.7.0%2Fallure-2.7.0.tgz
    else
        echo "Download allure archive"
        wget -O allure-2.7.0.tgz https://bintray.com/qameta/generic/download_file?file_path=io%2Fqameta%2Fallure%2Fallure%2F2.7.0%2Fallure-2.7.0.tgz
    fi

    cd
    echo "Unpacking archive with allure to allure_bin"
    tar -xvzf /tmp/allure-2.7.0.tgz -C ./allure_bin/
fi

# Переходим в директорию тестов
echo "Navigate to directory with tests: $path"
cd "$path"

# Запускаем все тесты, помещаем отчеты allure в директорию ./allure_results
echo "Run all tests using pytest library"
python3 $(which py.test) --alluredir=logs/allure-results/

# Разворачиваем локальный сервер с отчетами allure
echo "Create local server with allure results"
~/allure_bin/allure-2.7.0/bin/allure serve logs/allure-results/