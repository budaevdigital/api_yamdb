#!/bin/bash
NAME_PROJECT=api_yamdb
DOT_DIR_FILE_HOME=$NAME_PROJECT-master
DOT_DIR_FILE_HOME_ZIP=$NAME_PROJECT-master.zip
CURRENT_DIR=$(pwd)
echo $CURRENT_DIR

function install_and_start() {
    cd $DOT_DIR_FILE_HOME/
    python -m venv venv
    source ./venv/bin/activate
    echo "Активация виртуального окружения venv"
    python -m pip install --upgrade pip 
    python -m pip install -r requirements.txt 
    cd $NAME_PROJECT/
    python manage.py makemigrations 
    python manage.py migrate 
    python manage.py runserver 
}

if [[ ! -d $DOT_DIR_FILE_HOME ]]
then
    wget https://github.com/budaevdigital/$NAME_PROJECT/archive/master.zip -O $DOT_DIR_FILE_HOME_ZIP
    mkdir $DOT_DIR_FILE_HOME
    unzip $DOT_DIR_FILE_HOME_ZIP -d ~/
    rm $DOT_DIR_FILE_HOME_ZIP
    install_and_start
else
    rm -r $DOT_DIR_FILE_HOME
    wget https://github.com/budaevdigital/$NAME_PROJECT/archive/master.zip -O $DOT_DIR_FILE_HOME_ZIP
    mkdir $DOT_DIR_FILE_HOME
    unzip $DOT_DIR_FILE_HOME_ZIP -d ~/
    rm $DOT_DIR_FILE_HOME_ZIP
    install_and_start
fi
