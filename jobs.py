import base64
import hashlib
import os
import pickle

import requests as req

import feed_builder as bld
import html_parser as prs
from telegrapher import getJobTG


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

# Source URLs
url_jobs = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'

# Request HTML pages
res_jobs = req.get(url_jobs)

# Extract news as dictionaries
news_jobs = prs.parseJobs(res_jobs.text)

# Early exit
if len(news_jobs) == 0:
    exit()

# Load checklist to avoid repetitions
try:
    checklist_file = open('./jobs_checklist.dat', 'rb+')
except:
    checklist = []
else:
    checklist = pickle.load(checklist_file)
    checklist_file.close()

# Retrieve IV URLs if they exist, and add them to description
try:
    iv_file = open('./iv_entries.dat', 'rb+')
except:
    iv_dict = {}
else:
    iv_dict = pickle.load(iv_file)
    iv_file.close()
finally:
    new_iv_dict = {}

# Do
for item in news_jobs:
    key = str(base64.b64encode((item['link'] + item['description']).encode('utf-8')))
    if not key in iv_dict:
        iv_link = getJobTG(item['link'])
        new_iv_dict[key] = iv_link
        print('New IV link generated')
    else:
        new_iv_dict[key] = iv_dict[key]
        print('Existing key retrieved from dict')
    #item['description'] = '🗓 Scadenza: <i>' + item['description'] + '</i><br><a href="' + new_iv_dict[key] + '">ℹ️</a> Bando e candidature sul'

    if not item['guid'] in checklist:
        checklist.append(item['guid'])
        message = '*'+item['title']+'*\n🗓 Scadenza: _'+item['description']+'_\n[ℹ️]('+new_iv_dict[key].replace('-','\-')+') Bando e candidature sul [sito]('+item['link']+')'
        url_send = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=MarkdownV2'
        print(req.get(url=url_send).json())

# Save IV links
iv_file = open('iv_entries.dat', 'wb+')
pickle.dump(new_iv_dict, iv_file)
iv_file.close()

# Save previous entries (prevents reposting to channel)
while len(checklist) > 50:
    del checklist[0]

checklist_file = open('jobs_checklist.dat', 'wb+')
pickle.dump(checklist, checklist_file)
checklist_file.close()

# Generate RSS feeds as strings
feed_jobs = bld.toFeed(news_jobs, 'jb')

# Write feeds to file
text_file = open("./news_jobs.xml", "w")
text_file.write(feed_jobs)
text_file.close()
