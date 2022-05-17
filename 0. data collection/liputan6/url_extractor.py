import requests
import json, os
from bs4 import BeautifulSoup as bs
import datetime

from scraper_utils import save_data

def generate_date_range(date_range=30):
    ''' Generate range of date that can be used to construct liputan 6 article list url '''
    base = datetime.datetime.today()
    date_range = [base - datetime.timedelta(days=x) for x in range(date_range)]
    date_list = []
    for date in date_range:
        date_format = date.strftime("%Y/%m/%d")
        date_list.append(date_format)
    return date_list

def get_article_url(url):
    ''' Scrape links for each article in the list of articles '''
    request = requests.get(url)
    soup = bs(request.text)
    url_list = []
    links = soup.find_all('a', {'class': 'articles--rows--item__title-link'})
    if links:
        for link in links:
            link = link.get('href')
            url_list.append(link)
        return url_list

def generate_news_index_url(channel, date_range=30):
    ''' Generate liputan 6 index given the date that contains list of news articles '''
    base_url = 'https://www.liputan6.com'
    date_list = generate_date_range(date_range)
    index_urls = []
    for date in date_list:
        url = '{}/{}/indeks/{}'.format(base_url, channel, date)
        for page in range(5):
            link = '{}?page={}'.format(url, page+1)
            index_urls.append(link)
    return index_urls

def get_urls(channels, date_range):
    ''' Get urls for news articles given their list of channels in liputan 6 '''
    for channel in channels:
        url_list = []
        urls = generate_news_index_url(channel, date_range)
        for url in urls:
            articles_url = get_article_url(url)
            try:
                for article in articles_url:
                    url_list.append(article)
            except:
                continue
        
        if not os.path.isdir('0. data collection/liputan6/url/'):
            os.mkdir('0. data collection/liputan6/url/') 
        title = '0. data collection/liputan6/url/liputan6_{}_url.json'.format(channel)
        save_data(title, url_list)