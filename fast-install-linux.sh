#!/bin/bash
DOT_DIR_FILE_HOME=~/api_yamdb-master
DOT_DIR_FILE_HOME_ZIP=~/api_yamdb-master.zip


function install_and_start() {
    cd $DOT_DIR_FILE_HOME
    python -m venv venv && source ./venv/bin/activate # > /dev/null 2>&1 && echo "Создано виртуальное окружение venv"
    python -m pip install --upgrade pip # > /dev/null 2>&1 && echo "Обновляю pip в виртуальном окружении"
    python -m pip install -r requirements.txt # > /dev/null 2>&1 && echo "Устанавливаю необходимые пакеты в виртуальном окружении"
    cd api_yamdb/
    python manage.py makemigrations # > /dev/null 2>&1
    python manage.py migrate # > /dev/null 2>&1 && echo "Произведены первоначальные миграции моделей"
    python manage.py runserver # > /dev/null 2>&1 && echo "Поздравляем! Всё установлено и готово. Запускаю!"
}

if [[ ! -d $DOT_DIR_FILE_HOME ]]
then
    wget https://github.com/budaevdigital/api_yamdb/archive/master.zip -O $DOT_DIR_FILE_HOME_ZIP
    mkdir $DOT_DIR_FILE_HOME
    unzip $DOT_DIR_FILE_HOME_ZIP -d ~/
    rm $DOT_DIR_FILE_HOME_ZIP
    install_and_start
else
    rm -r $DOT_DIR_FILE_HOME
    wget https://github.com/budaevdigital/api_yamdb/archive/master.zip -O $DOT_DIR_FILE_HOME_ZIP
    mkdir $DOT_DIR_FILE_HOME
    unzip $DOT_DIR_FILE_HOME_ZIP -d ~/
    rm $DOT_DIR_FILE_HOME_ZIP
    install_and_start
fi
