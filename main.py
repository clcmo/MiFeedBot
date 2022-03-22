import os
from datetime import timedelta, datetime
from dateutil import parser
from time import sleep
import requests
import feedparser


token = os.environ['BOT_TOKEN']
channel = os.environ['CHANNEL_ID']
feed = os.environ['FEED_ID']

def send_message(message):
    requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={channel}&text={message}')

def main():
    rss_feed = feedparser.parse(feed)

    for entry in rss_feed.entries:

        parsed_date = parser.parse(entry.published)
        parsed_date = (parsed_date - timedelta(hours=8)).replace(tzinfo=None) # remove timezone offset
        now_date = datetime.utcnow()

        published_20_minutes_ago = now_date - parsed_date < timedelta(minutes=20)
        if published_20_minutes_ago:
            send_message(entry.links[0].href)
            print(entry.links[0].href)


if __name__ == "__main__":
    while(True):
        main()
        sleep(20 * 60)
        print("It works!")
