# 从南京航空航天大学的图书馆下载其数字馆藏——扫描版图书
## Raphael Yang

### Introduction | 简介
These Python applet can help you with downloading and converting scanned books from the library of Nanjing University of Aeronautics and Astronautics.

这个Python 小程序（BDr.py）可以帮助你下载南京航空航天大学（南航大）的扫描版图书，并转换生成PDF文档。

It should be also mentioned that Liu.Qi's image2PDF script from GitHub have been quoted. https://github.com/liuqi0725/image2PDF

这个仓库引用了Liu Qi 开源的image2PDF 组件。

### How to use | 您需如何使用
1. 将这个程序在你的平台上运行起来。
	1. 这个程序在macOS 下Python3.6 与Windows 10 下的WinPython 环境下都被Raf. 成功实践。
2. 根据提示，输入“书目在阅读器时标签栏的网址后回车”或直接回车。
3. 静候佳音。
4. 完成“已知的故障” 中“2. 这些清理工作……”中所提到的清理工作。

### Issues | 已知的故障
1. _The order of pages will be disorders when generating PDF. (Appears both on Mac and Pythonista iOS. Trying to both solving by myself and ask Liu.Qi for help)_ ←这个问题已经被解决。
2. 这些清理工作需要在每次转换后手动进行：
	1. 将tmp_BDr 文件夹清空，以避免下次运行时再次针对该书本进行转换。
	2. 将PDF 文档拿走，以避免下次运行时进行的转换将该PDF 文档内容覆盖。
	
### Imported Modules | 需要导入的模块
1. PIL
2. reportlab
3. requests
4. bs4
5. re

### To-do List | 期待完成的功能
2. 自动判别页数✓
3. 自动获取标题✓
4. 支持自动合成PDF 档案✓
5. 优化交互方式，建议外程序外外置json 配置文档
1. 支持全书的下载✓
5. 支持直接从书籍介绍界面解析书籍的信息✓
7. 支持cli 搜索图书，并提供一站式下载
8. 支持多线程下载
10. 支持多本图书批量操作
11. 支持所有「关键词」图书批量下载
12. 支持所有图书一键下载



### Tips for Improvements | 开发中总结的一些经验
1. 网页title 就是书名✓
2. 图片地址是绝对地址，根据观测，不会变化✓
3. 目录的图片地址，是原链接，将后部的序号参数左侧第一个'0'改为'!'后所得。✓
4. 在线阅读界面是动态地址！
5. 发现了从ISBN到目标位址的方法！*（还未实用这个发现）*
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
7. 这个程序被建议通过（较为规范的）C语言重新开发一遍。
