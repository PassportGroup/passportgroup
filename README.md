<p align="center">
    <h1 align="center">CTRL PASSPORTGROUP</h1>
    <br/>
</p>

## Introduction
Ctrl PassportGroup is a platform to manage passportgroup services like automatic GMAIL replying and scheduling of background tasks

## Requirements
Make sure you server meet the following requirements.
- Python 3.8.x+
- virtualenv
- **mysqlclient** driver if your are using mysql as a database
- **psycopg2** driver if your are using postgresql as a database
- MySQL Server 5.7.8+, Mariadb 10.3.2+ or PostgreSQL

## Installation
Install virtualenv with this command.
``` bash
$ pip3 install virtualenv
```

Install mysqlclient
``` bash
$ pip3 install mysqlclient
```

Install psycopg2
``` bash
$ pip3 install psycopg2
```

Fork and/or run this project by running the following command
``` bash
$ git clone https://github.com/PassportGroup/passportgroup.git
```

Navigate into the project's directory and create your virtual environment by running the following commands
``` bash
$ cd passportgroup
$ virtualenv venv
```

Activate virtual env
``` bash
$ source venv/bin/activate
```

Install project's dependencies.
Make sure your virtualenv is activate before running this command
``` bash
$ pip3 install -r requirements.txt
```

Copy .env.example for .env and modify according to yours credentials
``` bash
$ cp .env.example .env
```

This command will help migrate the database and populate the database!
```bash
$ python3 manage.py seeder
```

## Usage

Run the default django server
```bash
$ python3 manage.py runserver
```

Run npm in dev mode
```bash
$ npm run dev
```

To view the CTRL Platform go to, 
```
http://localhost:8000/
```

To view admin panel go to:
```
http://localhost:8000/access91/secure.portal/admin/
```


***NB:***
======

We are using the oauth2client library and a few tweaks needs to be made on the package to 
support django 3

change the following line in `venv/lib/python3.9/site-packages/oauth2client/contrib/django_util/models.py`
Look for 

`def from_db_value(self, value, expression, connection, context):`

Change it to 

`def from_db_value(self, value, expression, connection, context=None):`

Also in django3.0 `urlresolvers was removed be sure to change `reverse`