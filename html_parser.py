import base64

from bs4 import BeautifulSoup

# Parse HTML source text and return a dictionary
# INPUT:    string
# OUTPUT:   dictionary

# Parse general news
def parseNews(source, lang):
    soup = BeautifulSoup(source, 'lxml')

    # Get individual news blocks
    entries_raw = soup.find_all('div', {'class': 'layout ds-1col clearfix'})

    # Generate list of dictionaries
    entries = []

    for entry_raw in entries_raw:
        item = {}
        escapeTags(soup, entry_raw)

        if entry_raw.find('div', {'class': 'blu-title pad0 icon promo'}):
            # Orange news
            item['title'] = entry_raw.find('a').text
            item['link'] = 'https://www.unimi.' + lang + entry_raw.find('a')['href']
            descr = entry_raw.find('div', {'class': 'top10'}).decode_contents()
            if lang == 'it':
                descr += '<br/>ℹ️ Leggi la notizia completa sul <a href="' + item['link'] + '">sito</a>'
            elif lang == 'en':
                descr += '<br/>ℹ️ Read the full news on the <a href="' + item['link'] + '">website</a>'
            item['description'] = escapeChars(descr)
        else:
            # Blue news
            item['title'] = entry_raw.find('div', {'class': 'views-row'}).text
            if lang == 'it':
                item['link'] = 'https://www.unimi.it/it/archivio-avvisi'
            elif lang == 'en':
                item['link'] = 'https://www.unimi.it/en/notice-board'
            descr = entry_raw.find('div', {'class': 'bp-text'}).decode_contents()
            for attachment in entry_raw.find_all('div', {'class': 'field--item'}):
                descr += '<br>📄 ' + attachment.find('a').prettify()
            item['description'] = escapeChars(descr)

        item['guid'] = str(base64.b64encode((item['title'] + item['description']).encode('utf-8')))
        entries.append(item)

    return entries


# Parse part-time contracts
def parseJobs(source):
    soup = BeautifulSoup(source, 'lxml')

    # Get individual job blocks
    entries_raw = soup.find_all('div', {'class': 'views-row'})

    # Generate list of dictionaries
    entries = []

    for entry_raw in entries_raw:
        item = {}

        item['link'] = 'https://www.unimi.it' + entry_raw.find('a')['href']
        item['title'] = entry_raw.find('a').text
        item['description'] = entry_raw.find('time').text
        item['guid'] = str(base64.b64encode((item['title'] + item['description']).encode('utf-8')))
        
        entries.append(item)

    return entries


# Switch to Telegram-friendly HTML tags
def escapeTags(soup, entry):
    # Replace <em>s
    for tag in entry.find_all('em'):
        new_tag = soup.new_tag('i')
        tag.wrap(new_tag)
        tag.unwrap()
    # Replace <strong>s
    for tag in entry.find_all('strong'):
        new_tag = soup.new_tag('b')
        tag.wrap(new_tag)
        tag.unwrap()
    # Replace <li>s
    for tag in entry.find_all('li'):
        tag.insert_before(soup.new_string('• '))
        tag.insert_after(soup.new_tag('br'))
        tag.unwrap()
    # Remove <ul>s
    for tag in entry.find_all('ul'):
        tag.unwrap()
    # Remove <p>s
    for tag in entry.find_all('p'):
        tag.insert_after(soup.new_tag('br'))
        tag.unwrap()
    # Replace email addresses
    for tag in entry.find_all('a'):
        if 'data-cfemail' in tag.attrs:
            tag.replace_with(soup.new_string(cfDecodeEmail(tag['data-cfemail'])))


# Escape UTF-8 chars due to calling `decode_contents()`
# TODO: this should be unnecessary, look for BS's escaping options
def escapeChars(source):
    source = source.replace('\n', '')
    source = source.replace('\xa0', ' ')
    return source


# Decode email addresses obfuscated by CloudFare
def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    decodedString = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return decodedString
