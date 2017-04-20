import requests
import re
from multiprocessing import Pool


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Accept': 'application/json',
    'X-Request': 'JSON',
    'X-Requested-With': 'XMLHttpRequest'
}
params = {
    'max': '',
    'limit': '20',
}



def get_pins():
    pins = []
    # 森女
    url = 'http://huaban.com/explore/sennv/'
    html = requests.get(url, params=params, headers=headers)

    for i in html.json()['pins']:
        print(i['pin_id'])
        pins.append(i['pin_id'])

    while True:
        try:
            last_pin_id = html.json()['pins'][-1]['pin_id']
            params['max'] = last_pin_id
            html = requests.get(url, params=params, headers=headers)
            for i in html.json()['pins']:
                print(i['pin_id'])
                pins.append(i['pin_id'])
        except:
            return pins


def get_img_urls(pin):
    img_urls = []
    url = 'http://huaban.com/pins/{}/'.format(pin)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }
    html = requests.get(url, headers=headers)
    app_page_pin = re.findall("app\.page\[\"pin\"] = (.*?);", html.text)[0]
    keys = re.findall("\"key\":\"(.*?)\"", app_page_pin)
    for i in keys:
        img_urls.append('http://img.hb.aicdn.com/%s' % i)
        print(i)
    return img_urls



def download_imgs(img_url):
    html = requests.get(img_url)
    img_name = re.split('/', img_url)[-1]
    print('正在下载： ' + img_url)
    with open('%s.jpg' % img_name, 'wb') as img:
        img.write(html.content)



def main():
    pins = get_pins()
    img_urls = []
    for pin in pins:
        img_urls.extend(get_img_urls(pin))
    # 单进程下载
    # for img_url in img_urls:
    #     download_imgs(img_url)

    # 多进程下载
    pool = Pool()
    pool.map(download_imgs, img_urls)



if __name__ == '__main__':
    main()

