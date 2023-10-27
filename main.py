import requests as req
import html_parser as prs
import feed_builder as bld


# Source URLs
url_it = 'https://www.unimi.it/it/archivio-avvisi'
url_en = 'https://www.unimi.it/en/notice-board'

# Request HTML pages
res_it = req.get(url_it)
res_en = req.get(url_en)

# Extract news as dictionaries
news_it = prs.parse_news(res_it.text, 'it')
news_en = prs.parse_news(res_en.text, 'en')

# Generate RSS feeds as strings
feed_it = bld.to_feed(news_it, 'it')
feed_en = bld.to_feed(news_en, 'en')

# Write feeds to file
if len(news_it) > 0:
    text_file = open("./news_it.xml", "w")
    text_file.write(feed_it)
    text_file.close()

if len(news_en) > 0:
    text_file = open("./news_en.xml", "w")
    text_file.write(feed_en)
    text_file.close()
