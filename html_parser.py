import base64
import hashlib
from bs4 import BeautifulSoup

# Constants
NEWS_URL = 'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'

# Parse general news
def parse_news(source, lang):
    soup = BeautifulSoup(source, 'lxml')
    entries_raw = soup.find_all('div', {'class': 'layout ds-1col clearfix'})

    entries = []

    for entry_raw in entries_raw:
        item = {}
        escape_tags(soup, entry_raw)

        if entry_raw.find('div', {'class': 'blu-title pad0 icon arrow'}):
            item['title'] = entry_raw.find('a').text
            item['link'] = f'https://www.unimi.it{entry_raw.find('a')['href']}'
            content = entry_raw.find('div', {'class': 'top10'})
            descr = content.decode_contents() if content else ''
            descr += f'<br/>ℹ️ {"Leggi la notizia completa" if lang == "it" else "Read the full news"} sul <a href="{item["link"]}">sito</a>'
            item['description'] = escape_chars(descr)
        else:
            item['title'] = entry_raw.find('div', {'class': 'blu-title nero pad0'}).text.strip()
            item['link'] = f'https://www.unimi.it/{lang}/archivio-avvisi'
            descr = entry_raw.find('div', {'class': 'bp-text'}).decode_contents()
            descr += ''.join([f'📄 {attachment.find("a").prettify()}' for attachment in entry_raw.find_all('div', {'class': 'field--item'})])
            descr += ''.join([f'🔗 {hyperlink.find("a").prettify()}' for hyperlink in entry_raw.find_all('div', {'class': 'icon link'})])
            item['description'] = escape_chars(descr)

        item['guid'] = str(base64.b64encode((item['title'] + item['description']).encode('utf-8')))
        entries.append(item)

    return entries

# Parse part-time contracts
def parse_jobs(source):
    soup = BeautifulSoup(source, 'lxml')
    entries_raw = soup.find_all('div', {'class': 'views-row'})
    
    entries = []

    for entry_raw in entries_raw:
        item = {}
        item['link'] = f'https://www.unimi.it{entry_raw.find("a")["href"]}'
        item['title'] = entry_raw.find("a").text
        item['description'] = entry_raw.find("time").text
        item['guid'] = get_guid(item['link'] + item['description'])
        
        entries.append(item)

    entries = sorted(entries, key=lambda d: d['guid'])

    return entries

# Escape UTF-8 chars due to calling `decode_contents()`
def escape_chars(source):
    source = source.replace('\n', '').replace('\xa0', ' ')
    return source

# Switch to Telegram-friendly HTML tags
def escape_tags(soup, entry):
    tag_mapping = {
        'em': 'i',
        'strong': 'b',
        'li': lambda tag: f'• {tag.get_text()}<br>',
        'ul': '',
        'p': '<br>',
    }

    for tag_name, new_tag_name in tag_mapping.items():
        for tag in entry.find_all(tag_name):
            new_tag = soup.new_tag(new_tag_name) if callable(new_tag_name) else soup.new_tag(new_tag_name)
            tag.wrap(new_tag)
            tag.unwrap()

    for tag in entry.find_all('a', {'data-cfemail': True}):
        tag.string = cf_decode_email(tag['data-cfemail'])

# Decode email addresses obfuscated by CloudFare
def cf_decode_email(encoded_string):
    r = int(encoded_string[:2], 16)
    decoded_string = ''.join([chr(int(encoded_string[i:i+2], 16) ^ r) for i in range(2, len(encoded_string), 2)])
    return decoded_string

# Generate GUID for each listing
def get_guid(string):
    return hashlib.sha1(string.encode()).hexdigest()
