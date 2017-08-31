import PIL
import os
from reportlab.pdfgen import canvas









def mapd(nof):
    nop = 0
    c = canvas.Canvas('E:\\Q%s.pdf'%nof)
    while nop < len(os.listdir('E:\\Q%s'%nof)):
        c.drawImage('E:\\Q%s\\%s.jpg'%(nof,nop),0,0,width=,height=)
        c.showPage()
        nop = nop + 1
    else:
        c.save()
for i in range(X,Y): #XY为重复区间，本程序要求图片按数字顺序排列
  mapd(i)