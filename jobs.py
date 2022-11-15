import requests as req
import html_parser as prs
import feed_builder as bld


# Source URLs
url_jobs = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'

# Request HTML pages
res_jobs = req.get(url_jobs)

# Extract news as dictionaries
news_jobs = prs.parseJobs(res_jobs.text)

# Generate RSS feeds as strings
feed_jobs = bld.toFeed(news_jobs, 'jb')

# Write feeds to file
if len(news_jobs) > 0:
    text_file = open("./news_jobs.xml", "w")
    text_file.write(feed_jobs)
    text_file.close()
