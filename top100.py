import requests
from requests import RequestException
import re
import json
from multiprocessing import Pool

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}


def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?>.*?name"><a.*?data-act.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(\d+)</i>.*?</dd>',
        re.S)
    items = pattern.findall(html)
    print(items)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip(),
            'time': item[4],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    with open('result.txt', 'a',
              encoding='utf-8') as f:  # 关键write() argument must be str, not dict  (就是write（）里content必须是字符串所以需要json.doumps)
        f.write(str(content) + '\n')  # 相同作用表达  f.write(json.doumps(content,esure_ascii=False),'\n')
        f.close


# 1.print(json.dumps(content)) #2.print(json.loads(content)) 总结关键dumps是将dict转化成str格式，loads是将str转化成dict格式。

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    #  print(html)
    for item in parse_one_page(html):
        #        print(item)
        write_to_file(item)


if __name__ == '__main__':
    #    pool=Pool()
    #   pool.map(job,[i*10 for i in range(2)])
    for i in range(10):
        main(i * 10)