import pymongo
from isodate import isodatetime
from needClass import from_list_get_need_key_and_value
import logging
logging.basicConfig(level=logging.DEBUG)
class  Mongodb_connect(object):
    def __init__(self,UserID="",CID="",flags=0,skipnum=0,quireflag=0,limitnum=100,querydata={}):#flags判断查询大类，args参数判断统计的数据类型
        self.list=["ALL"]  #存放数据统计返回信息
        self.errCode=["errCode"]
        self.WifiCount=["WifiCount"]
        self.SSID=["SSID"]
        self.ConfigModule=["ConfigModule"]
        self.transform_Text=["密码格式位数"]
        self.ishandle = ["ishandle"]
        self.userid = ["UserID"]
        self.AppVersion = ["AppVersion"]
        self.devicerssi = ["设备路由器信号"]
        self.phonessi   = ["手机网络信号"]
        self.phoneDeviceRssi = ["手机设备信号"]
        self.routerMac=["routermac"]
        self.Result = ["Result"]
        self.OSVersion = ["OSVersion"]
        self.cid = ["CID"]
        self.ConnectMode = ["ConnectMode"]
        self.ip = ["ip"]
        self.AccountEmail = ["AccountEmail"]
        self.StartConfigDate = ["StartConfigDate"]
        self.IsVpn = ["IsVpn"]
        self.FirmVersion = ["FirmVersion"]
        self.desc = ["desc"]
        self.PassWord = ["PassWord"]
        self.detail = ["detail"]
        self.iplocation = ["IP位置"]
        self.aggregatedata=[]
        self.__UserID=UserID
        self.__CID=CID
        self.__flag=flags
        self.__quiredata=querydata
        # self.__args=args
        self.__username = "conn"
        self.__pwd="vd128A%"
        self.__host="54.173.16.151"
        self.__port="27017"
        self.__dbname="admin"
        self.__database="connectCenter"
        # self.__collection="setup_log"
        # self.__collectionbefor="app_upload_log"
        self.__skip=skipnum
        self.__limitnum=limitnum
        self.__uri="mongodb://{}:{}@{}:{}/{}?authMechanism=SCRAM-SHA-1".format(self.__username,self.__pwd,self.__host,self.__port,self.__dbname)
        # self.__data=self.connect_mongodb()  #获取需要的文档信息

    def connect_mongodb(self,*args,collection="setup_log"):
        logging.debug("self.__flag:{}".format(self.__flag))
        self.__client=pymongo.MongoClient(self.__uri)
        self.responsedata = self.__client[self.__database][collection]
        if self.__flag == "all":
            self.__quiredata = args[0]
        else:
            self.quireabout(*args)

    def getallfeedbackdata(self):
        return self.responsedata.find(self.__quiredata).limit(self.__limitnum).skip(self.__skip).sort("createTime", -1)

    def quireabout(self,*args):
        logging.info("into mongo query......")
        # 使用UserID或者CID查询配网日志
        if self.__flag == 0:
            ss = self.get_main_data()
            logging.info("had get mongodata......")
            self.getNeedData(ss)
        # 组合查询查询信息
        if self.__flag == 1:

            data = self.responsedata.find(self.__quiredata).limit(self.__limitnum).skip(self.__skip).sort("createTime", -1)
            self.getNeedData(data)

        #数据统计
        elif self.__flag ==2:
            logging.debug("数据统计参数：{}".format(args))
            if isinstance(args[0],str):
                data = self.responsedata.aggregate([{"$group": {"_id": "$%s"%args[0]}}])
                for x in data:
                    # if x["_id"]:
                    self.list.append(str(x["_id"]))
                    # else:
                    #     self.list.append(str(x["_id"]))
            elif isinstance(args[0],list):
                data=self.responsedata.aggregate(args[0])
                for x in data:
                    self.aggregatedata.append(x)



    # def dealaggregatedata(self,data):
    #
    #     for x in data:
    #         a=x["_id"]
    #         del x["_id"]
    #         a["count"]=x["count"]
    #
    #         print(a)
    #         # print(dict(x["_id"]+(del x["id"])))

    def getNeedData(self,data):
        logging.debug("into getNeeddata:{}".format(data))
        for x in data:
            logging.debug("data:{}".format(x))
            self.ConfigModule.append(self.findDict(x,"ConfigModule"))
            self.userid.append(self.findDict(x,"UserID"))
            self.AppVersion.append(self.findDict(x,"AppVersion"))
            self.Result.append(self.findDict(x,"Result"))
            self.OSVersion.append(self.findDict(x,"OSVersion"))
            self.ConnectMode.append(self.findDict(x,"ConnectMode"))
            self.ip.append(self.findDict(x,"ip"))
            self.AccountEmail.append(self.findDict(x,"AccountEmail"))
            self.StartConfigDate.append(self.findDict(x,"StartConfigDate"))
            self.IsVpn.append(str(self.findDict(x,"IsVpn")))
            # self.FirmVersion.append(self.findDict(x,"FirmVersion"))
            self.detail.append(x)
            if self.findDict(x, "CID") != "":
                self.cid.append(self.findDict(x, "CID"))
            else:
                try:
                    self.cid.append(x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"][0]["Result"]["deviceCid"] )
                except:
                    self.cid.append("")
            # 2020/10/10注释直接获得Firmware，Firmware修改为如下
            if self.findDict(x,"FirmVersion") != "":
                self.FirmVersion.append(self.findDict(x, "FirmVersion"))
            else:
                try:
                    if from_list_get_need_key_and_value(x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"],["Result","firmVersion"]) != None:
                        self.FirmVersion.append(from_list_get_need_key_and_value(x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"],["Result","firmVersion"]))
                    else:
                        self.FirmVersion.append("")
                except:
                    self.FirmVersion.append("")
            try:
                self.errCode.append(x["DetailInfo"]["Step4_DeviceReturnData"]["CurrentConfig"]["Result"]["err"])
            except:
                try:
                    self.errCode.append(str(x["DetailInfo"]["Step4_DeviceReturnData"]["CurrentConfig"]["err"]))
                except:
                    self.errCode.append("")
            # 2020/10/10修改self.WifiCount.append(x["DetailInfo"]["Step4_DeviceReturnData"]["WiFiListInfoArr"][0]["WiFiCount"])
            # 为如下（增加强制转换str）
            try:
                self.WifiCount.append(str(x["DetailInfo"]["Step4_DeviceReturnData"]["WiFiListInfoArr"][0]["WiFiCount"]))
            except:
                self.WifiCount.append("")
            try:
                self.SSID.append(x["DetailInfo"]["Step3_ConfigInfo"]["wifiSSID"] or x["DetailInfo"]["Step3_ConfigInfo"]["wifiID"])
            except KeyError:
                self.SSID.append("")

            try:
                self.PassWord.append(x["DetailInfo"]["Step3_ConfigInfo"]["wifiText"])
            except:
                self.PassWord.append("")

            try:
                text=x["DetailInfo"]["Step3_ConfigInfo"]["transfromText"]
                self.transform_Text.append(str(len(text))+text)
            except:
                self.transform_Text.append("")

            try:
                self.ishandle.append(x["DetailInfo"]["Step3_ConfigInfo"]["isManualInput"])
            except:
                self.ishandle.append("")

            try:
                self.desc.append(x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"][-1]["Result"]["description"])
            except:
                self.desc.append("")
            try:
                self.routerMac.append(x["DetailInfo"]["Step4_DeviceReturnData"]["CurrentConfig"]["Result"]["routerMac"])
            except:
                #2020/10/10添加oven routermac
                try:
                    k=0
                    for d in range(len(x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"])):
                        if "Result" in x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"][d].keys():
                            if "routerMac" in x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"][d]["Result"].keys():
                                if x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"][d]["Result"]["routerMac"] != "":
                                    self.routerMac.append(x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"][d]["Result"]["routerMac"])
                                    break
                                else:
                                    k+=1
                            else:
                                k += 1
                        else:
                            k += 1
                    if k == len(x["DetailInfo"]["Step4_DeviceReturnData"]["ConnectStepInfoArr"]):
                        self.routerMac.append("")
                except:
                    self.routerMac.append("")
            try:
                self.devicerssi.append(str(x["DetailInfo"]["Step4_DeviceReturnData"]["CurrentConfig"]["Result"]["deviceRSSI"]))
            except:
                self.devicerssi.append("")
            try:
                self.phonessi.append(str(x["DetailInfo"]["Step4_DeviceReturnData"]["CurrentConfig"]["PhoneRSSI"]))
            except:
                self.phonessi.append("")
            try:
                self.phoneDeviceRssi.append(x["DetailInfo"]["Step3_ConfigInfo"]["RSSI"])
            except:
                self.phoneDeviceRssi.append("")
        logging.info("alldata had getted......")

    def get_main_data(self):
        logging.info("into mongo getdata......")
        if self.__UserID != "":
            # requestdata="\"UserID\":\"{}\"".format(self.__UserID)
            # print(requestdata)
            data=self.responsedata.find({"UserID":"{}".format(self.__UserID)}).limit(self.__limitnum).skip(self.__skip).sort([("createTime",-1),("CreateAt",-1)])
            return data
        elif self.__CID != "":
            # requestdata = "\"CID\":\"{}\"".format(self.__CID)
            data = self.responsedata.find({"CID":"{}".format(self.__CID)}).limit(self.__limitnum).skip(self.__skip).sort([("createTime",-1),("CreateAt",-1)])
            return data
        else:
            data = self.responsedata.find({}).limit(self.__limitnum).skip(self.__skip).sort([("createTime",-1),("CreateAt",-1)])
            return data
    def get_aggregatedata(self):
        return self.aggregatedata
    def get_list(self):
        return self.list
    def get_errCode(self):
        return self.errCode
    def get_WifiCount(self):
        return self.WifiCount
    def get_SSID(self):
        return self.SSID
    def get_transform_Text(self):
        return self.transform_Text
    def get_AppVersion(self):
        return self.AppVersion
    def get_Result(self):
        return self.Result
    def get_OSVersion(self):
        return self.OSVersion
    def get_ConnectMode(self):
        return self.ConnectMode
    def get_ip(self):
        return self.ip
    def get_AccountEmail(self):
        return self.AccountEmail
    def get_StartConfigDate(self):
        return self.StartConfigDate
    def get_IsVpn(self):
        return self.IsVpn
    def get_FirmVersion(self):
        return self.FirmVersion
    def get_PassWord(self):
        return self.PassWord
    def get_desc(self):
        return self.desc
    def get_detail(self):
        return self.detail
    def get_iplocation(self):
        return self.iplocation
    def get_ishandle(self):
        return self.ishandle
    def get_userid(self):
        return self.userid
    def get_ConfigModule(self):
        return self.ConfigModule
    def get_cid(self):
        return self.cid
    def get_routerMac(self):
        return  self.routerMac
    def get_deviecrssi(self):
        return self.devicerssi
    def get_phonerssi(self):
        return self.phonessi
    def get_phoneDeviceRssi(self):
        return self.phoneDeviceRssi

    # def aggregations(self,flags):
    #     if flags == 1:


    def findDict(self,data,finddata):
        try:
            key=str(data[finddata])
            return key
        except:
            key=""
            return key

# if __name__=="__main__":
#     ss=Mongodb_connect(UserID="1264164")
#     # print(aa.find())