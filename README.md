## Intro
Automates Facebook Marketplace mailing. Useful when I look for subleases in a new city to support my digital nomad lifestyle.

## Requirements
```
brew install python
brew install --cask chromedriver
python -m pip install pipenv
pipenv install -r requirements.txt
```

## Preparation

```
EMAIL=
PASSWORD=
```

message.txt
```
Hi, is it available?
```

## Running

```shell
pipenv run ./src/main.py
```

## What can go wrong?

![Account is restricated](doc/RestriactedAccount.webp)
