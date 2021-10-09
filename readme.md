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

