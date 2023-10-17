import os
import telebot
import requests
import json
import time
from dotenv import load_dotenv
import random
from time import sleep
import logging

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
IND_API_URL = os.getenv('IND_API_URL')
ADMIN_ID = os.getenv('ADMIN_ID')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

MAX_RETRIES = 5
SLEEP_TIME = 2  # Time to sleep between retries, in seconds

# Public commands
bot.set_my_commands(commands=[
    telebot.types.BotCommand("start", "Start the bot"),
    telebot.types.BotCommand("settings", "Change settings"),
], scope=telebot.types.BotCommandScopeDefault())


def fetch_ind_dates():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(IND_API_URL)
            response.raise_for_status()

            if not response.text:
                print("Empty response received from API.")
                return None

            cleaned_response_text = response.text[5:]  # Remove first 5 characters
            slots = json.loads(cleaned_response_text)

            # Organize slots by date
            slots_by_date = {}
            for slot in slots['data']:
                date = slot['date']
                if date not in slots_by_date:
                    slots_by_date[date] = []
                slots_by_date[date].append(slot)

            # Sort dates and get time slots for the first 5 days
            sorted_dates = sorted(slots_by_date.keys())[:5]
            earliest_slots = {date: slots_by_date[date] for date in sorted_dates}

            return earliest_slots

        except requests.RequestException as e:
            print(f"Error occurred while calling API: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}, Response Content: {response.text}")
            return None

    retries += 1
    sleep_time = SLEEP_TIME + random.uniform(0, 1)  # Adding some jitter
    print(f"Retrying in {sleep_time:.2f} seconds...")
    sleep(sleep_time)


def send_to_chat(slots_by_date, chat_id):
    for date, slots in slots_by_date.items():
        slot_times = ["{0} - {1}".format(slot['startTime'], slot['endTime']) for slot in slots]

        message = (
            "📅 Date: {0}\n"
            "🕒 Available Time Slots:\n\n{1}"
            "\n\nGet your appointment: https://oap.ind.nl/oap/en/#/BIO"
        ).format(date, '\n'.join(slot_times))

        bot.send_message(CHANNEL_ID, message)
        bot.send_message(chat_id, message)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="Fetch Slots", callback_data="start_monitoring")
    keyboard.add(button)
    bot.send_message(message.chat.id, "Please choose:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "start_monitoring":
        bot.send_message(call.message.chat.id, "Starting to monitor IND API...")
        while True:
            slots_by_date = fetch_ind_dates()
            if slots_by_date:
                send_to_chat(slots_by_date, call.message.chat.id)
            time.sleep(300)  # Wait for 5 minutes before the next API call


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot.polling(non_stop=True)
