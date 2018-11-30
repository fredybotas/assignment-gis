import psycopg2
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup

load_dotenv('.env')

connect_str = "dbname='%s' user='%s' " \
              "host='%s' port='%s' password='%s'" \
              % (os.getenv('DB_NAME'),
                 os.getenv('DB_LOGIN'),
                 os.getenv('DB_HOST'),
                 os.getenv('DB_PORT'),
                 os.getenv('DB_PASS'))
db = psycopg2.connect(connect_str)

cursor = db.cursor()
cursor.execute("SELECT binomial from occurences_slovakia")
names_sc = cursor.fetchall()
names_sc = [x[0] for x in names_sc]
count = 0

res = {}
for animal in names_sc:
    print(animal)
    req = requests.get('https://species.wikimedia.org/wiki/'+animal.replace(' ', '_'))
    soup = BeautifulSoup(req.content, 'html.parser')
    els = soup.findAll('b')
    for el in els:
        if el.contents[0] == 'English:':
            name_en = el.next_sibling.replace(u'\xa0', '').split(',')[0]
            if name_en.find(' or ') != -1:
                name_en = name_en[:name_en.find(' or ')]
            if name_en.find(' (') != -1:
                name_en = name_en[:name_en.find(' (')]
            if name_en.find('.') != -1:
                name_en = name_en[:name_en.find('.')]
            if name_en.find(';') != -1:
                name_en = name_en[:name_en.find(';')]
            res[animal] = name_en
    print('-----------')


for k, v in res.items():
    print('Inserting %s' % v)
    cursor.execute("UPDATE occurences_slovakia SET binomial_en = %s WHERE binomial = %s", (v, k))
db.commit()