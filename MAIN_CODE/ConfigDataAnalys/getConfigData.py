from ts_mysql import MongoConfigDetailInfo
from routerMacVender import *
import logging
import datetime
import pymongo
import queue
import random
logging.basicConfig(level=logging.INFO)
SEARCH_DATE = None
# CONFIGINFO = None
class  Mongodb_connect(object):
    def __init__(self,config):
        self.data = []
        self.__username = config.get("mongo","username")
        # pwd = eval(config.get("mongo","pwd"))
        # self.__pwd=decrypt(*pwd)
        self.__pwd=config.get("mongo","pwd")
        self.__host=config.get("mongo","host")
        self.__port=config.get("mongo","port")
        self.__dbname=config.get("mongo","dbname")
        self.__database=config.get("mongo","database")
        self.__uri="mongodb://{}:{}@{}:{}/{}?authMechanism=SCRAM-SHA-1".format(self.__username,self.__pwd,self.__host,self.__port,self.__dbname)
        self.__connect_mongodb()

    def __connect_mongodb(self,collection="setup_log"):
        self.__client=pymongo.MongoClient(self.__uri)
        self.cursor = self.__client[self.__database][collection]

    def get_data(self,arg):
        return self.cursor.find(arg,no_cursor_timeout = True).limit(10000).sort("createTime", -1)

    def get_count(self,arg):
        return self.cursor.find(arg).count()

    def close(self):
        self.__client.close()


class GetInsertData():
    def __init__(self,alldata = None,table_flag = 0):
        self.data = None
        #判断写入的库
        self.flag = table_flag
        self.table = ["mongo_config_detail_info","mongo_cal_data","mac_vender"]
        self.alldata = alldata
        self.keys = []
        self.values = []
        # self.firstdata = True
        #下面存储要获取信息字段的函数和方法以及参数，如果除了data还有多个参数，需要用元组提交，同时创建方法时也要使用元组传递参数
        self.column = {"mongo_config_detail_info":{
                           "ObjId":{"method":get_id,"args":"_id"},
                           "UserID":{"method":get_data_by_key,"args":"UserID"},
                           "AccountEmail":{"method":get_data_by_key,"args":"AccountEmail"},
                           "ConfigModule":{"method":get_data_by_key,"args":"ConfigModule"},
                           "Result":{"method":get_data_by_key,"args":"Result"},
                           "ip":{"method":get_data_by_key,"args":"ip"},
                           "isManualInput":{"method":get_data_by_list,"args":["DetailInfo", "Step3_ConfigInfo", "isManualInput"]},
                           "AUTH":{"method":get_auth,"args":None},
                           "AppVersion":{"method":get_data_by_key,"args":"AppVersion"},
                           "createTime":{"method":get_data_by_key,"args":"createTime"},
                           "OSVersion":{"method":get_data_by_key,"args":"OSVersion"},
                           "MobileType":{"method":get_data_by_key,"args":"MobileType"},
                           "wifiSSID":{"method":get_data_by_list,"args":["DetailInfo", "Step3_ConfigInfo", "wifiSSID"]},
                           "transfromText":{"method":get_data_by_list,"args":["DetailInfo", "Step3_ConfigInfo", "transfromText"]},
                           "errcode":{"method":get_errcode,"args":None},
                           "description":{"method":get_description,"args":None},
                           "routermac":{"method":get_routermac,"args":None},
                           "free_heap":{"method":get_free_heap,"args":None},
                           "deviceMac":{"method":get_deviceMac,"args":None},
                           "routerRssi":{"method":get_routerRssi,"args":None},
                           "FirmVersion":{"method":get_firmwareVersion,"args":None},
                           "date":{"method":get_date,"args":None},
                           "step5_qeury_result":{"method":get_step5_qeury_result,"args":None},
                           "step5_network_status":{"method":get_step5_network_status,"args":None},
                           "step7_port_result":{"method":get_step7_port_result,"args":None},
                           "step4_wifi_code":{"method":get_data_by_list,"args":
                               ["DetailInfo", "Step4_DeviceReturnData", "ConnectStepInfoArr",-1,"Result","reason"]},
                           "step4_wifi_desc":{"method":get_data_by_list,"args":
                               ["DetailInfo", "Step4_DeviceReturnData", "ConnectStepInfoArr",-1,"Result","description"]},
                           "wifi_ble_code1":{"method":get_data_by_list,"args":
                               ["DetailInfo", "Step4_DeviceReturnData", "ConnectStepInfoArr",-2,"Result","type"]},
                           "wifi_ble_desc1":{"method":get_data_by_list,"args":
                               ["DetailInfo", "Step4_DeviceReturnData", "ConnectStepInfoArr",-2,"Result","msg"]},
                           "wifi_ble_code2": {"method": get_data_by_list, "args":
                               ["DetailInfo", "Step4_DeviceReturnData", "ConnectStepInfoArr", -1, "Result", "type"]},
                           "wifi_ble_desc2": {"method": get_data_by_list, "args":
                               ["DetailInfo", "Step4_DeviceReturnData", "ConnectStepInfoArr", -1, "Result", "msg"]},
                           },
                       "mongo_cal_data":{
                            "ObjId": {"method": get_id, "args": "_id"},
                            "UserID": {"method": get_data_by_key, "args": "UserID"},
                            "tcp_continue_time": {"method": get_tcp_time, "args": None},
                            "config_time": {"method": get_config_time, "args": None},
                            "connect_wifi_time": {"method": get_step4_cal_time, "args":
                                ["DEV_RECEIVE_APP_DATA", "DEV_CONNECTED_WIFI"]},
                            "get_ip_time": {"method": get_step4_cal_time, "args":
                                ["DEV_CONNECTED_WIFI", "DEV_GOT_IP"]},
                            "connect_server_time": {"method": get_step4_cal_time, "args":
                                ["DEV_GOT_IP", "DEV_CONNECTED_SERVER"]},
                            "device_config_time": {"method": get_step4_cal_time, "args":
                                ["DEV_RECEIVE_APP_DATA", "DEV_CONNECTED_SERVER"]}}}
        if self.flag != 2:
            self.set_keys()
            self.set_values()
        else:
            pass


    def get_table(self):
        return self.table[self.flag]

    def set_keys(self):
        self.keys.clear()
        for s in self.column[self.table[self.flag]].keys():
            self.keys.append(s)

    def get_keys(self,flag = 1):
        '''
        :param flag: flag =1,返回多重元组，如果为0 返回列表
        '''
        if flag:
            return tuple(self.keys)
        else:
            return self.keys

    def get_values(self,flag = 1):
        '''
        :param flag: flag =1,返回多重元组，如果为0 返回列表
        '''
        if flag:
            for s in self.data:
                self.values.append(tuple(s))
            return tuple(self.values)
        else:
            for s in self.data:
                self.values.append(s)
            logging.debug("len-values:{}".format(len(self.values)))
            return self.values

    def get_data(self):
        return self.data

    def set_values(self):
        self.data = []
        for s in self.alldata:
            self.data.append([])
            for a in self.keys:
                if self.column[self.table[self.flag]][a]["args"]:
                    d = self.column[self.table[self.flag]][a]["method"](s, self.column[self.table[self.flag]][a]["args"])
                else:
                    d = self.column[self.table[self.flag]][a]["method"](s)
                if d:
                    self.data[-1].append(d)
                else:
                    self.data[-1].append("")
        logging.debug("self.data-len:{}".format(len(self.data)))

def exception(func):
    def method(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as f:
            if args:
                if isinstance(args[0],dict):
                    if "_id" in args[0].keys():
                        logging.debug("there is an exception in {}:{},_id:{}".format(func.__name__,repr(f),args[0]["_id"]))
            else:
                logging.debug("there is an exception in {}:{}".format(func.__name__, repr(f)))
            return ""
    return method

def decrypt(encrypted, key_int):
    decrypted = encrypted ^ key_int
    length = (decrypted.bit_length() + 7) // 8
    decrypted_bytes = int.to_bytes(decrypted, length, 'big')
    return decrypted_bytes.decode()

def set_config(config):
    global CONFIGINFO
    CONFIGINFO = config

def get_auth(data):
    d = get_data_by_list(data,["DetailInfo", "Step3_ConfigInfo", "AUTH"])
    if d:
        if len(str(d)) >= 40:
            return str(d)[:10]
        else:
            return str(d)
    else:
        return ""

def mac_padd(mac_id_tmp):
    try:
        mac_id_arr = mac_id_tmp.split(":")
        mac_id_real_arr = []
        for one in mac_id_arr:
            if len(one) == 1:
                one = "0" + one
            else:
                pass
            mac_id_real_arr.append(one)
        return ":".join(mac_id_real_arr)
    except:
        return
@exception
def get_real_devicemac(string):
    return (str(hex(int(string[:2],16)-2))[2:] + string[2:])


def get_inset_data_to_macvender(keys,values,date):
    ObjId_index = keys.index("ObjId")
    routermacindex = keys.index("routermac")
    datalist = []
    alldata  = {}
    needdata = []
    if len(values) > 0:
        for s in values:
            if s[routermacindex] != "":
                mac = s[routermacindex]
                if mac[:8] not in datalist:
                    datalist.append(mac[:8])
                alldata[s[ObjId_index]] = mac[:8]
        if len(alldata.keys()) != 0:
            if len(datalist) == 1:
                sql1 = '''select mac,vender from mac_vender where mac in {}'''.format("(" +"'" + datalist[0] + "'" +")")
            else:
                sql1 = '''select mac,vender from mac_vender where mac in {}'''.format(tuple(datalist))
            # global CONFIGINFO
            MongoConfigDetailInfo.set_cofnig(CONFIGINFO)
            data1 = MongoConfigDetailInfo.get_data_by_sql(sql1)
            for ds in values:
               if ds[routermacindex] != "":
                   mac = ds[routermacindex].upper()[0:8]
                   for k in data1:
                       if mac == k[0]:
                           ds.append(k[1])

            keys.append("router_vender")
            for k in values:
                if len(k) < len(keys):
                    k.append("")
                needdata.append(tuple(k))

            return tuple(keys), tuple(needdata)
        else:
            return None, None
    else:
        return None,None

@exception
def get_step4_cal_time(data,list1):
    contime = ""
    getiptime = ""
    for s in data["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"]:
        if "Result" in s.keys():
            if contime == "":
                if list1[0] in s["Result"].values():
                    contime = s["DateTime"]
            elif getiptime == "":
                if list1[1] in s["Result"].values():
                    getiptime = s["DateTime"]
                    break
    if contime and getiptime:
        time1 = datetime.datetime.strptime("{}".format(contime), "%Y-%m-%d %H:%M:%S")
        time2 = datetime.datetime.strptime("{}".format(getiptime), "%Y-%m-%d %H:%M:%S")
        timesec = (time2 - time1).seconds
        return str(timesec)

@exception
def get_config_time(data):
    time1 = datetime.datetime.strptime("{}".format(data["DateTime"]),"%Y-%m-%d %H:%M:%S")
    time2 = datetime.datetime.strptime("{}".format(data["StartConfigDate"]),"%Y-%m-%d %H:%M:%S")
    timesec = (time1 - time2).seconds
    return str(timesec)

@exception
def get_step7_port_result(data):
    s = data["DetailInfo"]["Step7_ServerConnecting"]["Description"]
    if "Success" in s:
        return (str(data["DetailInfo"]["Step7_ServerConnecting"]["Port"])+" "+"Success")
    elif "Failure" in s:
        return (str(data["DetailInfo"]["Step7_ServerConnecting"]["Port"])+" "+"Failure")
    else:
        return ""

@exception
def get_step5_network_status(data):
    s = data["DetailInfo"]["Step5_RequestConnectStatus"][-1]["Result"]
    if "msg" in s:
        return "False"
    else:
        return "True"

@exception
def get_step5_qeury_result(data):
    s = data["DetailInfo"]["Step5_RequestConnectStatus"][-1]["Result"]
    if "Failure" in s:
        return "Failure"
    elif "Success" in s:
        return "Success"
    else:
        return ""



def get_date(data):
    global  SEARCH_DATE
    return SEARCH_DATE
#修复mongo异常objectid数据过长导致无法写入问题
@exception
def get_id(data,key):
    d = data[key]
    if len(str(d)) >= 50:
       return str(random.randint(100000000))
    else:
        return str(d)

@exception
def get_data_by_key(data,key):
    d = data[key]
    return str(d)

@exception
def get_tcp_time(data):
    step2       =   data["DetailInfo"]["Step2_ConnectDeviceByTCP"]
    starttime   =   0
    endtime     =   0
    number      =   0
    for s in range(len(step2)):
        if "Success" in step2[s]["Result"]:
            starttime   =   datetime.datetime.strptime(step2[s]["DateTime"],"%Y-%m-%d %H:%M:%S")
            number      =   s
            break
    for y in range(number,len(step2)):
        if "Failure" in step2[y]["Result"]:
            endtime     =   datetime.datetime.strptime(step2[y]["DateTime"],"%Y-%m-%d %H:%M:%S")
            break
        if y == len(step2)-1:
            endtime     =   datetime.datetime.strptime(step2[y]["DateTime"],"%Y-%m-%d %H:%M:%S")
    if isinstance(starttime,datetime.datetime) and isinstance(endtime,datetime.datetime):
        return str((endtime-starttime).seconds)
    else:
        return

@exception
def get_list_data_from_list(data, list1):
    for key in range(len(list1)):
        if isinstance(data, dict):
            if list1[key] in data.keys():
                data = data[list1[key]]
            else:
                return
        elif isinstance(data, list):
            for d in data:
                g = get_list_data_from_list(d, list1[key:])
                if g:
                    return g
        else:
            return
    if not isinstance(data,list) and not isinstance(data,dict):
        return str(data)

@exception
def get_data_by_list(data,list1):
    data1 = data
    for s in list1:
            data1 = data1[s]
    if len(str(data1)) > 200:
        return ""
    else:
        return str(data1)

def get_errcode(data):
    code = get_data_by_list(data,["DetailInfo","Step4_DeviceReturnData","CurrentConfig","Result","err"])
    if not code:
        code = get_data_by_list(data,["DetailInfo","Step4_DeviceReturnData","CurrentConfig","err"])
    if code:
        return str(code)

def get_description(data):
    des = get_data_by_list(data,["DetailInfo","Step4_DeviceReturnData","CurrentConfig","description"])
    if not des:
        des =get_data_by_list(data,["DetailInfo","Step4_DeviceReturnData","CurrentConfig","Result","description"])
    else:
        return des
    if not des:
        des =get_data_by_list(data,["DetailInfo","Step4_DeviceReturnData","ConnectStepInfoArr",-1,"Result","description"])
    else:
        return des
    if not des:
        des =get_data_by_list(data,["DetailInfo","Step4_DeviceReturnData","ConnectStepInfoArr",-1,"Result","msg"])
    else:
        return des

@exception
def get_routermac(data):
    routermac = get_data_by_list(data, ["DetailInfo", "Step4_DeviceReturnData", "CurrentConfig", "Result","routerMac"])
    if routermac:
        if routermac.startswith("ff:ff"):
            routermac = None
    if not routermac:
        routermac = get_list_data_from_list(data,["DetailInfo", "Step4_DeviceReturnData",
                                                  "ConnectStepInfoArr", "Result","routerMac"])
        if routermac:
            if routermac.startswith("ff:ff"):
                routermac = None
            else:
                return mac_padd(routermac)
    if not routermac and "Step5_RequestConnectStatus"  in data["DetailInfo"].keys():
        if len(data["DetailInfo"]["Step5_RequestConnectStatus"]) > 0:
            for s in data["DetailInfo"]["Step5_RequestConnectStatus"]:
                try:
                    if data["DetailInfo"]["Step3_ConfigInfo"]["wifiSSID"] in s["WifiName"]:
                        if "RouterMac" in s.keys():
                            if not s["RouterMac"].startswith("ff:ff"):
                                return mac_padd(s["RouterMac"])
                except:
                    pass
    return mac_padd(routermac)




def get_firmwareVersion(data):
    ver = get_data_by_key(data,"FirmwareVersion")
    if not ver:
        try:
            for x in data["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"]:
                if "Result" in x.keys():
                    if "firmVersion" in x["Result"].keys():
                        return x["Result"]["firmVersion"]
        except:
            pass

    return ver

def get_free_heap(data):
    free_head = get_list_data_from_list(data,["DetailInfo","Step4_DeviceReturnData","ConnectStepInfoArr","Result","free_heap"])
    return free_head

def get_deviceMac(data):
    device_mac     =  get_list_data_from_list(data,["DetailInfo","Step2_ConnectDeviceByTCP","RouterMac"])
    step3_wifiname =  get_data_by_list(data,["DetailInfo","Step3_ConfigInfo","wifiSSID"])
    step2_wifiname =  get_list_data_from_list(data,["DetailInfo","Step2_ConnectDeviceByTCP","WiFiName"])
    if device_mac:
        if step2_wifiname:
            if device_mac[-2:] == step2_wifiname[-2:]:
                return  mac_padd(get_real_devicemac(device_mac))
        if device_mac.startswith("ff:ff"):
            device_mac = None
    if not device_mac:
        device_mac = get_list_data_from_list(data,["DetailInfo","Step4_DeviceReturnData","CurrentConfig","RouterMac"])
    if not device_mac:
        device_mac = get_list_data_from_list(data,["DetailInfo","Step4_DeviceReturnData","ConnectStepInfoArr","Result","deviceMac"])
    return mac_padd(device_mac)

def get_routerRssi(data):
    routerRssi = get_list_data_from_list(data,["DetailInfo","Step4_DeviceReturnData","ConnectStepInfoArr","Result","routerRssi"])
    if routerRssi:
        return str(routerRssi)

def main_enter(starttime,endtime,config_info):
    set_config(config_info)
    ss=Mongodb_connect(config_info)
    global  SEARCH_DATE
    SEARCH_DATE = starttime.split("T")[0]
    logging.info("处理{}数据starttimeL{},endtime:{}".format(SEARCH_DATE,starttime,endtime))
    logging.info("获取 mongo_config_detail_info 主数据开始时间：{}".format(datetime.datetime.now()))

    #处理数据写入mongo_config_detail_info表
    ct= ss.get_data({"createTime":{'$gte':"{}".format(starttime),'$lt':"{}".format(endtime)}})
    logging.info("获取 mongo_config_detail_info 主数据完成时间：{}".format(datetime.datetime.now()))
    data = GetInsertData(ct)
    table = data.get_table()
    keys,values = get_inset_data_to_macvender(data.get_keys(flag=0),data.get_values(flag=0),SEARCH_DATE)
    logging.info("获取 mongo_config_detail_info 所有据完成时间：{}".format(datetime.datetime.now()))
    if values:
        logging.info("获取mongo_config_detail_info 插入数据完成，总计{}条,{}列".format(len(values),len(keys)))
        # global CONFIGINFO
        MongoConfigDetailInfo.set_cofnig(CONFIGINFO)
        MongoConfigDetailInfo.insert_table_info(table, keys, values)
        logging.info("插入mongo_config_detail_info 数据完成时间：{}".format(datetime.datetime.now()))
        ss.close()
    ss1 = Mongodb_connect(config_info)
    ct1 = ss1.get_data({"createTime":{'$gte': "{}".format(starttime), '$lt': "{}".format(endtime)}})
    logging.info("获取mongo_cal_data 数据开始时间：{}".format(datetime.datetime.now()))
    data1 = GetInsertData(ct1,table_flag = 1)
    table1 = data1.get_table()
    keys1 = data1.get_keys()
    values1 = data1.get_values()
    logging.info("获取mongo_cal_data 数据开始时间：{}".format(datetime.datetime.now()))
    if values1:
        logging.info("获取mongo_cal_data 数据总计{}条,{}列".format(len(values1), len(keys1)))
        MongoConfigDetailInfo.set_cofnig(CONFIGINFO)
        MongoConfigDetailInfo.insert_table_info(table1, keys1, values1)
        logging.info("插入mongo_cal_data数据完成时间：{}".format(datetime.datetime.now()))
        ss1.close()
    try:
        MongoConfigDetailInfo.close()
    except:
        pass

if __name__ == "__main__":
    date = ["2020-02-19","2020-05-29","2020-03-02"]
    for s in date:
        main_enter("{}T00:00:00".format(s), "{}T23:59:59".format(s))

    # list1 = []
    # starttime = datetime.datetime.strptime("2020-02-19T00:00:00", "%Y-%m-%dT%H:%M:%S")
    # now = datetime.datetime.utcnow()
    # MongoConfigDetailInfo.connectDB()
    # data = MongoConfigDetailInfo.get_data_by_sql("select DISTINCT date from mongo_config_detail_info ORDER BY date DESC")
    # for d in data:
    #     list1.append(d[0])
    # for s in range(360):
    #     needdata = starttime + datetime.timedelta(days = s)
    #     if needdata <= now:
    #
    #         if str(needdata.date()) not in list1:
    #             print(needdata.date())
    #         else:
    #             pass
    #     else:
    #         break
