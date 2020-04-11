#!/bin/bash
python manage.py makemigrations
git add .
echo Commit message?
read message1 message2 message3 message4
git commit -m $message1 $message2 $message3 $message4
git push heroku master
