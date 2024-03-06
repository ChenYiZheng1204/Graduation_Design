import pymysql

class Dbutl(object):
    connection = None

    def connection(cls,database):
        if cls.connection is None:
            cls.connection = pymysql.connect(host="localhost", user="root", password="123456", database=database, charset='utf8')
            return cls.connection
    @classmethod
    def __closs__conn(cls):
        if cls.connection:
            cls.connection.close()
            cls.connection = None
    # @classmethod
    # def __