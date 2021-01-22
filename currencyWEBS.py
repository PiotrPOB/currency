import datetime
from lxml import html
from datetime import date
import requests
import time

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



def srap_currency(url, xpath):
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
    currency_line = [local_time[0], local_time[1], *args]
    return currency_line

def currency_recording(file_name, column_header, recording_days, time_interval):
    f = open(file_name, "w")
    f.write(column_header+"\n")
    print("Starting recording EUR currency ...")
    for i in range(recording_days):
        hour_interval = int(time_interval*3600)
        time_interval = int(24/time_interval)
        for j in range(time_interval):
            currency_records = write_currency(srap_currency(urlEUR, xpathEUR), srap_currency(urlUSD, xpathUSD), srap_currency(urlCHF, xpathCHF), srap_currency(urlGBP, xpathGBP),srap_currency(urlRUB, xpathRUB))
            print(currency_records)
            f.write(";".join(currency_records)+"\n")
            time.sleep(hour_interval)
        
    f.close
    print("Stop recording EUR currency ...")


currency_recording('test.csv','date;time;euro;usd;chf;gbp;rub',1,0.05)

