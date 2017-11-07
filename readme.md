# Download-Scanned-Book-from-the-Library-of-NUAA
## Raphael Yang

### Introduction
These Python applet can help you with downloading and converting scanned books from the library of Nanjing University of Aeronautics and Astronautics.

It should be also mentioned that Liu.Qi's image2pdf script from GitHub have been quoted.

### Issues
1. Pages will be disorders when generating PDF. (Trying to both solving by myself and ask Liu.Qi for help)

### Imported Modules
1. PIL
2. reportlab
3. requests
4. bs4
5. re

### To-do List:
2. 支持自动判别页码数目✓
3. 支持自动获取标题✓
4. 支持自动合成PDF 档案
5. 优化交互方式，建议外程序外外置json 配置文档
1. 支持全书的下载✓
5. 支持直接从书籍介绍界面解析✓
6. 支持合成PDF 档案时加入目录
7. 支持cli 搜索图书，并提供一站式下载
8. 支持多线程下载
10. 支持多本图书批量操作
11. 支持所有「关键词」图书批量下载
12. 支持所有图书一键下载



### Tips for Improvements:
1. 网页title 就是书名✓
2. 图片地址是绝对地址，根据观测，不会变化✓
3. 目录的图片地址，是原链接，将后部的序号参数左侧第一个'0'改为'!'后所得。✓
4. 在线阅读界面是动态地址！
5. 发现了从ISBN到目标位址的方法！
	1. 只需要提供ISBN http://202.119.70.51:8088/servlet/isExitJson?isbn=978-7-121-22162-0

6. 根据http://202.119.70.51:8088/Jpath\_sky/js/jpathBrowser5.js?v=1.1 描述
	a. cov001.jpg - 封面 - 两页 -  "cov%03d"%i
	
	b. bok001.jpg - 书名页 "bok%03d"
	
	c. leg001.jpg - 版权页 "leg%03d"
	
	d. fow001.jpg - 前言 "fow%03d"
	
	e. !00001.jpg - 目录 "!%05d"
	
	f. 000001.jpg - 正文 "%06d"
	
	g. att001.jpg - 附录 "att%03d"
	
	h. bac001.jpg - 封底 "bac%03d"
