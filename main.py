import requests as req
import html_parser as prs
import feed_builder as bld


# Source URLs
url_it = 'https://www.unimi.it/it/archivio-avvisi'
url_en = 'https://www.unimi.it/en/notice-board'
url_jobs = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'

# Request HTML pages
res_it = req.get(url_it)
res_en = req.get(url_en)
res_jobs = req.get(url_jobs)

# Extract news as dictionaries
news_it = prs.parseNews(res_it.text, 'it')
news_en = prs.parseNews(res_en.text, 'en')
news_jobs = prs.parseJobs(res_jobs.text)

# Generate RSS feeds as strings
feed_it = bld.toFeed(news_it, 'it')
feed_en = bld.toFeed(news_en, 'en')
feed_jobs = bld.toFeed(news_jobs, 'jb')

# Write feeds to file
text_file = open("./news_it.xml", "w")
text_file.write(feed_it)
text_file.close()

text_file = open("./news_en.xml", "w")
text_file.write(feed_en)
text_file.close()

text_file = open("./news_jobs.xml", "w")
text_file.write(feed_jobs)
text_file.close()
