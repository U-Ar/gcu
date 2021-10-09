# GCU - GPA Calculator for UTAS

## About 

This is the command line tool for calculating your GPA with automatic access to UTAS.

UTAS is "Utokyo Academic affairs System", which offers the Web service for students of The University of Tokyo.

UTAS shows score tables, but it doesn't calculate GPA by itself, at least for me.

That's the reason why I developed this.

## System requirements

- docker
- docker-compose

should be available in your system to use this application.

## How to use

1. clone the repository into your local environment
```
git clone https://github.com/U-Ar/gcu.git
cd gcu
```
2. start two docker containers ("selenium", "app") using docker-compose
```
sudo docker-compose build --no-cache
sudo docker-compose up -d
```

3. enter the container "app" 
```
sudo docker-compose exec app bash
```

4. run the python program
```
python gcu.py
```

5. type student id and password following the prompt 
6. results will be shown

## Setting

The setting for calculating GPA can be changed with app/settings.txt.

The parameters are following:
- point of "優上" : default value is 4.3
- point of "優" : default value is 4.0
- point of "良" : default value is 3.0
- point of "可" : default value is 2.0
- point of "不可" : default value is 0.0
- flag of including courses whose "科目GP" is "*" : in the default setting you include

Don't add extra lines or remove spaces in settings.txt. Maybe becomes the cause of errors.

If you want other complex settings, please contact me.
Or I welcome your pull request.

## Implementation

The program is written in Python, and selenium is used to automatically manipulate a browser.

In order to make it independent of the local environment, 
both of the browser and the program are run in docker containers.

They communicate on port 4444, so you should assure it's not used or change source codes.