import base64
import hashlib

from bs4 import BeautifulSoup


IDX = {
    'it': 0,
    'en': 1
}
DESCR1 = [
    '<br/>ℹ️ Leggi la notizia completa sul <a href="',
    '<br/>ℹ️ Read the full news on the <a href="'
    ]
DESCR2 = [
    '">sito</a>',
    '">website</a>'
    ]
URL_UNIMI = 'https://www.unimi.it'
URL_BOARD = [
    '/it/archivio-avvisi',
    '/en/notice-board'
    ]
ICON_FILE = '📄'
ICON_LINK = '🔗'


# Parse general news
def parse_news(source: str, lang: str):
    soup = BeautifulSoup(source, 'lxml')

    # Get individual news blocks
    entries_raw = soup.find_all('div', {'class': 'layout ds-1col clearfix'})

    # Generate list of dictionaries
    entries = []

    for entry_raw in entries_raw:
        escape_tags(soup, entry_raw)
        
        item = {}
        if entry_raw.find('div', {'class': 'blu-title pad0 icon arrow'}):
            # Orange news
            item['title'] = entry_raw.find('a').text
            item['link'] = f'{URL_UNIMI}{entry_raw.find("a")["href"]}'
            content = entry_raw.find('div', {'class': 'top10'})
            descr = content.decode_contents() if content else ''
            descr += f'{DESCR1[IDX[lang]]}{item["link"]}{DESCR2[IDX[lang]]}'
        else:
            # Blue news
            item['title'] = entry_raw.find('div', {'class': 'blu-title nero pad0'}).text.strip()
            item['link'] = f'{URL_UNIMI}{URL_BOARD[IDX[lang]]}'
            descr = entry_raw.find('div', {'class': 'bp-text'}).decode_contents()
            for attachment in entry_raw.find_all('div', {'class': 'field--item'}):
                descr += f'{ICON_FILE}{attachment.find("a").prettify()}'
            for hyperlink in entry_raw.find_all('div', {'class': 'icon link'}):
                descr += f'{ICON_LINK}{hyperlink.find("a").prettify()}'
        item['description'] = escape_chars(descr)
        item['guid'] = str(base64.b64encode((item['title'] + item['description']).encode('utf-8')))
        
        entries.append(item)

    return entries


# Parse part-time contracts
def parse_jobs(source: str):
    soup = BeautifulSoup(source, 'lxml')

    # Get individual job blocks
    entries_raw = soup.find_all('div', {'class': 'views-row'})

    # Generate list of dictionaries
    entries = []

    for entry_raw in entries_raw:
        item = {}
        item['link'] = f'{URL_UNIMI}{entry_raw.find("a")["href"]}'
        item['title'] = entry_raw.find('a').text
        item['description'] = entry_raw.find('time').text
        item['guid'] = get_guid(item['link'] + item['description'])
        
        entries.append(item)

    entries = sorted(entries, key = lambda d: d['guid'])
    return entries


# Switch to Telegram-friendly HTML tags
def escape_tags(soup, entry):
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
            tag.replace_with(soup.new_string(cf_decode_email(tag['data-cfemail'])))
    # Replace email addresses 2
    for tag in entry.find_all('a', href=True):
        if 'email-protection' in tag['href']:
            #new_tag = soup.new_tag(name='a', attrs={'href':'mailto:'+cf_decode_email(tag['href'].split('#')[1])})
            #new_tag.string = tag.string
            #tag.replace_with(new_tag)
            tag.replace_with(cf_decode_email(tag['href'].split('#')[1]))


# Escape UTF-8 chars due to calling `decode_contents()`
# TODO: this should be unnecessary, look for BS's escaping options
def escape_chars(source):
    source = source.replace('\n', '')
    source = source.replace('\xa0', ' ')
    return source


# Decode email addresses obfuscated by CloudFare
def cf_decode_email(encodedString):
    r = int(encodedString[:2],16)
    decodedString = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return decodedString


# Generate GUID for each listing
def get_guid(string:str) -> str:
    return hashlib.sha1(str.encode(string)).hexdigest()