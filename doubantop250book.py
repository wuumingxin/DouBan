import requests
import re
import time
import json


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text
        else:
            return None
    except Exception as e:
        return e

def parse_one_page(html):
    # <a\sclass="nbg"\shref="(.*?)".*?src="(.*?)".*?</a>.*?pl2">.*?title="(.*?)".*?pl">(.*?)</p>.*?rating_nums">(.*?)</span>.*?inq">(.*?)</span>
    pattern = re.compile('<a\sclass="nbg"\shref="(.*?)".*?src="(.*?)".*?</a>.*?pl2">.*?title="(.*?)".*?pl">(.*?)</p>.*?rating_nums">(.*?)</span>(?:.*?inq">(.*?)</span>)?',re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'url': item[0],
            'image': item[1],
            'title': item[2],
            'author': item[3],
            'score': item[4],
            'expl': item[5]
        }

def write_one_file(content):
    with open('doubantop250book.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')

def main(start):
    url = 'https://book.douban.com/top250?start=' + str(start)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_one_file(item)

if __name__=='__main__':
    for i in range(10):
        main(i*25)
        time.sleep(1)
