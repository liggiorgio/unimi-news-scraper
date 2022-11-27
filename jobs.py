import base64
import pickle

import requests as req

import feed_builder as bld
import html_parser as prs
from telegrapher import getJobTG


# Source URLs
url_jobs = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'

# Request HTML pages
res_jobs = req.get(url_jobs)

# Extract news as dictionaries
news_jobs = prs.parseJobs(res_jobs.text)

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

for item in news_jobs:
    key = str(base64.b64encode((item['link'] + item['description']).encode('utf-8')))
    if not key in iv_dict:
        iv_link = getJobTG(item['link'])
        new_iv_dict[key] = iv_link
        print('New IV link generated')
    else:
        new_iv_dict[key] = iv_dict[key]
        print('Existing key retrieved from dict')
    item['description'] = '🗓 Scadenza: <i>' + item['description'] + '</i><br><a href=' + new_iv_dict[key] + '>ℹ️</a> Bando e candidature sul'

    print(item['title'])
    print(item['description'])
    print()

iv_file = open('iv_entries.dat', 'wb+')
pickle.dump(new_iv_dict, iv_file)
iv_file.close()

# Generate RSS feeds as strings
feed_jobs = bld.toFeed(news_jobs, 'jb')

# Write feeds to file
if len(news_jobs) > 0:
    text_file = open("./news_jobs.xml", "w")
    text_file.write(feed_jobs)
    text_file.close()
