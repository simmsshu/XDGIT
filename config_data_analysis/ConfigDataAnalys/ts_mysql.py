import pymysql
import logging
import datetime
import time
# from getConfigData import decrypt
logging.basicConfig(level=logging.INFO)

# def decrypt(encrypted, key_int):
#     decrypted = encrypted ^ key_int
#     length = (decrypted.bit_length() + 7) // 8
#     decrypted_bytes = int.to_bytes(decrypted, length, 'big')
#     return decrypted_bytes.decode()

class MongoConfigDetailInfo():

    @classmethod
    def set_cofnig(cls,config):
        cls.host = config.get("mysql","host")
        cls.user = config.get("mysql","user")
        # password = eval(config.get("mysql","password"))
        # cls.password = decrypt(*password)
        cls.password = config.get("mysql","password")
        cls.db = config.get("mysql","db")

    @classmethod
    def connectDB(cls):
        try:
            cls.db = pymysql.connect(host = cls.host,user = cls.user,password= cls.password,db= cls.db)
        except Exception as e:
            logging.info("MongoConfigDetailInfo connection ERR:{}".format(e))
        return cls.db

    @classmethod
    def close(cls):
        cls.db.close()

    @classmethod
    def insert_table_info(cls,table,keys,values):
        '''
        :param table: sring table名称
        :param keys: tuple 元组内元素需为字符串
        :param values: 双重元组数据，且内层元组数据需长度一致
        :return:
        '''
        sql = '''REPLACE INTO {table} {keys} VALUES ()'''.format(table=table, keys=keys)
        sql = cls._set_sql(sql,len(keys))
        logging.debug("执行sql语句:{}".format(sql))
        s = cls.connectDB()
        try:
            s.cursor().executemany(sql,values)
            s.commit()
        except Exception as d:
            logging.info("there is exception in insertdata to mysql,exception:{}".format(str(d)))

    @classmethod
    def get_data_by_sql(cls,sql):

        logging.debug("get_data_by_sql-sql:{}".format(sql))
        s = cls.connectDB()
        s = s.cursor()
        try:
            s.execute(sql)
            k = s.fetchall()
            return k
        except Exception as f:
            logging.info("get_data_by_sql Exception:{},sql:{}".format(str(f),sql))
            pass
            # time.sleep(10)
            # cls.get_data_by_sql(sql)

    @classmethod
    def update_info_by_condition(cls,table,condition_key,value_key,conditon_key_and_value):
        try:
            cursor = cls.connectDB()
            sql = "update {} SET {}=(%s) where {}=(%s)".format(table,condition_key,value_key)
            logging.debug("update_info_by_condition-sql:{}".format(sql))
            logging.debug("updatestarttime:{}".format(datetime.datetime.now()))
            cursor.cursor().executemany(sql, conditon_key_and_value)  # commit_id_list上面已经说明
            cursor.commit()
            logging.debug("updateendtime:{}".format(datetime.datetime.now()))
        except:
            raise


    @classmethod
    def _set_sql(cls,sql,num):
        sql = sql.replace("'","`")
        sql1 = sql[:-1]
        for s in range(num):
            sql1 += "%s,"
        sql = sql1[:-1] + ")"
        return sql

    @classmethod
    def getalldata(cls, sql):
        s = cls.connectDB()
        s.execute(sql)
        cls.alldata = s.fetchall()
        return cls.alldata

