#!/bin/bash
NAME_PROJECT=api_yamdb
DOT_DIR_FILE_HOME=$NAME_PROJECT-master
DOT_DIR_FILE_HOME_ZIP=$NAME_PROJECT-master.zip
CURRENT_DIR=$(pwd)
INSTALL_DIR="$CURRENT_DIR/$DOT_DIR_FILE_HOME_ZIP"

function install_and_start() {
    cd $DOT_DIR_FILE_HOME/
    python -m venv venv > /dev/null 2>&1
    source ./venv/bin/activate > /dev/null 2>&1
    echo "Активация виртуального окружения venv и установка всеъ необходимых пакетов"
    python -m pip install --upgrade pip > /dev/null 2>&1
    python -m pip install -r requirements.txt > /dev/null 2>&1
    cd $NAME_PROJECT/
    python manage.py makemigrations > /dev/null 2>&1
    python manage.py migrate > /dev/null 2>&1 && echo "Поздравляем! Всё установлено и готово. Запускаю!"
    python manage.py runserver 
}

if [[ ! -d $DOT_DIR_FILE_HOME ]]
then
    cd $CURRENT_DIR
    wget https://github.com/budaevdigital/$NAME_PROJECT/archive/master.zip -O $INSTALL_DIR > /dev/null 2>&1
    mkdir $DOT_DIR_FILE_HOME
    unzip $DOT_DIR_FILE_HOME_ZIP -d $CURRENT_DIR > /dev/null 2>&1
    rm $DOT_DIR_FILE_HOME_ZIP > /dev/null 2>&1
    install_and_start
else
    rm -r $DOT_DIR_FILE_HOME
    cd $CURRENT_DIR
    wget https://github.com/budaevdigital/$NAME_PROJECT/archive/master.zip -O $INSTALL_DIR > /dev/null 2>&1
    mkdir $DOT_DIR_FILE_HOME
    unzip $DOT_DIR_FILE_HOME_ZIP -d $CURRENT_DIR > /dev/null 2>&1
    rm $DOT_DIR_FILE_HOME_ZIP > /dev/null 2>&1
    install_and_start    
fi
