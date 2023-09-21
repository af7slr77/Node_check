# Node_check 
  - is a telegram bot that warns Zilliqa nodes holders if one of them has stopped working, or is working by skipping blocks.
## Installation:
 * `Сlone the repository to your computer`
```bash
$ git clone https://github.com/af7slr77/Node_check.git
```

## Create VENV and activate:
```bash
$ python3 -m venv
$ source venv/bin/activate
```
## Runing:
### Create file .env and put the following variables in it:
env varibles:
 * `DB_NAME=<your_db_name>`
 * `DB_USER=<your_login>`
 * `DB_PASSWORD=<your_password>`
 * `BOT_TOKEN=<your_telegram_bot_token>`

### Build Docker image:
```bash
$ sudo docker build -t bot .
```


### Run Docker Compose file:
```bash
$ sudo docker compose up -d
```