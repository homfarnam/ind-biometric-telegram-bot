import requests
import json
from time import sleep
import random
import telebot

from settings import city_api_map, MAX_RETRIES, SLEEP_TIME


def fetch_ind_dates(api_url: str):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(api_url)
            response.raise_for_status()

            if not response.text:
                print("Empty response received from API.")
                return None

            # Remove first 5 characters
            cleaned_response_text = response.text[5:]
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
            earliest_slots = {
                date: slots_by_date[date] for date in sorted_dates}

            return earliest_slots

        except requests.RequestException as e:
            print(f"Error occurred while calling API: {e}")
            return None
        except json.JSONDecodeError as e:
            print(
                f"Failed to decode JSON response: {e}, Response Content: {response.text}")
            return None

    retries += 1
    sleep_time = SLEEP_TIME + random.uniform(0, 1)  # Adding some jitter
    print(f"Retrying in {sleep_time:.2f} seconds...")
    sleep(sleep_time)


def send_to_chat(bot: telebot.TeleBot, slots_by_date, chat_id):
    for date, slots in slots_by_date.items():
        slot_times = [
            "{0} - {1}".format(slot['startTime'], slot['endTime']) for slot in slots]

        message = (
            "📅 Date: {0}\n"
            "🕒 Available Time Slots:\n\n{1}"
            "\n\nGet your appointment: https://oap.ind.nl/oap/en/#/BIO"
        ).format(date, '\n'.join(slot_times))

        bot.send_message(chat_id, message)
