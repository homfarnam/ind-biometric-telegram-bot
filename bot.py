import os
import telebot
import time
from dotenv import load_dotenv
import logging

from settings import city_api_map
from utils import fetch_ind_dates, send_to_chat

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
IND_API_URL = os.getenv('IND_API_URL')
ADMIN_ID = os.getenv('ADMIN_ID')

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# In-memory storage for user settings. TODO: Later, consider using a database.
user_settings = {}
user_stop_flags = {}

bot.delete_my_commands(scope=telebot.types.BotCommandScopeAllChatAdministrators())
bot.delete_my_commands(scope=telebot.types.BotCommandScopeAllPrivateChats())
bot.delete_my_commands(scope=telebot.types.BotCommandScopeChat(ADMIN_ID))
bot.delete_my_commands(scope=telebot.types.BotCommandScopeDefault())

bot.set_my_commands(commands=[
    telebot.types.BotCommand("start", "Start the bot"),
    telebot.types.BotCommand("settings", "Change settings"),
    telebot.types.BotCommand("help", "About the bot"),
], scope=telebot.types.BotCommandScopeDefault())


@bot.message_handler(commands=['start'])
def settings(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for city in city_api_map.keys():
        # Convert 'the_hague' to 'The Hague'
        city_label = city.replace('_', ' ').capitalize()
        button = telebot.types.InlineKeyboardButton(
            text=city_label, callback_data=f"set_city_{city}")
        keyboard.add(button)
    bot.send_message(message.chat.id, "Choose a city:", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def helpcommand(message):
    bot.send_message(message.chat.id, "This bot fetches IND appointment slots for you. "
                                      "You can set a city and start fetching data. \n"
                                      "You will be notified when slots are available each 5 minute. "
                                      "To start, use the /start command.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('set_city_'))
def set_city(call):
    city = call.data[len('set_city_'):]
    user_settings[call.from_user.id] = city
    bot.send_message(call.message.chat.id, f"City set to {city.capitalize()}.")

    # Ask the user if they want to start fetching data
    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(
        text="Start fetching data", callback_data="start_fetching")
    keyboard.add(button)
    bot.send_message(call.message.chat.id,
                     "Do you want to start fetching data?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "start_fetching")
def start_fetching(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Starting to fetch data...")

    # Initialize or reset the stop flag for this user
    user_stop_flags[user_id] = False

    if user_id in user_settings:
        city = user_settings[user_id]
        api_url = city_api_map.get(city)

        if api_url:

            while True:
                # Check if the user has requested to stop
                if user_stop_flags.get(user_id, True):
                    print(f"Stopped fetching data for user {user_id}")
                    break

                slots_by_date = fetch_ind_dates(api_url)

                if slots_by_date:
                    send_to_chat(bot, slots_by_date, chat_id)

                    # After fetching and sending the data, send the stop button
                    keyboard = telebot.types.InlineKeyboardMarkup()
                    button = telebot.types.InlineKeyboardButton(
                        text="Stop fetching data", callback_data="stop_fetching")
                    keyboard.add(button)
                    bot.send_message(chat_id, "Click below to stop fetching data:", reply_markup=keyboard)

                elif slots_by_date is None or len(slots_by_date) == 0:
                    bot.send_message(chat_id, "No available dates.")
                    break
                time.sleep(300)

    else:
        bot.send_message(chat_id, "Please set a city using the /start command.")


@bot.callback_query_handler(func=lambda call: call.data == "stop_fetching")
def stop_fetching(call):
    user_id = call.from_user.id
    user_stop_flags[user_id] = True  # Set the stop flag for this user
    bot.send_message(call.message.chat.id,
                     "Stopping data fetch. You can restart anytime by /start.")


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot.polling(non_stop=True)
