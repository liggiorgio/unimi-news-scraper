from telegraph import Telegraph

tg = Telegraph()
tg.create_account(short_name = 'collaborazioniunimi', author_name = 'Unimi - Collaborazioni studentesche')

response = tg.create_page(
    'N.1 collaborazione presso il Dipartimento di Scienze per gli Alimenti, la Nutrizione e l&#039;Ambiente - Nutrizione delle collettività',
    html_content='<p>Di seguito il bando per l\'attivazione di 1 collaborazione studentesca secondo l\'istituto delle 320 ore per un totale di 24 ore di lavoro per studente.</p><p>Il collaboratore sarà impegnato in attività di sostegno alle esercitazioni in aula di informatica (per un totale di 6 cicli di 4 ore ciascuno) in relazione all’insegnamento di Nutrizione delle collettività. Le collaborazioni in questione verranno attivate per il CdL di Scienze e Tecnologie della Ristorazione (Classe L-26).</p><p></p>',
    author_name = 'Autore',
    author_url = 'https://www.example.com'
)
print(response['url'])


tg = Telegraph()
tg.create_account(short_name = 'collaborazioniunimi')
response = tg.create_page(title = header,
    html_content = description,
    author_name = author,
    author_url = author_link)
print(response['url'])