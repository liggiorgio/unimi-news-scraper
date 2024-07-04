import os
import requests

from bs4 import BeautifulSoup


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
URL = 'https://www.unimi.it/it/studiare/borse-premi-mense-e-alloggi/borse-di-studio-regionali'


def main():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'lxml')
    entries_raw = soup.find_all('div', {'class': 'bp-title'})
    for entry_raw in entries_raw:
        title = entry_raw.text.lower()
        if 'bando' in title:
            if not '2023' in title or '2025' in title:
                message = 'È USCITO IL BANDO BORSE DI STUDIO!!!!!!'
                url_send = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=HTML'
    print( requests.post(url=url_send) )


if __name__ == '__main__':
    main()
