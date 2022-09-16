# Convert a list of dictionaries into an RSS feed

def toFeed(entries, lang):
    if lang == 'it':
        output = '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n<title>\nTutti gli avvisi | Università degli Studi di Milano Statale\n</title>\n<description>\nArchivio avvisi generali Unimi\n</description>\n<link>\nhttps://www.unimi.it/it/archivio-avvisi\n</link>\n'
    elif lang == 'en':
        output = '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n<title>\nNotice board | Università degli Studi di Milano Statale\n</title>\n<description>\nGeneral Unimi notice board\n</description>\n<link>\nhttps://www.unimi.it/en/notice-board\n</link>\n'
    elif lang == 'jb':
        output = '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n<title>\nBandi collaborazioni studentesche | Università degli Studi di Milano Statale\n</title>\n<description>\nBandi collaborazioni studentesche Unimi\n</description>\n<link>\nhttps://www.unimi.it/it/studiare/stage-e-lavoro/lavorare-durante-gli-studi/collaborazioni-studentesche/bandi-collaborazioni-studentesche\n</link>\n'

    for entry in entries:
        output += '<item>\n'
        output += '<title>\n' + escape(entry['title']) + '\n</title>\n'
        output += '<link>\n' + escape(entry['link']) + '\n</link>\n'
        output += '<description>\n' + escape(entry['description']) + '\n</description>\n'
        output += '<guid isPermaLink="false">' + escape(entry['guid']) + '</guid>\n'
        output += '</item>\n'

    output += '</channel>\n</rss>\n'

    return output


def escape(string):
    return string.replace('<', '&lt;').replace('>', '&gt;')