import requests
import html_parser as p
import feed_builder as b

from bs4 import BeautifulSoup
from telegraph import Telegraph


url_jobs = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni/n1-collaborazione-presso-il-dipartimento-di-scienze-gli-alimenti-la-nutrizione-e-lambiente'

res_jobs = requests.get(url_jobs)
source = res_jobs.text
soup = BeautifulSoup(source, 'lxml')

header = soup.find('h1', {'class': 'page-header'}).span.text
author = soup.find('div', {'class': 'icon building'}).a.text
author_link = 'https://www.unimi.it' + soup.find('div', {'class': 'icon building'}).a['href']
description = soup.find('div', {'class': 'row bs-2col-bricked node node--type-opportunita node--view-mode-full'}).decode_contents()

print(description)
exit()
