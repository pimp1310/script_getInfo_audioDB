import sys
import os
import time
import xbmcaddon

def log(path, msg):
    now = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(time.time()))
    f = open(path, 'a+')
    f.write(str(now) + '   ' + msg + '\n')
    f.close()