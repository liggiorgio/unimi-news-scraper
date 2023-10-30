import os
import requests

from feed_builder import to_feed
from html_parser import parse_jobs
from telegrapher import create_job_IV_page
from utils import *


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID_JOBS']
JOBS_URL = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'
JOBS_CHECKLIST_FILE = 'checklist_jobs.dat'
JOBS_FEED_FILE = 'news_jobs.xml'


def main():
    jobs_res = requests.get(JOBS_URL)
    jobs_entries = parse_jobs(jobs_res.text)
    
    if jobs_entries:
        jobs_checklist = load_checklist(JOBS_CHECKLIST_FILE)

        for entry in jobs_entries[::-1]:
            if not [job for job in jobs_checklist if job.guid == entry.guid]:
                entry.iv = create_job_IV_page(entry.link)
                jobs_checklist.append(entry)
                send_job_message(entry, BOT_TOKEN, CHAT_ID)

        save_checklist(jobs_checklist[-50:], JOBS_CHECKLIST_FILE)

        jobs_feed = to_feed(jobs_entries, 'jb')
        save_feed(jobs_feed, JOBS_FEED_FILE)


if __name__ == '__main__':
    main()