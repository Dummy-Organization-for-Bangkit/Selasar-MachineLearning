import requests
from bs4 import BeautifulSoup
import json, os, glob
import threading
from scraper_utils import write_file

def get_id(url):
    '''Getting the ID of the news from its url'''
    return url.split('/')[-2]

def get_summary(text):
    summary = ''
    for line in text.split('\n'):
        if 'window.kmklabs.channel =' in line:
            target = line
            break
    temp = target.split('window.kmklabs.article = ')[1]
    temp = temp.split(';')[0]
    data = json.loads(temp)
    return data['shortDescription']

def collect_data(text):
    soup = bs(text)
    title = soup.find_all('h1', {'class': 'read-page--header--title'})[0].get_text()
    date = soup.find_all('time', {'class': 'read-page--header--author__datetime updated'})[0].get_text()
    contents = soup.find_all('div', {'class': 'article-content-body__item-content'})
    article = []
    for content in contents:
        article.append(content.get_text())
    summary = get_summary(text)
    return title, date, article, summary

def scrape_article(url, destination):
    request = requests.get(url)
    url = request.url
    id = get_id(url)
    title, date, article, summary = collect_data(request.text)

    write_file(id, url, title, date, article, summary, destination)

def multiple_article_scraper(urls, destination):
    num_error = 0
    for url in urls:
        try:
            scrape_article(url, destination)
        except:
            num_error += 1
            print('Error scraping data {}/{}; ID {}; Error:{}'.format(i+1, num_news, get_id(url), num_error))

def multi_threading(urls, destination, num_thread=1):
    os.makedirs(destination, exist_ok=True)
    threads = []
    for i in range(num_thread):
        cur_idx = int(i*len(urls)/num_thread)
        cur_urls = urls[cur_idx:cur_idx+int(len(urls)/num_thread)]
        t = threading.Thread(target=multiple_article_scraper, args=(cur_urls, destination,))
        threads.append(t)
        t.start()
'''
def news_dataset_generator(urls, destination, num_thread=1):
    dataset = []
    num_news = len(url_list)
    num_error = 0
    for i, url in enumerate(url_list):
        print('Scraping {}/{}'.format(i+1, num_news))
        try:
            news = scrape_article(url)
            dataset.append(news)
        except:
            num_error += 1
            print('Error scraping data {}/{}; ID {}; Error:{}'.format(i+1, num_news, get_id(url), num_error))
    return dataset
'''

