# Pypular

## Installation

### Install postgresql

```
# install the binary
brew install postgresql
createdb pypular
```

### Create virtualenv

```
python3 -m venv venv_pypular
source venv_pypular/bin/activate
```
***Warning - django is not integrated yet***

### Installing dependencies
```
pip install -r requirements.txt
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
python -m api.twitter_connector
```
