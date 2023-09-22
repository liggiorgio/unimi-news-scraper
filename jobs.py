import base64
import os
import pickle
import requests as req

import feed_builder as bld
import html_parser as prs
from telegrapher import getJobTG

# Constants
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
JOBS_CHECKLIST_FILE = 'jobs_checklist.dat'
IV_ENTRIES_FILE = 'iv_entries.dat'
NEWS_JOBS_FILE = 'news_jobs.xml'

def esc_md(string):
    return string.replace('.', r'\.').replace('-', r'\-')

def get_iv_dict():
    try:
        with open(IV_ENTRIES_FILE, 'rb+') as iv_file:
            return pickle.load(iv_file)
    except FileNotFoundError:
        return {}

def save_iv_dict(iv_dict):
    with open(IV_ENTRIES_FILE, 'wb+') as iv_file:
        pickle.dump(iv_dict, iv_file)

def send_telegram_message(message):
    url_send = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=MarkdownV2'
    return req.get(url=url_send).json()

def main():
    # Request HTML pages
    url_jobs = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'
    res_jobs = req.get(url_jobs)

    # Extract news as dictionaries
    news_jobs = prs.parseJobs(res_jobs.text)

    # Early exit if no news
    if not news_jobs:
        return

    # Load checklist to avoid repetitions
    try:
        with open(JOBS_CHECKLIST_FILE, 'rb+') as checklist_file:
            checklist = pickle.load(checklist_file)
    except FileNotFoundError:
        checklist = []

    # Retrieve or generate IV URLs
    iv_dict = get_iv_dict()
    new_iv_dict = {}

    for item in news_jobs:
        key = base64.b64encode((item['link'] + item['description']).encode('utf-8')).decode('utf-8')
        iv_link = iv_dict.get(key, getJobTG(item['link']))
        new_iv_dict[key] = iv_link

        if item['guid'] not in checklist:
            checklist.append(item['guid'])
            message = f'*{esc_md(item["title"])}*\n🗓 Scadenza: _{esc_md(item["description"])}_\n[ℹ️]({esc_md(new_iv_dict[key])}) Bando e candidature sul [sito]({esc_md(item["link"])})'
            send_telegram_message(message)
    
    # Save IV links
    save_iv_dict(new_iv_dict)

    # Limit the checklist to the last 50 entries
    while len(checklist) > 50:
        checklist.pop(0)

    # Save the checklist
    with open(JOBS_CHECKLIST_FILE, 'wb+') as checklist_file:
        pickle.dump(checklist, checklist_file)

    # Generate RSS feeds as strings
    feed_jobs = bld.toFeed(news_jobs, 'jb')

    # Write feeds to file
    with open(NEWS_JOBS_FILE, 'w') as text_file:
        text_file.write(feed_jobs)

if __name__ == '__main__':
    main()
