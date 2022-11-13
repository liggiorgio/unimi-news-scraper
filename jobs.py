import requests
from bs4 import BeautifulSoup
from telegraph import Telegraph


# Remove non-parsable tags
def cleanTags(soup):
    soup.find('div', {'class': 'col-sm-12 bs-region bs-region--top'}).extract() # Empty
    soup.find('div', {'class': 'col-sm-6 col-md-8 bs-region bs-region--top-left'}).unwrap() # Body
    soup.find('div', {'class': 'bottom10 top10 bp-text'}).unwrap() # Description
    soup.find('div', {'class': 'bottom20'}).extract() # Location
    soup.find('div', {'class': 'paragraph top20 paragraph--type--bp-column-wrapper bgcolor-ebf0f6 bgcolor'}).unwrap() # Announcement
    new_tag = soup.new_tag('blockquote')
    soup.find('div', {'class': 'paragraph__column clearfix pad-box'}).wrap(new_tag)
    soup.find('div', {'class': 'paragraph__column clearfix pad-box'}).unwrap() # Announcement
    soup.find('h2', {'class': 'nero-title'}).extract() # Title
    soup.find('div', {'class': 'field field--name-field-bando field--type-entity-reference field--label-hidden field--item'}).unwrap() # Link
    soup.find('div', {'class': 'row bs-1col media media--type-bando media--view-mode-default'}).unwrap() # Link
    soup.find('div', {'class': 'col-sm-12 bs-region bs-region--main'}).unwrap() # Link
    soup.find('span', {'class': 'file-link'}).a['href'] = 'https://www.unimi.it' + soup.find('span', {'class': 'file-link'}).a['href']
    soup.find('span', {'class': 'file-link'}).unwrap() # Link
    soup.find('div', {'class': 'col-sm-6 col-md-4 bs-region bs-region--top-right'}).unwrap() # Deadlines
    soup.find('div', {'class': 'concorsi paragraph--type--bp-docs box-fullgraphic'}).div.unwrap() # Deadlines
    soup.find('div', {'class': 'concorsi paragraph--type--bp-docs box-fullgraphic'}).unwrap() # Deadlines
    new_tag = soup.new_tag('h3')
    soup.find('div', {'class': 'blu-title field-label-above'}).wrap(new_tag)
    soup.find('div', {'class': 'blu-title field-label-above'}).unwrap() # "Pubblicato"
    soup.find('div', {'class': 'bp-attachment icon published flex'}).unwrap() # Container
    new_tag = soup.new_tag('i')
    soup.find('div', {'class': 'pad-attachment'}).wrap(new_tag)
    soup.find('div', {'class': 'pad-attachment'}).unwrap() # Published
    soup.find('time').unwrap()
    new_tag = soup.new_tag('h3')
    soup.find('div', {'class': 'blu-title field-label-above'}).wrap(new_tag)
    soup.find('div', {'class': 'blu-title field-label-above'}).unwrap() # "Scandenza"
    soup.find('div', {'class': 'bp-attachment icon clock flex'}).unwrap() # Container
    new_tag = soup.new_tag('i')
    soup.find('div', {'class': 'pad-attachment'}).wrap(new_tag)
    soup.find('div', {'class': 'pad-attachment'}).unwrap() # Expiring
    soup.find('time').unwrap()
    soup.find('div', {'class': 'col-sm-7 col-md-8 bs-region bs-region--middle'}).extract() # Selections

if __name__ == "__main__":
    url_jobs = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni/n-6-collaborazioni-studentesche-presso-biblioteca-polo-centrale'

    res_jobs = requests.get(url_jobs)
    source = res_jobs.text
    soup = BeautifulSoup(source, 'lxml')

    # Extract main article properties
    header = soup.find('h1', {'class': 'page-header'}).span.text
    author = soup.find('div', {'class': 'icon building'}).a.text
    author_link = 'https://www.unimi.it' + soup.find('div', {'class': 'icon building'}).a['href']
    cleanTags(soup)
    temp = soup.find('div', {'class': 'row bs-2col-bricked node node--type-opportunita node--view-mode-full'})
    description = soup.new_tag('p')
    temp.wrap(description)
    temp.unwrap()

    tg = Telegraph()
    tg.create_account(short_name = 'collaborazioniunimi')
    response = tg.create_page(title = header,
        html_content = description.prettify(),
        author_name = author,
        author_url = author_link)
    print(response['url'])