from bs4 import BeautifulSoup
import urllib.request
import lxml
import time
import datetime
def generate_url_list():
    url_list = ['http://jbk.39.net/bw_t1']
    for i in range(1, 842):
        url_list.append('http://jbk.39.net/bw_t1_p%d#ps' % i)
        # print(url_list)
    return url_list


def generate_disease(page,url_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}

    # page = 0
    disease_list = []

    # 遍历每个网页
    for iii in range(0,len(url_list)):
        try:
            # page += 1
            request = urllib.request.Request(url=url_list[iii], headers=headers)
            data = urllib.request.urlopen(request).read()
            soup = BeautifulSoup(data, 'lxml', from_encoding='utf8')
            list_dt = soup.find_all('dt', class_='clearfix')

            # 遍历当前网页
            count=0
            for i in range(len(list_dt)):
                count+=1
                try:
                    dict = {}
                    dict['page'] = page
                    for child in list_dt[i].children:
                        if child.name == 'h3':
                            new_url = (child.contents[0])['href']
                            new_request = urllib.request.Request(url=new_url, headers=headers)
                            new_data = urllib.request.urlopen(new_request).read()
                            new_soup = BeautifulSoup(new_data, 'lxml', from_encoding='utf8')
                            div = new_soup.find('div', class_='tit clearfix', style='height:auto;')
                            # print(div.a.h1.get_text())
                            for tag in div.children:
                                if tag.name == 'a':
                                    dict['name'] = tag.h1.get_text()
                                if tag.name == 'h2':
                                    dict['nickname'] = tag.get_text()
                    disease_list.append(dict)
                except urllib.error.HTTPError as e:
                    print(count,'发生了httperror')
                except Exception as e:
                    print(count,'发生了错误：',str(e))

            # 每一百页保存在文件
            # if page%100 == 0 or iii == len(url_list)-1:

            if True:
                with open('dddd.txt', 'a', encoding='utf-8') as f:
                    for item in disease_list:
                        if 'nickname' in item.keys():
                            f.write(str(item['page']) + "   " + item['name'] + "   " + item['nickname'] + '\n')
                        else:
                            f.write(str(item['page']) + "   " + item['name'] + '\n')
                    disease_list = []
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),page, "页完成")

        except urllib.error.HTTPError as e:
            print(page,'页发生httperror错误')
        except Exception as e:
            print(page,'页发生未知错误:',str(e))
    for item in disease_list:
        print(item)
    print('程序完成')

# def easy(url):
#     disease_list = []
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
#     request = urllib.request.Request(url=url, headers=headers)
#     data = urllib.request.urlopen(request).read()
#     soup = BeautifulSoup(data, 'lxml', from_encoding='utf8')
#     list_dt = soup.find_all('dt', class_='clearfix')
#
#     # 遍历当前页
#     count=0
#     for i in range(len(list_dt)):
#         count +=1
#         try:
#             for child in list_dt[i].children:
#                 if child.name == 'h3':
#                     new_url = (child.contents[0])['href']
#                     new_request = urllib.request.Request(url=new_url, headers=headers)
#                     new_data = urllib.request.urlopen(new_request).read()
#                     new_soup = BeautifulSoup(new_data, 'lxml', from_encoding='utf8')
#                     div = new_soup.find('div', class_='tit clearfix', style='height:auto;')
#                     # print(div.a.h1.get_text())
#                     for tag in div.children:
#                         if tag.name == 'a':
#                             print(tag.h1.get_text(),end='')
#                         if tag.name == 'h2':
#                             print(tag.get_text(),end='')
#                     print()
#         except Exception as e:
#             print(count,'出错')
        # break



                # for child in list_dt[1].children:
                #     if child.name == 'h3':  # 存储了病名
                #         tag_a = child.contents[0]

                # for i in range(len(list_dt[0].contents)):
                #     print(i,list_dt[0].contents[i])
                # for i in range(len(list_dt[1].contents)):
                #     print(i,list_dt[1].contents[i])

                #     dict = {}
                #     tag1 = list_dt[i].contents[5]
                #     nickname = tag1['title']
                #     tag2 = list_dt[i].contents[1].contents[0]
                #     name = tag2['title']
                #
                #     dict["id"] = i
                #     dict["name"] = name
                #     dict["nickname"] = nickname
                #
                #     disease_list.append(dict)
                # for i in range(len(disease_list)):
                #     print(disease_list[i])


if __name__ == '__main__':
    flag = 1
    if flag == 1:
        url_list = generate_url_list()
        m = 839
        n = 1
        for i in range(n):
            generate_disease(m+i,url_list[m+i-1:m+i])
    else:
        easy('http://jbk.39.net/bw_t1_p9#ps')
