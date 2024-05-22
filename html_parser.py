from bs4 import BeautifulSoup, NavigableString
from entry import Entry


IDX = {
    'it': 0,
    'en': 1
}
DESCR1 = [
    '▶️ Scopri di più su <a href="',
    '▶️ Learn more on <a href="'
    ]
DESCR2 = [
    '">Unimi.it</a>',
    '">Unimi.it</a>'
    ]
URL_HOME = 'https://www.unimi.it'
URL_BOARD = [
    '/it/archivio-avvisi',
    '/en/notice-board'
    ]
ICON_FILE = '📄'
ICON_LINK = '🔗'


# Parse general news
def parse_news(source: str, lang: str):
    soup = BeautifulSoup(source, 'lxml')
    entries_raw = soup.find_all('div', {'class': 'layout ds-1col clearfix'})
    entries = []

    for entry_raw in entries_raw:
        escape_tags(soup, entry_raw)
        
        if entry_raw.find('div', {'class': 'blu-title pad0 icon arrow'}):
            # Orange news
            e_title = entry_raw.find('a').text
            e_link = f'{URL_HOME}{entry_raw.find("a")["href"]}'
            content = entry_raw.find('div', {'class': 'top10'})
            e_descr = content.decode_contents() if content else ''
            e_descr += f'%0A{DESCR1[IDX[lang]]}{e_link}{DESCR2[IDX[lang]]}'
            entry = Entry(e_title, escape_chars(e_descr), e_link, is_top=True)
        else:
            # Blue news
            e_title = entry_raw.find('div', {'class': 'blu-title nero pad0'}).text.strip()
            e_link = f'{URL_HOME}{URL_BOARD[IDX[lang]]}'
            content = entry_raw.find('div', {'class': 'bp-text'})
            e_descr = f'{content.decode_contents().strip()}\n' if content else ''
            for attachment in entry_raw.find_all('div', {'class': ['field--item', 'icon link']}):
                class_name = ' '.join(attachment.get('class'))
                match class_name:
                    case 'field--item':
                        e_descr += f'%0A{ICON_FILE}{attachment.find("a").prettify()}'.replace(
                                'href="/it', f'href="{URL_HOME}/it').replace(
                                'href="/en', f'href="{URL_HOME}/en')
                    case 'icon link':
                        e_descr += f'%0A{ICON_LINK}{attachment.find("a").prettify()}'.replace(
                                'href="/it', f'href="{URL_HOME}/it').replace(
                                'href="/en', f'href="{URL_HOME}/en')
            entry = Entry(e_title, escape_chars(e_descr), e_link)
        
        entries.append(entry)

    return entries


# Parse part-time contracts
def parse_jobs(source: str):
    soup = BeautifulSoup(source, 'lxml')
    entries_raw = soup.find_all('div', {'class': 'views-row'})
    entries = []

    for entry_raw in entries_raw:
        e_link = f'{URL_HOME}{entry_raw.find("a")["href"]}'
        e_title = entry_raw.find('a').text
        e_descr = entry_raw.find('time').text
        entry = Entry(e_title, e_descr, e_link)
        
        entries.append(entry)

    return entries


# Switch to Telegram-friendly HTML tags
def escape_tags(soup, entry):
    # Remove <span>s
    for tag in entry.find_all('span'):
        tag.unwrap()
    # Replace <li>s
    for tag in entry.find_all('li'):
        tag.insert_before(soup.new_string('• '))
        tag.insert_after(soup.new_string('%0A'))
        tag.unwrap()
    # Remove <ul>s
    for tag in entry.find_all('ul'):
        tag.unwrap()
    # Remove <p>s
    for tag in entry.find_all('p'):
        tag.insert_after(soup.new_string('%0A'))
        tag.unwrap()
    # Remove <br/>s
    for tag in entry.find_all('br'):
        tag.insert_after(soup.new_string('%0A'))
        tag.unwrap()
    # Replace email addresses
    for tag in entry.find_all('a'):
        if 'data-cfemail' in tag.attrs:
            tag.replace_with(soup.new_string(decode_email(tag['data-cfemail'])))
    # Replace email addresses 2
    for tag in entry.find_all('a', href=True):
        if 'email-protection' in tag['href']:
            #new_tag = soup.new_tag(name='a', attrs={'href':'mailto:'+cf_decode_email(tag['href'].split('#')[1])})
            #new_tag.string = tag.string
            #tag.replace_with(new_tag)
            tag.replace_with(decode_email(tag['href'].split('#')[1]))


# Escape UTF-8 chars due to calling `decode_contents()`
# TODO: this should be unnecessary, look for BS's escaping options
def escape_chars(source):
    return source.replace('\n', '') \
                 .replace('\xa0', ' ')


# Decode email addresses obfuscated by CloudFare
def decode_email(encoded_email):
    r = int(encoded_email[:2],16)
    decoded_email = ''.join([chr(int(encoded_email[i:i+2], 16) ^ r) for i in range(2, len(encoded_email), 2)])
    return decoded_email
