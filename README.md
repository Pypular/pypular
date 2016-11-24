# Pypular

## Summary

- [Como desenvolver](#como-desenvolver)
- [Configurando Banco de dados](#configurando-banco-de-dados)

## How to Development?

1. clone o respositório.
2. crie um virtualenv com Python 3.5.
3. Ative o virtualenv.
4. Instale as dependências.
5. Copie o arquivo de configuração
  
> git clone git@github.com:lffsantos/pypular.git pypular  
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
