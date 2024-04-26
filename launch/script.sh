#!/bin/bash

link=$(cat link.txt)
archive_name=$(basename "$link")
dir_name=$(echo "$archive_name" | cut -d. -f1)

wget "$link"
tar -xvf "$archive_name"
rm "$archive_name"
cd "$dir_name"

if [ ! -f "requirements.txt" ]
then
cp ../requirements.txt ./
fi

sudo apt -y install python3 python3-pip python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver