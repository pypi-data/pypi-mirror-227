#生成密码文件
from faker import Faker
from xlpkg import pub

def f_genpwd(fname,c):
    n=0
    fk=Faker(local='zh-cn')
    with open(fname,'w') as f1:
        while(n<c):
            f1.write(fk.password()+'\n')
            n+=1
    pass

#1.检查密码长度
def f_checkpwdlen(str):
    l=len(str)
    if(l<8):
        return(True)
    if(l>16):
        return(True)
    pass


#【判断密码是否符合要求】
x0="`-=()+[]\{}|;':\",/<>" #非密码字符 20个
x1="0123456789"#数字10个
x2="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"#字母52个
x3="~!@#$%^&*_.?" #密码字符12个

#检查密码是否为非密码字符,数字,字母,密码字符。
def f_checkpwd(str,x):
    for letter in str:
        if(letter in x):
            ret=True
            return(ret)
    pass

