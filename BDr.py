#! python3
# Rapahel Yang


# Testification:
# 1 Guosai 2013
# 2 General World
# 3 Sophie's World
# 4 STM32嵌入式微控制器快速上手
# 5 LabVIEW基础教程
# 6 LabVIEW工程实践技术



# 使用了以下的module：
# 1. requests
# 2. bs4
# 3. re

# For Debug begin
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

logging.disable(logging.CRITICAL)

# For Debug end

import requests, os, bs4, re, datetime, sys, shutil

from image2PDF.app.business.ImageProcessService import Convert2PDF

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



# Paste_Image_URL = 'http://202.119.70.51:88/png/png.dll?did=a174&pid=40C01F4995D263EFCD868F778B7D59393BD1CC6A751C85B465D95940401C92BEFC86831873301A554E12EA526E7C9C61707702D49E5E761BE8F90290ABC4FF15BA09F8027F770318FAB4B02BF7FAAE05CF62438646FCF3AE430631E3D8F320626817&jid=/000001.jpg&uf=ssr&zoom=0'
# 已經實現Paste_Image_URL自动获取；它位于在线阅读主页面的源码里，<body> 里面的<script> 中有提到。
#URL_IMGBEG = Paste_Image_URL[0:len(Paste_Image_URL)-24]


# 根據時間、書名產生文件夾名稱
time_now = datetime.datetime.now()
stamp_time = "%d%02d%02d_%02d%02d%02d" % (time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute, time_now.second)
speci_name = stamp_time + '_' + Book_Title
temp_folder = os.path.join('tmp_BDr',speci_name)
os.makedirs(temp_folder)

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

# 用requests 得到的variable，可以用len(VARIABLE.content) 来决定是否含有内容。

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

                # 用requests 得到的variable，可以用len(VARIABLE.content) 来决定是否含有内容。

                if(len(tmp_page.content) <= 200):
                        if( i ==1 ):
                                print('"%s" Part Not Found In This Book' % name_pages[j])
                        break

                with open(temp_folder + '/' + name_pages[j] + type_pages[5]%i + '.jpg', 'wb') as file:
                        file.write(tmp_page.content)
                        logging.debug('#DEBUG_正在输出第%d页\n\n', i)
        if( not ( i ==1 ) ):
                print('The "%s" Part of __%s__ is Finished\nThe Number of Page is %d\n\n' % (str(name_pages[j]), Book_Title, i) )




print('\n*************************\n*Entire Book Downloaded.*\n*************************\n')


Convert2PDF(os.path.join('.','tmp_BDr'))


