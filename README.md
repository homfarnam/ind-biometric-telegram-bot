# IND Slot Monitor Bot

## Description

A Telegram bot designed to monitor and alert about the availability of free slots for biometric appointments from the IND (Immigration and Naturalisation Service) in the Netherlands. The bot fetches the earliest available slots for the first 5 days and sends this information to a specified Telegram channel at regular intervals.

## Features

- Fetches available biometric appointment slots from the IND API.
- Filters and sorts slots by date.
- Sends the earliest available slots of the first 5 days to the Telegram channel.
- Continuous monitoring of the IND API at 5-minute intervals.

## Environment Variables

Before running the bot, make sure to set the following environment variables either in your shell or in a `.env` file:

- `TELEGRAM_TOKEN`: Your Telegram Bot API token.
- `CHANNEL_ID`: The Telegram Channel ID where the bot will send messages.
- `IND_API_URL`: The URL of the IND API to fetch slots from.

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

### .env File

Create a `.env` file in the root directory and add the following:

```env
TELEGRAM_TOKEN=your_telegram_bot_api_token
CHANNEL_ID=your_channel_id
IND_API_URL=your_ind_api_url
```

### Running the Bot

Run your bot using:

```bash
python bot.py
```

## Usage

- Send `/start` to the bot.
- Click on "Fetch Slots" to start monitoring the IND API.

The bot will then start monitoring the IND API and will send messages to the specified Telegram channel.
