from html import escape


IDX = {
    'it': 0,
    'en': 1,
    'jb': 2
    }
FEED_NAME = [
    'Tutti gli avvisi | Unimi',
    'Notice board | Unimi',
    'Collaborazioni studentesche | Unimi'
    ]
FEED_DESCR = [
    'Avvisi generali dell\'Università degli Studi di Milano "La Statale"',
    'General notice board of the University of Milan "La Statale"',
    'Bandi delle collaborazioni studentesche dell\'Università degli Studi di Milano "La Statale"'
    ]
FEED_LINK = [
    'https://www.unimi.it/it/archivio-avvisi',
    'https://www.unimi.it/en/notice-board',
    'https://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche'
]
DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>'
RSS = ['<rss version="2.0">', '</rss>']
CHANNEL = ['<channel>', '</channel>']
TITLE = ['<title>', '</title>']
DESCR = ['<description>', '</description>']
LINK = ['<link>', '</link>']
ITEM = ['<item>', '</item>']
GUID = ['<guid isPermaLink="false">', '</guid>']


# Create an XML RSS feed
def to_feed(entries: list[dict], kind: str):
    output: str = f'{DECLARATION}{RSS[0]}{CHANNEL[0]}'
    
    output += f'{TITLE[0]}{FEED_NAME[IDX[kind]]}{TITLE[1]}'
    output += f'{DESCR[0]}{FEED_DESCR[IDX[kind]]}{DESCR[1]}'
    output += f'{LINK[0]}{FEED_LINK[IDX[kind]]}{LINK[1]}'

    for entry in entries:
        output += f'{ITEM[0]}'
        output += f'{TITLE[0]}{escape(entry["title"])}{TITLE[1]}'
        output += f'{LINK[0]}{escape(entry["link"])}{LINK[1]}'
        output += f'{DESCR[0]}{escape(entry["description"])}{DESCR[1]}'
        output += f'{GUID[0]}{escape(entry["guid"])}{GUID[1]}'
        output += f'{ITEM[1]}'

    output += f'{CHANNEL[1]}{RSS[1]}'

    return output
