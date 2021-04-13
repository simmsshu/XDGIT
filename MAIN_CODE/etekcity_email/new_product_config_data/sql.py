#错误码描述统计
def get_errcode_desc(starttime,endtime):
    return f'''SELECT
                errcode '错误码',
                IF
                    ( ( errcode = "53.0" OR errcode = "54.0" ), IF ( wifi_ble_desc2 = "", wifi_ble_desc1, wifi_ble_desc2 ), description ) '描述',
                    count( * ) '数量',
                    count( DISTINCT UserID ) '用户数' 
                FROM
                    mongo_config_detail_info 
                WHERE
                    date >= "{starttime}"
                    AND date < "{endtime}"
                    AND Result = "Failure" 
                    AND ConfigModule REGEXP "WIFIBT[A-Z].*|^WFBO|^WFON" 
                GROUP BY
                    错误码,
                    描述'''

#52,53,54加密方式统计
def get_auth_count(starttime,endtime):
    return f''' SELECT
                errcode,
                description,
                AUTH,
                count( * ) count,
                COUNT( IF ( isManualInput = "TRUE", 1, NULL ) ) MANUINPUT,
                COUNT( IF ( isManualInput = "FALSE", 1, NULL ) ) NOTMANUINPUT 
            FROM
                mongo_config_detail_info 
            WHERE
                date >= "{starttime}"
                AND date < "{endtime}"
                AND Result = "Failure" 
                AND ConfigModule REGEXP "WIFIBT[A-Z].*|^WFBO|^WFON" 
                AND errcode REGEXP "5[2-4]" 
            GROUP BY
                errcode,
                description,
                AUTH '''

#配网失败路由器RSSI统计
def get_router_count(starttime,endtime):
    return  f'''SELECT
                errcode '错误码',
                IF
                ( ( errcode = "53.0" OR errcode = "54.0" ), IF ( wifi_ble_desc2 = "", wifi_ble_desc1, wifi_ble_desc2 ), description ) '描述',
                COUNT( IF ( ( routerRssi < "-99.0" AND routerRssi >= "-60.0" ), 1, NULL ) ) "60-100",
                COUNT( IF ( ( routerRssi < "-60.0" AND routerRssi >= "-40.0" ), 1, NULL ) ) "40-60",
                COUNT( IF ( ( routerRssi > "-40.0" AND routerRssi >= "-20.0" ), 1, NULL ) ) "20-40" 
            FROM
                mongo_config_detail_info 
            WHERE
                date >= "{starttime}"
                AND date < "{endtime}"
                AND Result = "Failure" 
                AND ConfigModule REGEXP "WIFIBT[A-Z].*|^WFBO|^WFON" 
                AND errcode REGEXP "5[2-4]" 
            GROUP BY
                错误码,
                描述'''

def get_wifibt_alldata(starttime,endtime):
    return f'''select * from mongo_config_detail_info where date >= '{starttime}' 
                AND date <'{endtime}' 
                AND Result = "Failure" 
                AND ConfigModule REGEXP "WIFIBT[A-Z].*|^WFBO|^WFON"'''

import pymysql
import logging
import datetime
import time
logging.basicConfig(level=logging.DEBUG)


class Mysql_config():

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
            raise
            logging.info("MongoConfigDetailInfo connection ERR:{}".format(e))
        finally:
            return cls.db

    @classmethod
    @property
    def close(cls):
        cls.db.cursor().close()
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
        d = cls.connectDB()
        s = d.cursor(pymysql.cursors.DictCursor)
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
