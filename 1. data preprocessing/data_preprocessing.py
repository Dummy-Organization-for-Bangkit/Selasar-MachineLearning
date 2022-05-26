import re
import os
import glob
import json

unknown = set()

def load_data(title):
    with open(title, encoding='utf-8') as f:
        return json.load(f)

def split_paragraph(content_list):
    contents = []
    for content in content_list:
        paragraphs = []
        content = content.split('\n')
        for paragraph in content:
          if not '\xa0' in paragraph:
              paragraphs.append(paragraph)
        contents.append(paragraphs)
    return contents

def tokenize_content(content_list):
    content_list = split_paragraph(content_list)
    content = []
    for i, paragraph in enumerate(content_list):
        for i, sentence in enumerate(paragraph):
            words = []
            sentence = sentence.split(' ')
            for word in sentence:
                token = tokens = re.findall(r"[\w'\%\&\-\/\=\+\*$£]+|[\[\]().,!?\:;\"\“\”]", word)
                words += token
            content.append(words)
    return content
    
def tokenize_summary(summary):
    summary = summary.split(' ')
    words = []
    for word in summary:
        if len(word) > 0:
            token = tokens = re.findall(r"[\w'\%\&\-\/\=\+\*$£]+|[\[\]().,!?\:;\"\“\”]", word)
            words += token
    return words

def preprocessing(PATH, DESTINATION):
    os.makedirs(DESTINATION, exist_ok=True)
    files = glob.glob(PATH)
    for file in files:
        json_file = load_data(file)
        clean_content = tokenize_content(json_file['content'])
        clean_summary = tokenize_summary(json_file['summary'])
        clean_data = {
            'id': json_file['id'],
            'url': json_file['url'],
            'clean_content': clean_content,
            'clean_summary': clean_summary
        }
        with open(DESTINATION+str(clean_data['id'])+'.json', 'w') as json_file:
            json.dump(clean_data, json_file)

preprocessing('data/raw/train/*', 'data/clean/train/')
preprocessing('data/raw/dev/*', 'data/clean/dev/')
preprocessing('data/raw/test/*', 'data/clean/test/')

