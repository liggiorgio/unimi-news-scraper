import imgkit
import json
import os
import requests as req

from bs4 import BeautifulSoup
from telegraph import Telegraph


URL_HOME = 'https://www.unimi.it'
ACCOUNT_NEWS = 'avvisiunimi'
ACCOUNT_JOBS = 'collaborazioniunimi'
ICON_FILE = '📄'
ICON_LINK = '🔗'


def create_news_IV_page(url: str):
    job_res = req.get(url)
    source = job_res.text
    soup = BeautifulSoup(source, 'lxml')
    
    header = soup.find('h1', {'class': 'page-header'}).span.text
    temp = soup.find('div', {'class': 'col-sm-7 col-md-8 bs-region bs-region--top-left'})
    for span in temp.find_all('span'):
        span.unwrap()
    for div in temp.find_all('div'):
        div.unwrap()
    links = soup.find('div', {'class': 'elenco-allegati'})
    if links:
        attachments = soup.new_tag('blockquote')
        for i, a in enumerate(links.find_all('a')):
            entry = soup.new_tag('li')
            entry.string = f'{ICON_FILE} ' if a.has_attr('type') else f'{ICON_LINK} '
            entry.append(a)
            if i:
                attachments.append(soup.new_tag('br'))
            attachments.append(entry)
        temp.append(attachments)
    contents = temp.decode_contents().strip()

    return publish_iv(ACCOUNT_NEWS, header, contents)


def create_job_IV_page(job_url: str):
    job_res = req.get(job_url)
    source = job_res.text
    soup = BeautifulSoup(source, 'lxml')

    header = soup.find('h1', {'class': 'page-header'}).span.text
    author = soup.find('div', {'class': 'icon building'}).a.text
    author = f'{author[:125]}...' if len(author) > 128 else author
    author_link = f'{URL_HOME}{soup.find("div", {"class": "icon building"}).a["href"]}'
    clean_tags_jobs(soup)
    temp = soup.find('div', {'class': 'row bs-2col-bricked node node--type-opportunita node--view-mode-full'})
    description = soup.new_tag('p')
    temp.wrap(description)
    temp.unwrap()

    return publish_iv(ACCOUNT_JOBS, header, description.prettify(), author, author_link)


def publish_iv(account, header, content, author=None, author_link=None):
    tg = Telegraph()
    tg.create_account(short_name = account)
    response = tg.create_page(title = header,
        html_content = content,
        author_name = author,
        author_url = author_link)
    return response['url']


def clean_tags_jobs(soup):
    soup.find('div', {'class': 'col-sm-12 bs-region bs-region--top'}).extract() #empty
    soup.find('div', {'class': 'col-sm-6 col-md-8 bs-region bs-region--top-left'}).unwrap() #body
    soup.find('div', {'class': 'bottom10 top10 bp-text'}).unwrap() #description
    soup.find('div', {'class': 'bottom20'}).extract() #location
    soup.find('div', {'class': 'paragraph top20 paragraph--type--bp-column-wrapper bgcolor-ebf0f6 bgcolor'}).unwrap() #announcement
    new_tag = soup.new_tag('blockquote')
    soup.find('div', {'class': 'paragraph__column clearfix pad-box'}).wrap(new_tag)
    soup.find('div', {'class': 'paragraph__column clearfix pad-box'}).unwrap() #announcement
    soup.find('h2', {'class': 'nero-title'}).extract() #title
    soup.find('div', {'class': 'field field--name-field-bando field--type-entity-reference field--label-hidden field--item'}).unwrap() #link
    soup.find('div', {'class': 'row bs-1col media media--type-bando media--view-mode-default'}).unwrap() #link
    soup.find('div', {'class': 'col-sm-12 bs-region bs-region--main'}).unwrap() #link
    soup.find('span', {'class': 'file-link'}).a['href'] = 'https://www.unimi.it' + soup.find('span', {'class': 'file-link'}).a['href']
    soup.find('span', {'class': 'file-link'}).unwrap() #link
    attachs = soup.find('div', {'class': 'field field--name-field-allegati-bando field--type-entity-reference field--label-hidden field--items'})
    if not attachs == None:
        attachs.wrap(attachs.find('span', {'class': 'file-link'}).a)
        new_tag = soup.new_tag('br')
        attachs.parent.insert_before(new_tag)
        attachs.decompose()
    soup.find('div', {'class': 'col-sm-6 col-md-4 bs-region bs-region--top-right'}).unwrap() #deadlines
    soup.find('div', {'class': 'concorsi paragraph--type--bp-docs box-fullgraphic'}).div.unwrap() #deadlines
    soup.find('div', {'class': 'concorsi paragraph--type--bp-docs box-fullgraphic'}).unwrap() #deadlines
    if soup.find('div', {'class': 'bp-attachment icon published flex'}):
        new_tag = soup.new_tag('h3')
        soup.find('div', {'class': 'blu-title field-label-above'}).wrap(new_tag)
        soup.find('div', {'class': 'blu-title field-label-above'}).unwrap() #"Pubblicato"
        soup.find('div', {'class': 'bp-attachment icon published flex'}).unwrap() #container
        new_tag = soup.new_tag('i')
        soup.find('div', {'class': 'pad-attachment'}).wrap(new_tag)
        soup.find('div', {'class': 'pad-attachment'}).unwrap() #published
        soup.find('time').unwrap()
    if soup.find('div', {'class': 'bp-attachment icon clock flex'}):
        new_tag = soup.new_tag('h3')
        soup.find('div', {'class': 'blu-title field-label-above'}).wrap(new_tag)
        soup.find('div', {'class': 'blu-title field-label-above'}).unwrap() #"Scandenza"
        soup.find('div', {'class': 'bp-attachment icon clock flex'}).unwrap() #container
        new_tag = soup.new_tag('i')
        soup.find('div', {'class': 'pad-attachment'}).wrap(new_tag)
        soup.find('div', {'class': 'pad-attachment'}).unwrap() #expiring
        soup.find('time').unwrap()
    soup.find('div', {'class': 'col-sm-7 col-md-8 bs-region bs-region--middle'}).extract() #selections
    for span in soup.find_all('span'):
        span.unwrap()
    for table in soup.find_all('table'):
        filename = 'table.jpg'
        opts = {'format': 'jpg', 'encoding': 'UTF-8', 'width': '400'}
        imgkit.from_string(table.prettify(), filename, css='style.css', options=opts)
        img_url = telegraph_file_upload(filename)
        os.remove(filename)
        img = soup.new_tag('img')
        img['src'] = img_url
        table.insert_before(img)
        table.decompose()


def telegraph_file_upload(path_to_file):
    # From: https://stackoverflow.com/questions/70291947/telegraph-api-upload-file

    file_types = {'gif': 'image/gif', 'jpeg': 'image/jpeg', 'jpg': 'image/jpg', 'png': 'image/png', 'mp4': 'video/mp4'}
    file_ext = path_to_file.split('.')[-1]
    
    if file_ext in file_types:
        file_type = file_types[file_ext]
    else:
        return f'error, {file_ext}-file can not be proccessed' 
      
    with open(path_to_file, 'rb') as f:
        url = 'https://telegra.ph/upload'
        response = req.post(url, files={'file': ('file', f, file_type)}, timeout=1)
    
    telegraph_url = json.loads(response.content)
    telegraph_url = telegraph_url[0]['src']
    telegraph_url = f'https://telegra.ph{telegraph_url}'
    
    return telegraph_url
