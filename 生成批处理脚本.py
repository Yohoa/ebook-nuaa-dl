import sys, os
file = open('BatProc.sh', 'w')
while(True):
    tmp_URL = input()
    if (tmp_URL== 'STOP'):
        print('This is the end')
        break
    file.write('python3 BDr.py \"' + tmp_URL + '\"\n')
file.close()
os.system(r'chmod +x "BatProc.sh"; ./BatProc.sh')

