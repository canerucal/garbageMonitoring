# Garbage Monitoring System 

<img width="720" alt="resim" src="https://user-images.githubusercontent.com/60014138/180310530-81674cac-42e8-4366-ad6e-3b987ece8474.png">
<img width="720" alt="resim" src="https://user-images.githubusercontent.com/60014138/180310945-c7a61938-38e9-49d0-9c44-8a9a4a54d270.png">
<img width="720" alt="resim" src="https://user-images.githubusercontent.com/60014138/180311087-6199aaba-acd7-465e-a7c5-60c6821295f7.png">

## What is the purpose? / Working Principle
This system will warn the responsible when a garbage/trash is full and ease discharging.
The sensor which connected to Raspberry Pi is triggerred when the distance getting close and sends the numeric value to Django back-end. Acccording to distance value, "trash image" is changing with the range of 0%, 25%, 50% and lastly 100%.

## Features

Trash location can be shown via Google Maps on main page. And when the trash is discharged, responsible can click the "discharge the trash" and value will turn 0%.

Trash discharging percentage is logging on system, and efficiency of system can be follow-up from there.

On efficiency graph section, user can see the 6 months trend.

## Technologies
Django Web Framework, HTML, CSS, JS, Python and a Raspberry Pi.

## How to setup
`git clone https://github.com/canerucal/May-22_garbageMonitoring.git`

`cd garbageMonitoring`

`python3 -m venv venv`

`source env/bin/activate`

`pip install -r requirements.txt`

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py createsuperuser`

`python manage.py runserver`

And also you need to create a database for logging. Table and column names can be found on models.py.
