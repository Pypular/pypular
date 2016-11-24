# Pypular

## Summary

- [How to Development](#how-to-development)
- [Setting up Database](#setting-up-database)

## How to Development?

1. clone repository.
2. create a virtualenv.
3. Active virtualenv.
4. Install dependencies.
5. Copy the configuration file.
  
> git clone git@github.com:denisra/pypular.git pypular  
> cd pypular  
> python3 -m venv .virtualenv  
> source .virtualenv/bin/activate  
> pip install -r requirements.txt  
> cp contrib/env-sample .env  

======

## Installation

### Install postgresql

```
# install the binary
brew install postgresql
createdb pypular
```

## Configuration

### Getting credentials your on Twitter

Access Twitter App Management and [create a new app](https://apps.twitter.com/app/new) and generate your Access Token on https://apps.twitter.com/app/[id]/keys

### Configuration

Copy and change with your own credentials

```
cp api/conf/api.yaml.template api/conf/api.yaml
```

## Running

```
python -m twitter_connector
```
