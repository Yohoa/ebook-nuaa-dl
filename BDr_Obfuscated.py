#! python3
import logging as O0O00OOO000OOO00O #line:41
O0O00OOO000OOO00O .basicConfig (level =O0O00OOO000OOO00O .DEBUG ,format =' %(asctime)s - %(levelname)s- %(message)s')#line:43
import requests as OO00O0000000000OO ,os as O0OOO0O0O00OO00O0 ,bs4 as OO000OO0OOOO0O000 ,re as OO0OO0O0O00OOOOOO ,datetime as OO000OOOOO0000O0O ,sys as OO00O0O0O00OO0O0O #line:46
O0O00OOO000OOO00O .disable (O0O00OOO000OOO00O .CRITICAL )#line:48
# !00001.jpg - 目录 "!%05d"
if (len (OO00O0O0O00OO0O0O .argv )==2 ):#line:61
        Reader_URL =str (OO00O0O0O00OO0O0O .argv [1 ])#line:62
else :#line:63
        if (len (OO00O0O0O00OO0O0O .argv )==1 ):#line:64
                print ('Input the URL You Get from Online Reader of Your Book')#line:65
                Reader_URL =input ()#line:66
        else :#line:67
                print ("\n*************************\n*   Nothing Finished.   *\n*************************\n")#line:68
                OO00O0O0O00OO0O0O .exit ()#line:69
Reader_res =OO00O0000000000OO .get (Reader_URL )#line:72
Reader_res .raise_for_status ()#line:73
Reader_res_bs =OO000OO0OOOO0O000 .BeautifulSoup (Reader_res .text ,"html.parser")#line:77
Get_Image_URL_Header =Reader_res_bs .select ('script')[6 ].getText ()#line:79
re_URL =OO0OO0O0O00OOOOOO .compile (r"http://202.119.70.51:88/png/png.dll.*/")#line:80
mo =re_URL .search (Get_Image_URL_Header )#line:81
URL_IMGBEG =mo .group ()#line:82
Book_Title =Reader_res_bs .select ('title')[0 ].getText ()#line:83
O0O00OOO000OOO00O .debug ('#DEBUG_Image_URL_Begin: '+URL_IMGBEG )#line:85
O0O00OOO000OOO00O .debug ('#DEBUG_Book_Title: '+Book_Title )#line:86
time_now =OO000OOOOO0000O0O .datetime .now ()#line:119
stamp_time ="%d%02d%02d_%02d%02d%02d"%(time_now .year ,time_now .month ,time_now .day ,time_now .hour ,time_now .minute ,time_now .second )#line:120
name_folder =stamp_time +'_'+Book_Title #line:121
O0OOO0O0O00OO00O0 .makedirs (name_folder )#line:122
type_pages =['cov%03d','bok%03d','leg%03d','fow%03d','!%05d','%06d','att%03d','bac%03d']#line:124
name_pages =['01_Cover_','02_BookTi_','03_Lega_','04_Prefa_','05_Menu_','06_Text_','07_Appendix_','08_Back_']#line:125
for j in range (0 ,7 ):#line:129
        for i in range (1 ,999999 ):#line:130
                tmp_page =OO00O0000000000OO .get (URL_IMGBEG +type_pages [j ]%i +'.jpg')#line:131
                O0O00OOO000OOO00O .debug ('Requesting Page %d:\n%s',i ,URL_IMGBEG +type_pages [j ]%i +'.jpg')#line:133
                while (not (tmp_page .status_code ==200 )):#line:135
                        tmp_page =OO00O0000000000OO .get (URL_IMGBEG +type_pages [j ]%i +'.jpg')#line:136
                        O0O00OOO000OOO00O .debug ('#DEBUG_下载出错, 正在重试: 第%d页\n\n\n\n\n\n\n',i )#line:139
                if (len (tmp_page .content )<=200 ):#line:147
                        if (i ==1 ):#line:148
                                print ('"%s" Part Not Found In This Book'%name_pages [j ])#line:149
                        break #line:150
                with open (name_folder +'/'+name_pages [j ]+type_pages [5 ]%i +'.jpg','wb')as file :#line:152
                        file .write (tmp_page .content )#line:153
                        O0O00OOO000OOO00O .debug ('#DEBUG_正在输出第%d页\n\n',i )#line:154
        if (not (i ==1 )):#line:155
                print ('The "%s" Part of __%s__ is Finished\nThe Number of Page is %d\n\n'%(str (name_pages [j ]),Book_Title ,i ))#line:156
print ('\n*************************\n*Everything is finished.*\n*************************\n')
#e9015584e6a44b14988f13e2298bcbf9


#===============================================================#
# Obfuscated by Oxyry Python Obfuscator (http://pyob.oxyry.com) #
#===============================================================#
