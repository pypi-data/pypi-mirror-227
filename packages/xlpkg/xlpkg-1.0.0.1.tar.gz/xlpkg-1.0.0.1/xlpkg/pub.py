from datetime import datetime  as dt
import traceback
import random
import os
import webbrower
import subprocess

"""
01 f_cmd(cmd)  执行系统命令
02 f_rdint(m,n) 生成m,n范围内的随机整数
03 f_lpad(s,n) 在字符串前补0。s：字符串;n:字符串总长度。
04 f_phone()  生成随机手机号码
05 f_dt(type) 返回当前日期、时间。
"""
def f_msgok(msg):
    pass

def f_msgokcancel(msg):
    pass

def f_msgyesno(msg):
    pass

def f_msgokcancel(msg):
    pass

#关于
def f_msgabout(msg):
    QMessageBox.about('about',msg)
    pass

#错误
def f_msgabout(msg):
    QMessageBox.critical('Error',msg)
    pass

#警告
def f_msgwarn(msg):
    QMessageBox.warning('Warn',msg)
    pass

#消息
def f_msginfo(msg):
    QMessageBox.information('Info',msg)
    pass

#消息
def f_msgquestion(msg):
    QMessageBox.question('Question',msg)
    pass

#列举
def f_enumerate(lst):
    for i,el in enumerate(lst):
        print(i,el)
    pass

#字符串左对齐、居中对齐、右对齐。
def f_align(s,n,flag):
    if(flag==-1):
        op="<"+str(n)
        return(format(s,op))
    if(flag==0):
        op="^"+str(n)
        return(format(s,op))
    if(flag==1):
        op=">"+str(n)
        return(format(s,op))
    pass

#执行系统命令
def f_cmd(cmd):
    try:
        os.system(cmd)
    except Exception as e:
        print('Error:',e)
    pass

#执行系统命令
def f_subproc(cmd):
    try:
        subprocess.Popen(cmd)
    except Exception as e:
        print('Error:',e)
    pass

#执行系统命令
def f_webbrower(url):
    try:
        webbrower.pen(url)
    except Exception as e:
        print('Error:',e)
    pass
#随机整数
def f_rdint(m,n):
    return(random.randint(m,n))
    pass

#字符前补0。s：字符串;n:字符串总长度。
def f_lpad(s,n):
    return(s.zfill(n))
    pass

#随机手机号码
def f_phone():
    return('1'+str(f_rdint(3,9))+str(f_rdint(0,9))+f_lpad(str(f_rdint(1,99999999)),8))
    #各运营商不同号段
    '''
    移动
    134(0-8)、135、136、137、138、139、
    147、
    150、151、152、157、158、159、
    172、178、
    182、183、184、187、188、
    195、197、198
    联通：
    130、131、132、
    145、155、156、
    166、
    175、176、
    185、186、
    196
    电信：
    133、149、153 、
    173、177、
    180 、181 、189、
    190、191、193、199
    '''
    pass

#返回当前日期、时间
def f_dt(type):
    if(type==None or type==0):
        return(dt.now().strftime('%Y%m%d %H:%M:%S'))
    if(type==1):
        return(dt.now().strftime('%Y%m%d'))
    if(type==2):
        return(dt.now().strftime('%H:%M:%S'))
    if(type==3):
        return(dt.now())
    if(type=='y' or type=='Y'):
        return(dt.now().strftime('%Y'))
    if(type=='m'):
        return(dt.now().strftime('%m'))
    if(type=='d' or type=='D'):
        return(dt.now().strftime('%d'))
    if(type=='H'):
        return(dt.now().strftime('%H'))
    if(type=='M'):
        return(dt.now().strftime('%M'))
    if(type=='S'):
        return(dt.now().strftime('%S'))

    if(type=='long'):#长格式
        return(dt.now())
    if(type=='ts'):#当前日期时间转时间戳
        now=dt.now()
        return(dt.timestamp(now))

#将指定的时间戳转成日期时间
def f_tstodt(ts):
        return(dt.fromtimestamp(ts))
    
#将指定的日期时间转成时间戳
def f_dttots(dts):
        return(dt.timestamp(dts))

#返回错误文件名、行号、错误类型、错误消息
def f_errorfileline(e):
    
    print('【Error】\n01. file:\033[91m{}\033[0m'.format(e.__traceback__.tb_frame.f_globals["__file__"]),' line:\033[91m{}\033[0m'.format(e.__traceback__.tb_lineno))
    print('02.',type(e))
    print('03.',str(e))
    print('04.')
    traceback.print_exc()
    pass
