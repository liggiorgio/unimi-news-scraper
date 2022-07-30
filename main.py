import requests

x = requests.get('https://www.unimi.it/it/archivio-avvisi')

source = x.text

index_from = source.find('<div class="layout ds-1col clearfix">')
index_to = source.find('<nav class="pager-nav text-center" role="navigation" aria-labelledby="pagination-heading">')

source = source[index_from:index_to:]
source = " ".join(source.split())
source = source[0:-7:]

entries = source.split('<div class="col-sm-4 views-row views-row">')

output = ""

for entry in entries:
    print(entry)
    print()
    output += entry
    output += '\n'

text_file = open("./data.html", "w")
text_file.write(output)
text_file.close()