import requests
import html_parser as p
import feed_builder as b


url_jobs = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'

res_jobs = requests.get(url_jobs)

news_jobs = p.parseJobs(res_jobs.text)

p.parseJobsIV((news_jobs[1])['link'])
exit()

feed_jobs = b.toFeed(news_jobs, 'jb')

text_file = open("./news_jobs.xml", "w")
text_file.write(feed_jobs)
text_file.close()
