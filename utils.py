import csv
import io
import os
import json
import zipfile
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup
from datetime import datetime

import redis

BSE_URL = 'http://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx?expandable=3'

def redis_conn():
    return redis.Redis.from_url(os.environ.get("REDIS_URL", 'None'),db=1,charset='utf-8', decode_responses=True)

def getBhavCopy():
    bse_page = requests.get(BSE_URL)
    soup = BeautifulSoup(bse_page.content,'lxml')

    iframe_url = soup.find('iframe').attrs.get('src')
    frame_page = requests.get(BSE_URL[:BSE_URL.rfind('/')+1] + iframe_url)
    soup = BeautifulSoup(frame_page.content, 'lxml')
    zip_file_url = soup.find(id='btnhylZip').attrs.get('href')

    zip_file = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(zip_file.content))
    z.extractall('zips')
    return str('zips' + '/' + z.namelist()[0])

def saveToRedis():
    r = redis_conn()
    r.flushall()
    csv_values = csv.DictReader(open(getBhavCopy(), 'r'))
    for row in csv_values:
        r.hmset(row['SC_NAME'].rstrip(), dict(row))
    r.set('scrape_date',str(datetime.today().date().day))


def get_stock_by_name(name):
    results = []
    r = redis_conn()
    if r.get('scrape_date') != str(datetime.today().date().day):
        saveToRedis()
    for equity in r.scan_iter(match='*'+str(name).upper()+'*'):
        results.append(r.hgetall(equity))
    return results

def get_10_stocks():
    results = []
    r = redis_conn()
    if r.get('scrape_date') != str(datetime.today().date().day):
        saveToRedis()
    keys = r.keys('*')
    keys.remove('scrape_date')
    for equity in keys:
        results.append(r.hgetall(equity))
    newlist = sorted(results, key=lambda x: (float(x['PREVCLOSE'])-float(x['CLOSE']))/float(x['LAST']))
    return newlist[:10]

