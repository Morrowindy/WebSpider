import re
import requests
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
}
base_url = 'http://maoyan.com/board/4?offset='
pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                     + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                     + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
SLEEP_TIME = 2
result_df = list()


def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image_path': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }


def process(url):
    html = get_one_page(url)
    generator = parse_one_page(html)
    result_df.extend(generator)


def main():
    for i in range(10):
        process(base_url + str(i))
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
    writer = pd.ExcelWriter('maoyan100.xlsx')
    result_df = pd.DataFrame(result_df)
    result_df.to_excel(writer, index=False)
    writer.save()
    print(result_df.info())
