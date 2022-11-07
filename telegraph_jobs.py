from telegraph import Telegraph

tg = Telegraph()
tg.create_account(short_name = '1337')

response = tg.create_page(
    'Hey',
    html_content='<p>Hello, world!</p>'
)
print(response['url'])
