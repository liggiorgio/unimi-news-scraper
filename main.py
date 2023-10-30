import os
import requests

from feed_builder import to_feed
from html_parser import parse_news
from telegrapher import create_news_IV_page
from utils import *


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID_IT = os.environ['CHAT_ID_NEWS_IT']
CHAT_ID_EN = os.environ['CHAT_ID_NEWS_EN']
IT_URL = 'https://www.unimi.it/it/archivio-avvisi'
EN_URL = 'https://www.unimi.it/en/notice-board'
IT_CHECKLIST_FILE = 'checklist_it.dat'
EN_CHECKLIST_FILE = 'checklist_en.dat'
IT_FEED_FILE = 'news_it.xml'
EN_FEED_FILE = 'news_en.xml'


def main():
    # Italian news
    it_res = requests.get(IT_URL)
    it_entries = parse_news(it_res.text, 'it')

    if it_entries:
        it_checklist = load_checklist(IT_CHECKLIST_FILE)

        for entry in it_entries[::-1]:
            if not [news for news in it_checklist if news.guid == entry.guid]:
                entry.iv = create_news_IV_page(entry.link) if entry.is_top else None
                it_checklist.append(entry)
                send_news_message(entry, BOT_TOKEN, CHAT_ID_IT)

        save_checklist(it_checklist[-50:], IT_CHECKLIST_FILE)

        it_feed = to_feed(it_entries, 'it')
        save_feed(it_feed, IT_FEED_FILE)

    # English news
    en_res = requests.get(EN_URL)
    en_entries = parse_news(en_res.text, 'en')

    if en_entries:
        en_checklist = load_checklist(EN_CHECKLIST_FILE)

        for entry in en_entries[::-1]:
            if not [news for news in en_checklist if news.guid == entry.guid]:
                entry.iv = create_news_IV_page(entry.link) if entry.is_top else None
                en_checklist.append(entry)
                send_news_message(entry, BOT_TOKEN, CHAT_ID_EN)

        save_checklist(en_checklist[-50:], EN_CHECKLIST_FILE)

        en_feed = to_feed(en_entries, 'en')
        save_feed(en_feed, EN_FEED_FILE)


if __name__ == '__main__':
    main()
