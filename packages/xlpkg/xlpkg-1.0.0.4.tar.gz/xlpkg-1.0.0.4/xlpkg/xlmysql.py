import mysql.connector
import pymysql
import sshtunnel

#pymysql 连接数据库
def f_conn0(v_host,v_port,v_user,v_password,v_database):
    try:
        conn = pymysql.connect( host=v_host,port=v_port,user=v_user,password=v_password, database=v_database, charset="utf8")
        return(conn)
    except Exception as e:
        print(f"{e}")
        return None

#mysql.connector 连接数据库
def f_conn1(v_host,v_port,v_user,v_password,v_database):
    try:
        conn = mysql.connector.connect( host=v_host,port=v_port,user=v_user,password=v_password, database=v_database, charset="utf8")
        return(conn)
    except Exception as e:
        print(f"{e}")
        return None

#ssh 连接数据库
def f_sshconn(v_host,v_port,v_user,v_password,v_database):
    with sshtunnel.SSHTunnelForwarder(('172.18.6.153',22),ssh_username='admin',ssh_password='wd123456',remote_bind_address=('172.18.2.135',3306)) as server:
        #print('01.SSH连接成功!')
        conn = mysql.connector.connect( host=v_host,port=v_port,user=v_user,password=v_password, database=v_database, charset="utf8")
        #print('02.MySQL数据库连接成功!')
        return(conn)
    pass

#查询
def f_query(conn,sql,args=None):
    cur=conn.cursor()
    cur.execute(sql,args)
    res=cur.fetchall()
    cur.close()
    return(res)

#插入单条数据
def f_insert(conn,sql,args=None):
    cur=conn.cursor()
    cur.execute(sql,args)
    conn.commit()
    cur.close()
    return(cur.rowcount)

#插入多条数据
def f_insertm(conn,sql,args=None):
    cur=conn.cursor()
    cur.executemany(sql,args)
    conn.commit()
    cur.close()
    return(cur.rowcount)

#删除
def f_del(conn,sql,args=None):
    cur=conn.cursor()
    cur.execute(sql,args[0])
    conn.commit()
    cur.close()
    return(cur.rowcount)

#更新
def f_update(conn,sql,args=None):
    cur=conn.cursor()
    cur.execute(sql,args)
    conn.commit()
    cur.close()
    return(cur.rowcount)
