import base64
import os
import pickle
import requests
import sys

from feed_builder import to_feed
from html_parser import parse_jobs
from telegrapher import create_job_IV_page


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
JOBS_URL = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'
JOBS_PREV_ENTRIES_FILE = 'jobs_checklist.dat'
IV_ENTRIES_FILE = 'iv_entries.dat'
JOBS_FEED_FILE = 'news_jobs.xml'


def escape_md(string):
    return string.replace('.','\.').replace('-','\-')


def load_checklist():
    try:
        with open(JOBS_PREV_ENTRIES_FILE, 'rb+') as checklist_file:
            return pickle.load(checklist_file)
    except FileNotFoundError:
        return []


def save_checklist(job_entries: list):
    with open(JOBS_PREV_ENTRIES_FILE, 'wb+') as checklist_file:
        pickle.dump(job_entries, checklist_file)


def load_iv_dict():
    try:
        with open(IV_ENTRIES_FILE, 'rb+') as iv_file:
            return pickle.load(iv_file)
    except FileNotFoundError:
        return {}


def save_iv_dict(iv_entries: dict):
    with open(IV_ENTRIES_FILE, 'wb+') as iv_file:
        pickle.dump(iv_entries, iv_file)


def send_telegram_message(msg: str):
    url_send = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=MarkdownV2'
    requests.post(url=url_send)


def main():
    res_jobs = requests.get(JOBS_URL)
    news_jobs = parse_jobs(res_jobs.text)
    if not news_jobs:
        sys.exit()

    jobs_checklist = load_checklist()
    iv_dict = load_iv_dict()
    new_iv_dict = {}

    for item in news_jobs:
        iv_guid = str(base64.b64encode((item['link'] + item['description']).encode('utf-8')))
        iv_link = iv_dict.get(iv_guid, create_job_IV_page(item['link']))
        new_iv_dict[iv_guid] = iv_link

        if not item['guid'] in jobs_checklist:
            jobs_checklist.append(item['guid'])
            title = f'_*__{escape_md(item["title"])}__*_'
            deadline = f'🗓 Scadenza: _{escape_md(item["description"])}_'
            info = f'[ℹ️]({new_iv_dict[iv_guid]}) Bando e candidature sul [sito]({item["link"]})'
            message = f'{title}\n{deadline}\n{info}'
            send_telegram_message(message)

    save_iv_dict(new_iv_dict)
    save_checklist(jobs_checklist[-50:])

    feed_jobs = to_feed(news_jobs, 'jb')
    with open(JOBS_FEED_FILE, 'w') as feed_file:
        feed_file.write(feed_jobs)

if __name__ == '__main__':
    main()