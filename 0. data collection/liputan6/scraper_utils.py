import json
import random
import os

def save_data(title, data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data(title):
    with open(title, encoding='utf-8') as f:
        return json.load(f)

def write_file(id, url, title, date, article, summary, destination):
    news_data = {
        'id': id,
        'url': url,
        'title': title,
        'date': date,
        'content': article,
        'summary': summary
    }
    title = '{}/{}.json'.format(destination, id)
    save_data(title, news_data)

def split_urls(url_list):
    random.shuffle(url_list)
    train_indices = int(len(url_list) * 0.9)
    
    train = url_list[:train_indices]
    dev_test = url_list[train_indices:]
    
    dev_indices = int(len(dev_test) * 0.5)
    dev = dev_test[:dev_indices]
    test = dev_test[dev_indices:]

    return train, dev, test

def generate_news_url_split(file_dir, destination):
    train_urls = []
    dev_urls = []
    test_urls = []

    file_list = os.listdir(file_dir)
    for json_file in file_list:
        if not json_file.endswith('.json'):
            break
        file_path = os.path.join(file_dir, json_file)
        url_list = load_data(file_path)
        train, dev, test = split_urls(url_list)

        for url in train:
            train_urls.append(url)
        for url in dev:
            dev_urls.append(url)
        for url in test:
            test_urls.append(url)
    
    news_urls = {'train_urls': train_urls,
    'dev_urls': dev_urls,
    'test_urls': test_urls
    }
    title = '{}/url.json'.format(destination)
    save_data(title, news_urls)


