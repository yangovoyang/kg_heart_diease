from bs4 import BeautifulSoup
import urllib.request
import re
import xlsxwriter


def generate_url():
    url_list = []
    with open('心血管疾病链接.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        url_list.append(line)
    return url_list


def download_page(url, page):
    global result
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
        request = urllib.request.Request(url=url, headers=headers)
        data = urllib.request.urlopen(request).read()
        soup = BeautifulSoup(data, 'lxml', from_encoding='utf8')
        # 获取病名和别名
        div = soup.find('div', class_='tit clearfix')
        diease_alias = ''
        diease_name = ''
        for tag in div.children:
            if tag.name == 'a':
                for sub in tag.children:
                    if sub.name == 'h1':
                        diease_name = sub.get_text()
            if tag.name == 'h2':
                diease_alias = tag.get_text()[1:-1]
        # 获取典型症状和相关症状
        dl = soup.find('dl', class_='links')
        diease_typical_symptom = ''
        diease_relative_symptom = ''
        diease_early_symptom = ''
        diease_late_symptom = ''

        dds = dl.find_all('dd')
        for tag in dds:
            if tag.i.get_text() == '典型症状：':
                diease_typical_symptom = tag.get_text()
            if tag.i.get_text() == '早期症状：':
                diease_early_symptom = tag.get_text()
            if tag.i.get_text() == '晚期症状：':
                diease_late_symptom = tag.get_text()
            if tag.i.get_text() == '相关症状：':
                diease_relative_symptom += '相关症状：'
                a = tag.find_all('a')
                for indexx, subtag in enumerate(a):
                    diease_relative_symptom += subtag['title']
                    if indexx != len(a) - 1:
                        diease_relative_symptom += ','
        result.append([diease_name, url, diease_alias, diease_typical_symptom, diease_early_symptom, diease_late_symptom, diease_relative_symptom])
    except Exception as e:
        print('page', page, '错误', repr(e))


def download(url_list):
    for page, url in enumerate(url_list):
        download_page(url_list[page], page + 1)
        print('第', page, '页完成')


if __name__ == '__main__':
    result = []
    # url_list = generate_url()
    download(generate_url())
    workbook = xlsxwriter.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet()
    for i in range(len(result)):
        for j in range(len(result[i])):
            worksheet.write(i, j, result[i][j])
    workbook.close()
