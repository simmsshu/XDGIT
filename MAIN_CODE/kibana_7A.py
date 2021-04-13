from elasticsearch import Elasticsearch
from datetime import datetime,timedelta
import re
import json
class Kibana_7Alog():
    def __init__(self,CID,days=30,searchflag="body1",fromsize=0,size=500):
        self.CID=CID
        self.urlAndPort="http://elk.vesync.com:9200"
        self.days=days
        self.searchflag=searchflag    #判断需要调用的body
        self.fromsize=fromsize
        self.size=size
        self.accountid=["accountid"]
        self.cid=["CID"]
        self.T=["时间"]
        self.deviceName=["设备名"]
        self.firmVersion=["固件版本"]
        self.RSSI=["RSSI"]
        self.initState=["重连原因"]
        self.H=["重连服务器"]
        self.mac=["设备mac"]
        self.wifiName=["wifi名"]
        self.onfflinetotaltime=[]
        self.totallogs=0
        self.count_network=0
        self.count_wifi=0
        self.count_poweron=0
        self.count_confignet=0
        self.count_upgrade=0
        self.logsFrom = ["日志来源"]
        self.actions = ["action"]
        self.scheduleid = ["ScheduleID"]
        self.schStartTime = ["开始时间"]
        self.startAction = ["startAction"]
        self.endTime = ["结束时间"]
        self.loop = ["执行周期"]
        self.err=""

        self.startCollectDatta()
    def getIdex(self,days):
        headindex="cloud-wifioutlet7a-"
        totalDays=[]
        totalIndex=[]
        today=datetime.utcnow()
        for i in range(0,days):
            totalDays.append((today-timedelta(i)).__format__('%Y-%m-%d'))
        for i in totalDays:
            totalIndex.append(headindex+i)
        return  totalIndex

    def getBodyInitstate(self,flags):
        body={}
        for i in range(20):
            body["body"+str(i)]=dict()
        body["body1"] = {
            "size": 500,  # 返回查询条数
            "from": 0,  # 返回起始页
            "sort": {"T": {"order": "desc"}},  # 排序
            # "_source": ["data", "T", "host.name"],  # 返回指定字段
            "query": {
                "bool": {
                    "minimum_should_match": 2,
                    "should": [
                        {
                            "match_phrase": {
                                "M": {
                                    "query": "device login info"
                                }
                            }},
                        {"match_phrase": {
                            "cid": {
                                "query": "{}".format(self.CID)
                            }
                        }}
                    ]
                }
            }

        }

        body["body2"]={
            "size": 500,  # 返回查询条数
            "from": 0,  # 返回起始页
            "sort": {"T": {"order": "desc"}},  # 排序
            # "_source": ["data", "T", "host.name"],  # 返回指定字段
              "query": {
                "bool": {
                  "minimum_should_match": 2,
                  "should": [
                    {
                      "match_phrase": {
                        "M": "close connect"
                      }
                    },
                    {
                      "match_phrase": {
                        "M": "Registration Successful"
                      }
                    },
                    {
                      "match_phrase": {
                        "M": {
                          "query": "device login info"
                        }
                      }
                    },
                      {"match_phrase": {
                          "cid": {
                              "query": "{}".format(self.CID)
                          }
                      }}
                  ]
                }
              }
            }
        body["body3"]={
            "size": 500,  # 返回查询条数
            "from": 0,  # 返回起始页
            "sort": {"T": {"order": "desc"}},  # 排序
            # "_source": ["data", "T", "host.name"],  # 返回指定字段
                  "query": {
                    "bool": {
                      "minimum_should_match": 2,
                      "must_not": {
                        "match_phrase": {
                          "iName": {
                            "query": "dispatchControllerMsg"
                          }
                        }
                      },
                      "should": [
                        {
                          "match_phrase": {
                            "message": {
                              "query": "\"uri\":\"/timer\""
                            }
                          }
                        },
                        {
                          "match_phrase": {
                            "M": {
                              "query": "got timer event report"
                            }
                          }
                        },
                        {"match_phrase": {
                            "cid": {
                                "query": "{}".format(self.CID)
                            }
                        }}
                      ]
                    }
                  }
                }
        for ss in body.keys():
            body[ss]["size"] = self.size
            body[ss]["from"] = self.fromsize

        return body[flags]
    def getNeddData(self,searchResults):
        Time=[]
        day=["日期"]
        minite=["分钟"]
        second=["秒"]
        self.totallogs=searchResults["hits"]["total"]
        for hit in searchResults["hits"]["hits"]:
            Time.append(hit["_source"]["T"])
            self.H.append(hit["_source"]["host"]["name"])
            self.accountid.append(hit["_source"]["accountId"])
            if self.getStrtoJsonData(hit["_source"],"data") != "":
                dataData=hit["_source"]["data"]
                jsondata=json.loads(dataData)
                self.deviceName.append(self.getStrtoJsonData(jsondata,"deviceName"))
                self.firmVersion.append(self.getStrtoJsonData(jsondata, "firmVersion"))
                self.RSSI.append(self.getStrtoJsonData(jsondata, "rssi").__str__())
                self.mac.append(self.getStrtoJsonData(jsondata, "mac"))
                self.initState.append(self.getStrtoJsonData(jsondata, "initState"))
                self.wifiName.append(self.getStrtoJsonData(jsondata, "wifiName"))

            else:
                self.deviceName.append("")
                self.firmVersion.append("")
                self.RSSI.append("")
                self.mac.append("")
                self.initState.append(self.getonofflinedata(hit["_source"]["M"],hit["_source"]["T"]))
                self.wifiName.append("")
        for i in Time:
            day.append(str(i).split("T",1)[0])
            second.append(str(i).split("T",1)[1])
        for s in range(1,len(second)):
            minite.append(second[s].split(".",1)[0])
        for j in range(1,len(day)):
            self.T.append(day[j]+"  "+second[j])
        self.getinitstateTotal(self.initState)
        self.offline_alltime(self.initState,day,minite)

    def getbody3Data(self,data):
        pat1=re.compile(r"\"id\":(.*?),")
        pat2=re.compile(r"\"relay\":\"(.*?)\"")
        pat3=re.compile("T(.*?):\d{2}\.")
        self.minute=["具体时间"]
        for hit in data["hits"]["hits"]:
            self.minute.append(pat3.search(hit["_source"]["T"]).group(1))
            self.T.append(self.changeTformat(hit["_source"]["T"]))
            self.accountid.append(self.getStrtoJsonData(hit["_source"],"accountId"))
            self.cid.append(self.getStrtoJsonData(hit["_source"],"cid"))
            if hit["_source"]["iName"] == "OnUserRequest":
                msg = json.loads(hit["_source"]["msg"])
                st, et = self.accourateStaAndEndTime(msg["start_time"], msg["duration"])
                self.logsFrom.append("云端发送")
                self.actions.append(msg["action"])
                self.scheduleid.append(str(msg["id"]))
                self.schStartTime.append(st)
                if msg["start_action"] == 1:
                    self.startAction.append("open")
                else:
                    self.startAction.append("break")
                self.endTime.append(et)
                self.loop.append(self.loopToWeekly(msg["loop"]))
            elif hit["_source"]["iName"] == "OnJSONMessage" and self.wetherBinA(hit["_source"]["M"],"report"):
                self.logsFrom.append("执行记录")
                self.actions.append("report")
                self.scheduleid.append(self.data_null(pat1.search(hit["_source"]["M"])))
                self.schStartTime.append("")
                self.startAction.append(self.data_null(pat2.search(hit["_source"]["M"])))
                self.endTime.append("")
                self.loop.append("")
            else:
                try:
                    msg = json.loads(hit["_source"]["msg"])
                    self.actions.append(str(msg["error"]))
                except KeyError:#解决7Aschedule查询msg KeyError导致程序闪退
                    self.actions.append("error")
                self.logsFrom.append("设备回复")
                self.scheduleid.append("")
                self.schStartTime.append("")
                self.startAction.append("")
                self.endTime.append("")
                self.loop.append("")
    def changeTformat(self,T):
        dateandtime=T.replace("T","  ")
        dateandtime=dateandtime.replace(".","  ")
        return dateandtime
    def loopToWeekly(self,number):
        binary = str(bin(number))[2:-1]
        # print(binary)
        weekly = ""
        dict = {"6": "1", "0": "7", "1": "6", "2": "5", "3": "4", "4": "3", "5": "2"}
        if number == 0:
            return "never"
        else:
            if len(binary) < 7:
                binary = "0" * (7 - len(binary)) + binary  # 将所有数据补全为7位二进制
            # binary1 = binary[1:]  # loop转换后周一标识符在最前面，移至末尾
            # binary2 = binary[0]
            # binary = binary1 + binary2
            for i in range(len(binary)):
                if binary[i] == "1":
                    weekly = weekly + dict[str(i)] + ","
            if weekly[-1] == ",":
                weekly = weekly[0:-1]

        return weekly

    def accourateStaAndEndTime(self,starttime,duration=0):
        start_hour=int(starttime)//60
        start_minute=int(starttime)%60
        startTime=self.whetherFirstisZero(start_hour)+":"+self.whetherFirstisZero(start_minute)
        end_hour=(int(starttime)+int(duration))//60
        if end_hour >= 24:
            end_hour = end_hour -24
        end_minute=(int(starttime)+int(duration))%60
        endTime=self.whetherFirstisZero(end_hour)+":"+self.whetherFirstisZero(end_minute)
        return startTime,endTime

    def whetherFirstisZero(self,a):
        if len(str(a))<2:
            b="0"+str(a)
            return b
        else:
            return str(a)

    def data_null(self, k):
        s = ''
        try:
            if k :
                s = k.group(1)
            else:
                s = ''
        except Exception as e:
            s=""
        return s

    def wetherBinA(self,a,b):
        if b in a:
            return True
        else:
            return  False
    def getStrtoJsonData(self,data,searchData):
        try:
            return data[searchData]
        except Exception as e:
            return ""

    def getonofflinedata(self,data,time):
        if data == "Registration Successful":
            return  "Connect"
        elif data == "close connect":
            return "die"
        else:
            return str(time)

    def offline_alltime(self, s, day, sec):
        onoffline_time = []
        about_time = []
        ss = []
        reconnect = []
        for i in range(1, len(day)):
            onoffline_time.append(datetime.strptime(day[i] + " " + sec[i], "%Y-%m-%d %H:%M:%S"))
            ss.append(s[i])
            reconnect.append(s[i])
        for i in range(len(onoffline_time)):
            about_time.append(str(onoffline_time[i]))

        for i in range(0, len(onoffline_time)):
            if reconnect[i] == "die" and i != 0 and reconnect[i - 1] != "die":
                about_time[i - 1] = str(onoffline_time[i - 1] - onoffline_time[i])
            else:
                about_time[i - 1] = ""
        self.onfflinetotaltime.append("掉线时长")
        for i in range(len(about_time)):
            self.onfflinetotaltime.append(about_time[i])

    def startCollectDatta(self):
        es=Elasticsearch(self.urlAndPort)
        es_index=self.getIdex(self.days)
        body=self.getBodyInitstate(self.searchflag)
        try:
            searchResults=es.search(body=body,index=es_index,ignore_unavailable=True)
            if self.searchflag == "body1" or self.searchflag =="body2":
                self.getNeddData(searchResults)
            elif self.searchflag == "body3":
                self.getbody3Data(searchResults)
                # for hit in searchResults["hits"]["hits"]:
                #     if hit["_source"]["iName"] == "OnUserRequest":
                #         print(json.loads(hit["_source"]["msg"])["start_action"])
        except Exception as e:
            pass


    def getaccountid(self):
        return self.accountid
    def getcid(self):
        return self.CID
    def getT(self):
        return self.T
    def getdeviceName(self):
        return self.deviceName
    def getfirmVersion(self):
        return self.firmVersion
    def getRSSI(self):
        return self.RSSI
    def getinitState(self):
        return self.initState
    def getH(self):
        return self.H
    def getmac(self):
        return self.mac
    def getwifiName(self):
        return self.wifiName
    def gettotallogs(self):
        return self.totallogs
    def getseonfflinetotaltime(self):
        return self.onfflinetotaltime
    def geterr(self):
        return self.err

    def getinitstateTotal(self,initstate):
        # print(initstate)
        for i in initstate:
            if i== "Network":
                self.count_network += 1
            elif i== "Wifi":
                self.count_wifi += 1
            elif i== "PowerOn":
                self.count_poweron += 1
            elif i== "ConfigNet":
                self.count_confignet += 1
            elif i== "upgrade":
                self.count_upgrade += 1
            else:
                pass
    def getcount_network(self):
        return self.count_network
    def getcount_wifi(self):
        return self.count_wifi
    def getcount_poweron(self):
        return self.count_poweron
    def getcount_confignet(self):
        return self.count_confignet
    def getcount_upgrade(self):
        return self.count_upgrade
    def getminute(self):
        return self.minute
    def geOwnCid(self):
        return  self.cid
    def getlogsFrom(self):
        return self.logsFrom
    def getactions(self):
        return self.actions
    def getscheduleid(self):
        return self.scheduleid
    def getschStartTime(self):
        return self.schStartTime
    def getstartAction(self):
        return self.startAction
    def getendTime(self):
        return self.endTime
    def getloop(self):
        return self.loop


