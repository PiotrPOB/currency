#install lxml and reruests library -> command 1. pip install lxml, 2.pip install requests

import datetime
from lxml import html
from datetime import date
import requests
import time

#day dictionary
days = {0: 'Mo', 1 : 'Tu', 2 : 'We', 3: 'Th', 4: 'Fr', 5: 'Sa', 6: 'Su'}

# currnecy source
urlEUR = 'https://internetowykantor.pl/kurs-euro/'
urlUSD = 'https://internetowykantor.pl/kurs-dolara/'
urlCHF = 'https://internetowykantor.pl/kurs-franka/'
urlGBP = 'https://internetowykantor.pl/kurs-funta/'
urlRUB = 'https://internetowykantor.pl/kurs-rubla-rosyjskiego/'


xpathEUR = '//*[@id="waluta-EUR"]/div[2]/div[4]/span[2]'
xpathUSD = '//*[@id="waluta-USD"]/div[2]/div[4]/span[2]'
xpathCHF = '//*[@id="waluta-CHF"]/div[2]/div[4]/span[2]'
xpathGBP = '//*[@id="waluta-GBP"]/div[2]/div[4]/span[2]'
xpathRUB = '//*[@id="waluta-RUB"]/div[2]/div[4]/span[2]'



def wrap_currency(url, xpath):
    page = requests.get(url)
    tree= html.fromstring(page.text)
    text_web = tree.xpath(xpath+"/text()")
    text_web = str(text_web[0])
    text_web = list(text_web)
    text_web[1]='.'
    text_web = "".join(text_web)
    return text_web


def write_currency(*args):
    local_time = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    local_time = str(local_time).split()
    day_of_week = days[datetime.datetime.today().weekday()]
    currency_line = [day_of_week, local_time[0], local_time[1], *args]
    return currency_line

def currency_recording(file_name, column_header, recording_days, time_interval):
    # recordind_days - how many days works recording, integer
    # time_interval = 1 - means one record per hour in a day, 0.002 - means recording currency every ca. 3 seconds, 60 minutes = 3600 sec.
    f = open(file_name, "w")
    f.write(column_header+"\n")
    print("Starting recording EUR currency ...")
    for i in range(recording_days):
        hour_interval = int(time_interval*3600)
        time_interval = int(24/time_interval)
        for j in range(time_interval):
            currency_records = write_currency(wrap_currency(urlEUR, xpathEUR), wrap_currency(urlUSD, xpathUSD), wrap_currency(urlCHF, xpathCHF), wrap_currency(urlGBP, xpathGBP),wrap_currency(urlRUB, xpathRUB))
            print(currency_records)
            f.write(";".join(currency_records)+"\n")
            time.sleep(hour_interval)
        
    f.close
    print("Stop recording EUR currency ...")



currency_recording('kursy.csv','date;time;euro;usd;chf;gbp;rub',1,0.002)


