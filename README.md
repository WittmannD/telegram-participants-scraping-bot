## Telegram participants scraping bot
Telegram bot for receiving information about members of channels and groups. Written using `Telethon` library.

### Run project locally
Before you begin, you need to set a few environment variables in the `.env` file.
Example:
```shell
# expected .env file entry
TELEGRAM_API_ID=123456890
TELEGRAM_API_HASH=telegramapihash
TELEGRAM_BOT_TOKEN=12345678:telegrambottoken
TELEGRAM_PHONE_NUMBER=+321123456789
```
```shell
cd participants-telegram-scraping-bot
# setup virtual environment
python3 -m venv venv
source venv/bin/activate
# install deps and run app
python3 -m pip install -r requriments.txt
python3 main.py
```
### Run using Docker
```shell
docker build -t participants-telegram-scraping-bot .
docker run --env-file .env participants-telegram-scraping-bot
```

### Preview
Available on https://t.me/members_scraping_bot. Deployed on AWS trial, so if the bot doesn't respond, it means the trial is over :)