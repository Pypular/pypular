# Pypular

[![Build Status](https://travis-ci.org/Pypular/pypular.svg?branch=master)](https://travis-ci.org/Pypular/pypular)

## Summary


- [Setting up Database](#setting-up-database)
- [How to Development](#how-to-development)

## Setting up Database

### Install postgresql

1. MacOS

```
# install the binary
brew install postgresql
```

2. Ubuntu

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

### Create DB

Command to create database on postgres:

Open your terminal:

**Fisrt option**:

```
createdb pypular
```

**Second option**

1. Change for postgres account:

    ```
    sudo su - postgres
    ```
    
2. Run command line to start client postgres.

   ```
   psql
   ```
   
3. Create user and password.

   ```
   CREATE USER 'username' WITH PASSWORD 'somepassword';
   ```
   
4. Create a database instance.

   ```
   CREATE DATABASE 'database-name' WITH OWNER 'username' ENCODING 'utf-8';
   ```

## How to Development?

1. clone repository.
2. create a virtualenv.
3. Active virtualenv.
4. Install dependencies.
5. Copy the configuration file.
6. Run Migrations
  
```
git clone git@github.com:denisra/pypular.git pypular  
cd pypular  
python3 -m venv .virtualenv  
source .virtualenv/bin/activate  
pip install -r requirements.txt  
cp contrib/env-sample .env  
python manage.py migrate
```
======


## Configuration

### Getting credentials your on Twitter

Access Twitter App Management and [create a new app](https://apps.twitter.com/app/new) and generate your Access Token on https://apps.twitter.com/app/[id]/keys

### Configuration

Copy and change with your own credentials

```
cp contrib/env-sample .env
```

## Running

```
honcho run python manage.py twitter
```

## Checking data

### Create SuperUser
```
honcho run python manage.py createsuperuser
```

### Accessing Django Admin
```
honcho run python manage.py runserver
```
