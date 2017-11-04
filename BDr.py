#! python3
# Rapahel Yang


# Testification:
# 1 Guosai 2013
# 2 General World
# 3 Sophie's World
# 4 STM32嵌入式微控制器快速上手
# 5 LabVIEW基础教程
# 6 LabVIEW工程实践技术


#	To-do List:
#✓	2. 支持自动判别页码数目
#✓	3. 支持自动获取标题
#	4. 支持自动合成PDF 档案
#	5. 优化交互方式，建议外程序外外置json 配置文档
#✓	1. 支持全书的下载
#✓	5. 支持直接从书籍介绍界面解析
# 	6. 支持合成PDF 档案时加入目录
#	7. 支持cli 搜索图书，并提供一站式下载
#	8. 支持多线程下载
#✓	9. 阅读版权法、著作权法
#-	10. 支持多本图书批量
#	11. 支持所有「关键词」图书批量下载
#	12. 支持所有图书一键下载


# Tips for Improvements:
# 	1. 网页title 就是书名✓
#	2. 图片地址是绝对地址，根据观测，不会变化✓
#	3. 目录的图片地址，是原链接，将后部的序号参数左侧第一个0改为! 后所得。✓
#	4. 在线阅读界面是动态地址！
#       5. 发现了从ISBN到目标位址的方法！
#               只需要提供ISBN http://202.119.70.51:8088/servlet/isExitJson?isbn=978-7-121-22162-0

# 使用了以下的module：
# 1. requests
# 2. bs4
# 3. re

import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')


import requests, os, bs4, re, datetime, sys

logging.disable(logging.CRITICAL)

# 根据http://202.119.70.51:8088/Jpath_sky/js/jpathBrowser5.js?v=1.1 描述
# cov001.jpg - 封面 - 两页 -  "cov%03d"%i
# bok001.jpg - 书名页 "bok%03d"
# leg001.jpg - 版权页 "leg%03d"
# fow001.jpg - 前言 "fow%03d"
# !00001.jpg - 目录 "!%05d"
# 000001.jpg - 正文 "%06d"
# att001.jpg - 附录 "att%03d"
# bac001.jpg - 封底 "bac%03d"


if (len(sys.argv) == 2):
        Reader_URL = str(sys.argv[1])
else:
        if(len(sys.argv) == 1):
                print('Input the URL You Get from Online Reader of Your Book')
                Reader_URL = input()
        else:
                print("\n*************************\n*   Nothing Finished.   *\n*************************\n")
                sys.exit()


Reader_res = requests.get(Reader_URL)
Reader_res.raise_for_status()

# 使用Beautiful Soup 解析網頁，通過Regex 精確查找連接位置。

Reader_res_bs = bs4.BeautifulSoup(Reader_res.text, "html.parser")

Get_Image_URL_Header = Reader_res_bs.select('script')[6].getText()
re_URL = re.compile(r"http://202.119.70.51:88/png/png.dll.*/")
mo = re_URL.search(Get_Image_URL_Header)
URL_IMGBEG = mo.group()
Book_Title = Reader_res_bs.select('title')[0].getText() # 該行实现了自动获取Title的功能

logging.debug('#DEBUG_Image_URL_Begin: ' + URL_IMGBEG)
logging.debug('#DEBUG_Book_Title: ' + Book_Title)


# Book_Title = "苏菲的世界"
# 已經實現Book_Title自动获取；它位于在线阅读主页面的title

# Paste_Image_URL = 'http://202.119.70.51:88/png/png.dll?did=a174&pid=40C01F4995D263EFCD868F778B7D59393BD1CC6A751C85B465D95940401C92BEFC86831873301A554E12EA526E7C9C61707702D49E5E761BE8F90290ABC4FF15BA09F8027F770318FAB4B02BF7FAAE05CF62438646FCF3AE430631E3D8F320626817&jid=/000001.jpg&uf=ssr&zoom=0'
# 已經實現Paste_Image_URL自动获取；它位于在线阅读主页面的源码里，<body> 里面的<script> 中有提到。
#URL_IMGBEG = Paste_Image_URL[0:len(Paste_Image_URL)-24]



# Article_num = 269
# 已經實現Article_num 的自动判断。
# 用requests 得到的variable，可以用len(VARIABLE.content) 来决定是否含有内容。

# imgUrlList = [];

# for i in range(1, Article_num+1) :
# 	URL = URL_IMGBEG + "%06d"%i + ".jpg"
# 	imgUrlList.append(URL)


# os.system("mkdir "+'/Users/Yangzhizhi/Documents/Books/'+Book_Title)

# for i, j in enumerate(imgUrlList):
#     with open('/Users/Yangzhizhi/Documents/Books/'+Book_Title+'/'+"Article_%06d"%(i+1)+".jpg", 'wb') as file:
#         Page_s_temp = requests.get(j)
#         file.write(Page_s_temp.content)
#         print(str(Page_s_temp.status_code)+'\n')
# print("Task Finished\n ")

# 根據時間、書名產生文件夾名稱
time_now = datetime.datetime.now()
stamp_time = "%d%02d%02d_%02d%02d%02d" % (time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute, time_now.second)
name_folder = stamp_time + '_' + Book_Title
os.makedirs(name_folder)

type_pages = ['cov%03d',
              'bok%03d',
              'leg%03d',
              'fow%03d',
              '!%05d',
              '%06d',
              'att%03d',
              'bac%03d'
              ]
name_pages = [  '01_Cover_',
                '02_BookTi_',
                '03_Lega_',
                '04_Prefa_',
                '05_Menu_',
                '06_Text_',
                '07_Appendix_',
                '08_Back_'
                ]

# 下载頁面

for j in range(0, 7):
        for i in range(1, 999999):
                tmp_page = requests.get(URL_IMGBEG+type_pages[j]%i + '.jpg')

                logging.debug('Requesting Page %d:\n%s', i, URL_IMGBEG+type_pages[j]%i + '.jpg')

                while ( not ( tmp_page.status_code == 200 ) ): # 用not 來進行邏輯判斷
                        tmp_page = requests.get(URL_IMGBEG+type_pages[j]%i + '.jpg')


                        logging.debug('#DEBUG_下载出错, 正在重试: 第%d页\n\n\n\n\n\n\n', i)

                # 1. 遇到「越界」的書頁，服務器仍然會返回「200」（代表成功的）狀態碼。
                # 2. 通過下載的到的文件大小來判斷下載進程是否越界。
                # 3. 未針對正文首頁序號並非「1」的頁面進行workaround ，這意味著目前（Thu, 31
                # Aug 2017 12:58:40 +0800）該腳本針對形如「毛泽东选集.第二卷/毛泽东著」
                # 這樣的書籍，將會異常退出。

                if(len(tmp_page.content) <= 200):
                        if( i ==1 ):
                                print('"%s" Part Not Found In This Book' % name_pages[j])
                        break

                with open(name_folder + '/' + name_pages[j] + type_pages[5]%i + '.jpg', 'wb') as file:
                        file.write(tmp_page.content)
                        logging.debug('#DEBUG_正在输出第%d页\n\n', i)
        if( not ( i ==1 ) ):
                print('The "%s" Part of __%s__ is Finished\nThe Number of Page is %d\n\n' % (str(name_pages[j]), Book_Title, i) )




print('\n*************************\n*Everything is finished.*\n*************************\n')










