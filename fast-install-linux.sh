#!/bin/bash
DOT_DIR_FILE_HOME=~/api_yamdb-master
DOT_DIR_FILE_HOME_ZIP=~/api_yamdb-master.zip
CURRENT_DIR = $(pwd)

function install_and_start() {
    cd $DOT_DIR_FILE_HOME
    python -m venv venv && source ./venv/bin/activate 
    python -m pip install --upgrade pip 
    python -m pip install -r requirements.txt 
    cd api_yamdb/
    python manage.py makemigrations 
    python manage.py migrate 
    python manage.py runserver 
}

if [[ ! -d $DOT_DIR_FILE_HOME ]]
then
    cd $CURRENT_DIR 
    wget https://github.com/budaevdigital/api_yamdb/archive/master.zip -O $DOT_DIR_FILE_HOME_ZIP
    mkdir $DOT_DIR_FILE_HOME
    unzip $DOT_DIR_FILE_HOME_ZIP -d ~/
    rm $DOT_DIR_FILE_HOME_ZIP
    install_and_start
else
    rm -r $DOT_DIR_FILE_HOME
    cd $CURRENT_DIR
    wget https://github.com/budaevdigital/api_yamdb/archive/master.zip -O $DOT_DIR_FILE_HOME_ZIP
    mkdir $DOT_DIR_FILE_HOME
    unzip $DOT_DIR_FILE_HOME_ZIP -d ~/
    rm $DOT_DIR_FILE_HOME_ZIP
    install_and_start
fi
