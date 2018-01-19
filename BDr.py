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

# from image2PDF.app.business.ImageProcessService import Convert2PDF
from Image2PDF import convert_images2PDF_one_dir

def printline(): #划线
        line = "###########################################\n"
        print(line)

def welcome(): #欢迎
        project_loc = 'https://github.com/Yohoa/Download-Scanned-Book-from-the-Library-of-NUAA\n'
        project_recomm = 'Thank you for using, any kind of contribution including code contributing, public recommendation bug reports.\nPS: Experts of digital copyright affairs are needed. \n\n感谢您的使用，我们欢迎任何形式的贡献，包括贡献代码、推广和提交程序错误。此外，我们还希望得到数字版权方面专家的帮助。 \nRaphael\n'
        concise_intro = 'Input Book\'s URL and enter. More features including “Download with ISBN” are under development.\n\n请您键入您要下载的书目在阅读器时标签栏的网址后回车。更多功能正在开发中（包括直接输入ISBN下载图书等）。\n'
        printline()
        print("#About\n" + project_recomm)
        printline()
        print("项目地址：\n" + project_loc)
        print("Project Repository⬇\n" + project_loc)
        printline()
        print("#Concise Introduction\n" + concise_intro)
        printline()

def validate_namer(Namer): #有效化名字
        valid_name_re = re.compile(r'[\\/:"*?<>|]+')
        return valid_name_re.sub('_', Namer)

def catch_n_download(Reader_URL):
        try:
                Reader_res = requests.get(Reader_URL)
                Reader_res.raise_for_status()

                # 使用Beautiful Soup 解析網頁，通過Regex 精確查找連接位置。

                Reader_res_bs = bs4.BeautifulSoup(Reader_res.text, "html.parser")

                Get_Image_URL_Header = Reader_res_bs.select('script')[6].getText()
                re_URL = re.compile(r"http://202.119.70.51:88/png/png.dll.*/")
                mo = re_URL.search(Get_Image_URL_Header)
                URL_IMGBEG = mo.group()
                Book_Title = validate_namer(Reader_res_bs.select('title')[0].getText()) # 該行实现了自动获取Title的功能，并移除特殊符号。
                #Book_Title = "".join(x for x in Book_Title if (x.isalnum() or x in "._-")) #Remove the invalid characters in filename under some OS.

                # valid_name_re = re.compile(r'[\\/:"*?<>|]+')
                # Book_Title = valid_name_re.sub('_', Book_Title)

                # logging.debug('#DEBUG_Image_URL_Begin: ' + URL_IMGBEG)
                # logging.debug('#DEBUG_Book_Title: ' + Book_Title)



                # Paste_Image_URL = 'http://202.119.70.51:88/png/png.dll?did=a174&pid=40C01F4995D263EFCD868F778B7D59393BD1CC6A751C85B465D95940401C92BEFC86831873301A554E12EA526E7C9C61707702D49E5E761BE8F90290ABC4FF15BA09F8027F770318FAB4B02BF7FAAE05CF62438646FCF3AE430631E3D8F320626817&jid=/000001.jpg&uf=ssr&zoom=0'
                # 已經實現Paste_Image_URL自动获取；它位于在线阅读主页面的源码里，<body> 里面的<script> 中有提到。
                #URL_IMGBEG = Paste_Image_URL[0:len(Paste_Image_URL)-24]


                # 根據時間、書名產生文件夾名稱
                time_now = datetime.datetime.now()
                stamp_time = "%d%02d%02d_%02d%02d%02d" % (time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute, time_now.second)
                speci_name = stamp_time + '_' + Book_Title
                temp_folder = os.path.join('.','tmp_BDr',speci_name)
                os.makedirs(temp_folder)

                # 取自图书馆页面之逆向中的书本页面分类的文件名标志
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
                        printline()
                        print("Now downloading %s Part of the book\n" % name_pages[j])
                        for i in range(1, 999999): # 至多下载每部分包含九十九万九千九百九十九页的书
                                tmp_page = requests.get(URL_IMGBEG+type_pages[j]%i + '.jpg')

                                # logging.debug('Requesting Page %d:\n%s', i, URL_IMGBEG+type_pages[j]%i + '.jpg')

                                while ( not ( tmp_page.status_code == 200 ) ): # 用not 來進行邏輯判斷
                                        tmp_page = requests.get(URL_IMGBEG+type_pages[j]%i + '.jpg')


                                        # logging.debug('#DEBUG_下载出错, 正在重试: 第%d页\n\n\n\n\n\n\n', i)

                                # 1. 遇到「越界」的書頁，服務器仍然會返回「200」（代表成功的）狀態碼。
                                # 2. 通過下載的到的文件大小來判斷下載進程是否越界。
                                # 3. 未針對正文首頁序號並非「1」的頁面進行workaround ，這意味著目前（Thu, 31
                                # Aug 2017 12:58:40 +0800）該腳本針對形如「毛泽东选集.第二卷/毛泽东著」
                                # 這樣的書籍，將會異常退出。

                                # 用requests 得到的variable，可以用len(VARIABLE.content) 来决定是否含有内容。

                                if(len(tmp_page.content) <= 200):
                                        if( i ==1 ):
                                                print('"%s" Part not found.\n' % name_pages[j])
                                                print('"本书没有%s部分。 \n\n' % name_pages[j])
                                        break

                                with open(temp_folder + '/' + name_pages[j] + type_pages[5]%i + '.jpg', 'wb') as file:
                                        file.write(tmp_page.content)
                                        # logging.debug('#DEBUG_正在输出第%d页\n\n', i)
                        if( not ( i ==1 ) ):
                                print('"%s" Part of "%s" is Finished.\nEventually, %d Pages are fetched All.\n\n' % (str(name_pages[j]), Book_Title, i))
                                print('《%s》的"%s"部分已经获取完成。\n该部分共%d页。\n\n' % (Book_Title, str(name_pages[j]), i))

                print('\n*************************\n*Entire Book Downloaded.*\n*************************\n')
                print('\n*************************\n*全书下载完成；开始生成PDF档。*\n*************************\n')
        except:
                print("\nExceptions happened in downloading process. Please report this bug including the book title and your experience to mailto#zhizhiyang.cn . Both Chinese and English are capable. Thank you for your feedback.\n")
                print("在下在抓取期间出现了无法挽回的故障。请您携您要下载的书以及您遭遇的出错经过致信mailto#zhizhiyang.cn 与在下之开发者。中英文皆可，感谢您的反馈！\n")

        try:
                convert_images2PDF_one_dir(temp_folder, save_name=(Book_Title + "_raf1.pdf"))
                shutil.move(os.path.join(temp_folder, Book_Title + "_raf1.pdf"), os.path.join('.', Book_Title + "_raf1.pdf"))
                printline()
                print("\nConversion is conducted successfully.\n转换成功。请您查看本程序路径下相随的PDF 档。\n")
                print("Some clean are needed to be done manually.\n您需要做一下清理工作。")
        except:
                print("\nExceptions happened in conversion process. Please report this bug including the book title and your experience to mailto#zhizhiyang.cn . Both Chinese and English are capable. Thank you for your feedback.\n")
                print("转换期间出现了问题。请您携您要下载的书以及您遭遇的出错经过致信mailto#zhizhiyang.cn 与开发者。中英文皆可，感谢您的反馈！\n")

# Main program


if (len(sys.argv) == 2):
        Reader_URL = str(sys.argv[1])
else:
        if(len(sys.argv) == 1):
                welcome()
                Reader_URL = input()
                # if (len(Reader_URL) == 0 or (Reader_URL.find('http') == -1 )):
                #         print("\n*************************\n Redirect to img2PDF now.  \n*************************\n")
                #         Convert2PDF(os.path.join('.','tmp_BDr'))
                #         sys.exit()
        else:
                print("\n*************************\n*   Nothing Finished.   *\n*************************\n")
                sys.exit()


catch_n_download(Reader_URL)
