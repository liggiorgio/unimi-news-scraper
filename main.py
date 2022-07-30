import requests

x = requests.get('https://www.unimi.it/it/archivio-avvisi')

source = x.text

index_from = source.find('<div class="layout ds-1col clearfix">')
index_to = source.find('<nav class="pager-nav text-center" role="navigation" aria-labelledby="pagination-heading">')

source = source[index_from:index_to:]
source = " ".join(source.split())
source = source[0:-7:]

source_split = source.split('<div class="col-sm-4 views-row views-row">')

entries = []

# Parse items
for string in source_split:
    _str = string
    item = {}
    
    if 'blu-title pad0 icon promo' in _str:
        # Orange news
        idx_f = _str.find('hreflang="it"') + 14
        idx_t = _str.find('</a>')
        item['title'] = _str[idx_f:idx_t:]

        idx_f = string.find('<a href="') + 9
        idx_t = string.find('hreflang="it"') - 2
        item['link'] = 'https://www.unimi.it' + _str[idx_f:idx_t:]

        idx_f = _str.find('"top10"') + 9
        _str = _str[idx_f::]
        idx_t = _str.find('</div>') - 1
        item['descr'] = _str[0:idx_t:]
    else:
        # Blue news
        idx_f = _str.find('"views-row"') + 12
        _str = _str[idx_f::]
        idx_t = _str.find('</div>')
        item['title'] = _str[0:idx_t:]

        item['link'] = ''

        idx_f = _str.find('"bp-text"') + 11
        _str = _str[idx_f::]
        idx_t = _str.find('</div>') - 1
        item['descr'] = _str[0:idx_t:]
        
    item['guid'] = str(hash(item['title'] + item['link'] + item['descr']))
    entries.append(item)

output = '<rss version="2.0"><channel><title>Tutti gli avvisi | Università degli Studi di Milano Statale</title><description>Archivio avvisi generali Unimi</description><link>https://www.unimi.it/it/archivio-avvisi</link>'

text_file = open("./news_it.xml", "w")

for entry in entries:
    output += '<item>'
    output += '<title>' + entry['title'] + '</title>'
    output += '<link>' + entry['link'] + '</link>'
    output += '<description>' + entry['descr'] + '</description>'
    output += '<guid isPermaLink="false">' + entry['guid'] + '</guid>'
    output += '</item>'

output += '</channel></rss>'
text_file.write(output)
text_file.close()