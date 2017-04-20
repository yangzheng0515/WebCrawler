import requests
from lxml import etree
import os
import xlwt

# job location company salary link      detail

keyword = 'web'

job = []
location = []
company = []
salary = []
link = []
detail = []

for page in range(1, 15):
    url = 'http://www.shixiseng.com/interns?k={}&p={}'.format(keyword, page)
    response = requests.get(url)
    s = etree.HTML(response.text)

    job_names = s.xpath('//*[@id="load_box_item"]/div/div/div/a/h3/text()')
    locations = s.xpath('//*[@id="load_box_item"]/div/div/p/span[1]/span/text()')
    companies = s.xpath('//*[@id="load_box_item"]/div/div/div/p/a/text()')
    salaries = s.xpath('//*[@id="load_box_item"]/div/div/p/span[2]/text()')
    salaries = salaries[1::2]  # 数组隔一个删一个
    for i, item in enumerate(salaries):
        salaries[i] = item.replace('\n\n', '')
    links = s.xpath('//*[@id="load_box_item"]/div/div/div/a/@href')
    for i, item in enumerate(links):
        links[i] = 'http://www.shixiseng.com' + item

    job.extend(job_names)
    location.extend(locations)
    company.extend(companies)
    salary.extend(salaries)
    link.extend(links)

for url in link:
    response = requests.get(url)
    s = etree.HTML(response.text)
    details = s.xpath('//*[@id="container"]/div[1]/div[1]/div[3]//text()')
    detail_str = ''
    for i in details:
        detail_str += i
    detail.append(detail_str)


# print(job)
# print(location)
# print(company)
# print(salary)
# print(link)
# print(detail)

book = xlwt.Workbook()
sheet = book.add_sheet('sheet', cell_overwrite_ok=True)
path = '/home/yz/PycharmProjects/WebCrawler/shixiseng'
os.chdir(path)

j = 0
for i in range(len(job)):
    try:
        sheet.write(i + 1, j, job[i])
        sheet.write(i + 1, j + 1, location[i])
        sheet.write(i + 1, j + 2, company[i])
        sheet.write(i + 1, j + 3, salary[i])
        sheet.write(i + 1, j + 4, link[i])
        sheet.write(i + 1, j + 5, detail[i])
    except Exception as e:
        print('出现异常：' + str(e))
        continue
book.save('web.xls')
