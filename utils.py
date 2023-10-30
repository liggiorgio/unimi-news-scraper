import pickle
import requests

from entry import Entry


ICON_DEADLINE = '⌛️'
ICON_APPLY = '📝'
ICON_TOP = '📣'


def escape_html(string: str):
    return string.replace('+', '%2B').replace('&', '%26')


def escape_md(string: str):
    return string.replace('_','\_') \
              .replace('*','\*') \
              .replace('[','\[') \
              .replace(']','\]') \
              .replace('(','\(') \
              .replace(')','\)') \
              .replace('~','\~') \
              .replace('`','\`') \
              .replace('>','\>') \
              .replace('#','\#') \
              .replace('+','\+') \
              .replace('-','\-') \
              .replace('=','\=') \
              .replace('|','\|') \
              .replace('{','\{') \
              .replace('}','\}') \
              .replace('.','\.') \
              .replace('!','\!')


def load_checklist(path: str):
    try:
        with open(path, 'rb') as checklist_file:
            return pickle.load(checklist_file)
    except FileNotFoundError:
        return []


def save_checklist(entries: list, path: str):
    with open(path, 'wb') as checklist_file:
        pickle.dump(entries, checklist_file)


def save_feed(feed: str, path: str):
    with open(path, 'w') as feed_file:
        feed_file.write(feed)


def send_news_message(entry: Entry, bot_token: str, chat_id: str):
    m_title = f'<i><b><u>{entry.title}</u></b></i>'
    if entry.is_top:
        m_title = f'<a href="{entry.iv}">{ICON_TOP}</a> {m_title}'
    m_content = f'{entry.descr}'
    message = escape_html(f'{m_title}\n{m_content}')
    url_send = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=HTML'
    print( requests.post(url=url_send) )


def send_job_message(entry: Entry, bot_token: str, chat_id: str):
    m_title = f'_*__{escape_md(entry.title)}__*_'
    m_deadline = f'{ICON_DEADLINE} _{escape_md(entry.descr)}_'
    m_info = f'[{ICON_APPLY}]({entry.iv}) Bando e candidature su [Unimi\.it]({entry.link})'
    message = escape_html(f'{m_title}\n{m_deadline}\n{m_info}')
    url_send = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=MarkdownV2'
    print( requests.post(url=url_send) )
