# _*_ coding: utf-8 _*_

################################################################
# Title：爬取赶集网济南市租房信息 地址：http://jn.ganji.com/fang1/  #
# Author： yz                                                  #
# Date：2017年 10月 26日 星期四 14:04:15 CST                     #
################################################################

import requests
from lxml import etree

def is_num_by_except(num):
    try:
        int(num)
        return True
    except:
        return False


def main():
    base_url = 'http://jn.ganji.com/fang1/o{}/'
    count = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }

    for page in range(1, 10):    # 251
        url = base_url.format(str(page))
        response = requests.get(url, headers=headers)
        s1 = etree.HTML(response.text)
        print("crawl " + url)

        house_location_list = s1.xpath('//*[@id="f_mew_list"]/div[6]/div[1]/div[3]/div[1]//dd[3]/span/a[1]/text()')
        house_price_list = s1.xpath('//*[@id="f_mew_list"]/div[6]/div[1]/div[3]/div[1]//dd[5]/div[1]/span[1]/text()')
        house_area_list1 = s1.xpath('//*[@id="f_mew_list"]/div[6]/div[1]/div[3]/div[1]//dd[2]/span[5]/text()')
        house_area_list2 = s1.xpath('//*[@id="f_mew_list"]/div[6]/div[1]/div[3]/div[1]//dd[2]/span[3]/text()')

        # house_location = ""     # 地点
        # house_area = ""         # 面积
        # house_price = ""        # 价格
        with open('JNInfo.txt', 'w') as file:
            for i in range(0, len(house_location_list)):
                house_location = house_location_list[i].strip()
                house_price = house_price_list[i]
                print(house_location)
                print(house_price)
                house_area = house_area_list1[i][:-1] if is_num_by_except(house_area_list1[i][:-1]) else house_area_list2[i][:-1]

                print(house_area)
                #file.write(str(count) + '\t' + house_location + '\t' + house_area + '\t' + house_price + '\n')
                print(str(count) + '\t' + house_location + '\t' + house_area + '\t' + house_price + '\n')
                count += 1

if __name__ == '__main__':
    main()







