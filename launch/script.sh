#!/bin/bash

link="https://www.dropbox.com/scl/fi/f0jcmvdyoxfo5vjjd1x4x/models.zip?rlkey=9rm5668smt8cophi2aa23qb3d&st=cs7h4py7&dl=0"
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

export BOT_TOKEN="7039717257:AAEduH_t-lH8XJh91c2jrmhNpvCkpWvyqkI"