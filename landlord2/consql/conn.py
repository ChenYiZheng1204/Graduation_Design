import pymysql
# db = pymysql.connect(host = "localhost",user="root",password="123456",database="card_game",charset='utf8')
# cursor = db.cursor()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
def get_name_id(username,userid):
    db = pymysql.connect(host="localhost", user="root", password="123456", database="card_game", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    Susername = None
    Suserpwd = None
    cursor.execute("select * from user_list")
    data = cursor.fetchall()
    for i in data:
        Susername = i[0]
        Suserpwd = i[1]
        if username != Susername:
            pass
        else:
            if userid != Suserpwd:
                db.close()
                return 1
    else:
        db.close()
        return 0

def resgin_name_id(username,userid):
    db = pymysql.connect(host="localhost", user="root", password="123456", database="card_game", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    Rename = None
    Repwd = None
    cursor.execute("select * from user_list")
    data = cursor.fetchall()
    for i in data:
        getsername = i[0]
        if getsername == username:
            db.close()
            return 0
    if username == '' or userid == '':
        db.close()
        return 1
    else:
        cursor.execute('insert into user_list (user_id,user_pwd) values ("%s","%s")' % (username, userid))
        cursor.execute("select * from user_list")
        data = cursor.fetchall()
        print(data)
        db.close()
        return 2

# print("数据库连接成功")
# insert_sql = cursor.execute("insert into user_list(user_id,user_pwd) values('qwe',123)")
# 运行sql语句
# db.commit()
# db.close()