#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/21
# @Author : trl
from bs4 import BeautifulSoup
import requests
from datetime import datetime


def yield_province_url():
    url = 'http://www.ip138.com/post'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    provinces = soup.find(id='newAlexa').table.find_all('a')
    for p in provinces:
        yield p.get_text(), p.get('href')


def yield_province_city_url():
    host = 'http://www.ip138.com'
    for url in yield_province_url():
        response = requests.get(host + url[1])
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'lxml')
        cities = soup.find('table', attrs={'class': 't12'}).find_all('a')
        for c in cities:
            city = c.find('b')
            if city:
                yield url[0], city.get_text(), host + url[1] + city.parent.get('href')


def yield_data1():
    host = 'http://www.ip138.com'
    for url in yield_province_url():
        city_flag = 0
        response = requests.get(host + url[1])
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'lxml')
        cities = soup.find('table', attrs={'class': 't12'}).find_all('tr')[1:]
        for c in cities:
            city = c.find('b')
            if city:
                city_flag += 1
        if city_flag == 0:
            for c in cities:
                tds = c.find_all('td')
                try:
                    a = url[0] + ' ' + tds[0].get_text() + ' ' + tds[0].get_text() + ' ' + tds[1].get_text()
                    b = url[0] + ' ' + tds[3].get_text() + ' ' + tds[3].get_text() + ' ' + tds[4].get_text()
                    with open('{}.txt'.format(datetime.now().date()), 'a+') as f:
                        f.write(unicode.encode(a, 'utf-8')+'\n')
                        f.write(unicode.encode(b, 'utf-8') + '\n')
                    print url[0], tds[0].get_text(), tds[0].get_text(), tds[1].get_text()
                    print url[0], tds[3].get_text(), tds[3].get_text(), tds[4].get_text()
                except IndexError:
                    pass


def yield_data2():
    for province, city, url, in yield_province_city_url():
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'lxml')
        cities = soup.find('table', attrs={'class': 't12'}).find_all('tr')[1:]
        for c in cities:
            tds = c.find_all('td')
            try:
                a = province + ' ' + city + ' ' + tds[0].get_text() + ' ' + tds[1].get_text()
                b = province + ' ' + city + ' ' + tds[3].get_text() + ' ' + tds[4].get_text()
                with open('{}.txt'.format(datetime.now().date()), 'a+') as f:
                    f.write(unicode.encode(a, 'utf-8') + '\n')
                    f.write(unicode.encode(b, 'utf-8') + '\n')
                print province, city, tds[0].get_text(), tds[1].get_text()
                print province, city, tds[3].get_text(), tds[4].get_text()
            except IndexError:
                pass


if __name__ == '__main__':
    yield_data1()
    yield_data2()
