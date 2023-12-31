# IND Biometric Slot Monitor Bot

## Description

A Telegram bot designed to monitor and alert about the availability of free slots for biometric appointments from the
IND (Immigration and Naturalisation Service) in the Netherlands. The bot fetches the earliest available slots for the
first 5 days and sends this information to your chat with the bot.

## Features

- Fetches available biometric appointment slots from the IND API.
- Filters and sorts slots by date.
- Sends the earliest available slots of the first 5 days to the chat.

## Environment Variables

Before running the bot, make sure to set the following environment variables either in your shell or in a `.env` file:

- `TELEGRAM_TOKEN`: Your Telegram Bot API token.

## Setup and Installation

### Requirements

- Python 3.x
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- `requests`
- `python-dotenv`

Install the requirements:

```bash
pip install pyTelegramBotAPI requests python-dotenv
```

or

```bash
pip install -r requirements.txt
```

### .env File

Create a `.env` file in the root directory and add the following:

```env
TELEGRAM_TOKEN=your_telegram_bot_api_token
```

### Running the Bot

Run your bot using:

```bash
python bot.py
```

## Usage

- Send `/start` to the bot.
- Click on any cities that you want to start monitoring the IND API.

The bot will then start monitoring the IND API and will send messages to your chat.

---

## Docker Deployment

If you have Docker installed on your machine, you can use it to deploy the bot without worrying about dependencies.

### Building the Docker Image

First, navigate to the root directory of the project where the `Dockerfile` is located. Then, build the Docker image
using the following command:

```bash
docker build -t ind-bot .
```

### Running the Docker Container

After building the image, you can run it in detached mode so that it operates in the background. To do this, use the
following command:

```bash
docker run -d -p 4000:80 -e TELEGRAM_TOKEN=your_token ind-bot
```

Replace `your_token` with your actual Telegram bot token, respectively.

### Monitoring Logs

To check the logs of a running container, you can use the following command:

```bash
docker logs [CONTAINER_ID]
```

Replace `[CONTAINER_ID]` with the actual container ID that you received when you started the Docker container.

### Stopping the Docker Container

If you need to stop the Docker container, you can do so with the following command:

```bash
docker stop [CONTAINER_ID]
```

Replace `[CONTAINER_ID]` with the actual container ID.
