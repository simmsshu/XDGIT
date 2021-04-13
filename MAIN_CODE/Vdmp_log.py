from elasticsearch import Elasticsearch
import re
from datetime import datetime,timedelta
import json
import time
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)

class VdmpLog():
    def __init__(self,CID="",body="body1",searchtime=30,fromsize=0,size=500):
        self.CID=CID
        self.body=body
        self.searchtime=searchtime
        self.fromsize=fromsize
        self.size=size
        self.getMScheduleIndex=[]
        self.scheduleDictDetail=[]
        self.T = ["时间"]
        self.DataFrom = ["日志来源"]
        self.scheduleid = ["ScheduleID"]
        self.operations = ["Operation"]
        self.status=["schedule开关"]
        self.scheduleDetail = ["Schedule详情"]
        self.satartTs=["开始时间"]
        self.startAction = ["开始动作"]
        self.endTs=["结束时间"]
        self.endAct=["结束动作"]
        self.repeat=["执行周期"]
        self.err=""
        self.alldata=[]

        self.getVdmpLog()


    def getVdmpLog(self):
        ES=Elasticsearch("http://elk.vesync.com:9200")
        Index=self.getIdex(self.searchtime)
        Body=self.getBody(self.body)
        try:
            searchResults=ES.search(body=Body,index=Index,ignore_unavailable=True)
            # print(searchResults)
            self.getTotalData(searchResults)
        except Exception as e:
            # self.err=e
            raise e


    def getTotalData(self, data):
        pat1=re.compile(r"(.*?) client")
        pat2 = re.compile(r"\{\"(\w*sch\w*)\"\:(\{.*?\})\}",re.I)
        pat3 = re.compile(r"\"operation\":\"(.*?)\"")
        pat4 = re.compile(r"Payload=(\{.*\})(,|>)")
        pat5 = re.compile(r"(\{|,)\"(\w*sch\w*)\"\:(\{.*?\})\}", re.I)

        for hit in data["hits"]["hits"]:
            logging.debug("hit:{}".format(hit))
            operation=pat3.search(hit["_source"]["M"]).group(1)
            self.T.append(self.changeTformat(hit["_source"]["T"]))
            self.scheduleid.append(self.getScheduleIndex(hit["_source"]["M"]))
            self.operations.append(operation)
            datasource=self.regexFindWetherNull(pat1.search(hit["_source"]["M"]),1)
            if datasource == "Send":
                self.DataFrom.append("服务器")
                flags=1
                scheduleDetaild=self.getScheduleDetaild(flags,pat2,hit["_source"]["M"])
                self.scheduleDetail.append(pat2.search(hit["_source"]["M"]).group(2))
                if operation == "add":
                    self.status.append(self.getJsonData(scheduleDetaild, "status", ))
                    self.satartTs.append(self.translatUnixToTime(scheduleDetaild["startTs"]))
                    self.startAction.append(self.getJsonData(scheduleDetaild, "startAct"))
                    self.endTs.append(self.translatUnixToTime(self.getJsonData(scheduleDetaild, "endTs")))
                    self.endAct.append(self.getJsonData(scheduleDetaild, "endAct"))
                    self.repeat.append(self.getRepeat(scheduleDetaild))
                    self.getScheduleInofIndex(scheduleDetaild)

                else:
                    self.status.append("")
                    self.satartTs.append("")
                    self.startAction.append("")
                    self.endTs.append("")
                    self.endAct.append("")
                    self.repeat.append("")
            elif datasource == "Received":
                self.DataFrom.append("设备")
                self.scheduleDetail.append(pat4.search(hit["_source"]["M"]).group(1))
                if operation == "start" or operation == "end":
                    flags=1
                    scheduleDetaild = self.getScheduleDetaild(flags, pat5, hit["_source"]["M"],number=3)
                    self.status.append(self.getJsonData(scheduleDetaild,"status",))
                    self.satartTs.append(self.translatUnixToTime(self.getJsonData(scheduleDetaild,"startTs")))
                    self.startAction.append(self.getJsonData(scheduleDetaild,"startAct"))
                    self.endTs.append(self.translatUnixToTime(self.getJsonData(scheduleDetaild, "endTs")))
                    self.endAct.append(self.getJsonData(scheduleDetaild,"endAct"))
                    self.repeat.append(self.getRepeat(scheduleDetaild))
                    self.getScheduleInofIndex(scheduleDetaild)
                else:
                    flags=2

                    self.status.append("")
                    self.satartTs.append("")
                    self.endAct.append("")
                    self.startAction.append("")
                    self.endTs.append("")
                    self.repeat.append("")

        for key in self.getMScheduleIndex:
            aa=[]
            aa.append(key)
            self.scheduleDictDetail.append(aa)
        for hits in data["hits"]["hits"]:
            flags = 1
            for i in range(len(self.scheduleDictDetail)):
                operation = pat3.search(hits["_source"]["M"]).group(1)
                datasource = self.regexFindWetherNull(pat1.search(hits["_source"]["M"]), 1)
                if datasource == "Send":
                    if operation == "add" :
                        scheduleDetaild = self.getScheduleDetaild(flags, pat2, hits["_source"]["M"])
                        self.scheduleDictDetail[i].append(str(self.getJsonData(scheduleDetaild,self.getMScheduleIndex[i])))
                        # print(scheduleDetaild[self.getMScheduleIndex[i]])
                        # print(self.getMScheduleIndex[i])
                    else:
                        self.scheduleDictDetail[i].append("")
                elif datasource == "Received":
                    if operation == "start" or operation == "end":
                        scheduleDetaild = self.getScheduleDetaild(flags, pat5, hits["_source"]["M"],number=3)
                        if len(scheduleDetaild.keys())!= 0:
                            self.scheduleDictDetail[i].append(
                                str(self.getJsonData(scheduleDetaild, self.getMScheduleIndex[i])))
                        else:
                            self.scheduleDictDetail[i].append("")

                    else:
                        self.scheduleDictDetail[i].append("")

    def getAllData(self):
        self.alldata.append(self.T)
        self.alldata.append(self.DataFrom)
        self.alldata.append(self.scheduleid)
        self.alldata.append(self.operations)
        self.alldata.append(self.status)
        self.alldata.append(self.scheduleDetail)
        self.alldata.append(self.satartTs)
        self.alldata.append(self.startAction)
        self.alldata.append(self.endTs)
        self.alldata.append(self.endAct)
        if len(self.scheduleDictDetail) != 0:
            for s in self.scheduleDictDetail:
                self.alldata.append(s)

        self.alldata.append(self.repeat)
        logging.debug("alldata:{}".format(self.alldata))
        return self.alldata
    def getScheduleInofIndex(self,data):
        for df in data.keys():
            if df not in self.getMScheduleIndex and df not in ['operation', 'status', 'startTs', 'endTs', 'repeat', 'startAct', 'endAct']:
                self.getMScheduleIndex.append(df)
            # else:
            #     self.getMScheduleIndex.append("Null")

    def getRepeat(self,data):
        try:
            repeat=data["repeat"]
            return self.loopToWeekly(repeat)
        except Exception as e:
            # repeat=data["attribute"]
            return ""

    def loopToWeekly(self,number):
        binary = str(bin(number))[2:-1]
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

    def getJsonData(self,data,index):
        try:
            return data[index]
        except Exception as e:
            return ""
    def translatUnixToTime(self,unix):
        if unix != "":
            hour=str(time.gmtime(unix).tm_hour)
            minute=str(time.gmtime(unix).tm_min)
            if len(hour)<2:
                hour = "0"+hour
            if len(minute)<2:
                minute= "0"+ minute
            a1 = hour + ":" + minute
            return a1
        else:
            return ""

    def getScheduleDetaild(self,flags,regex,data,number=2):
        if flags==1:
            if regex.search(data):
                try:
                    s=json.loads(regex.search(data).group(number))
                except:
                    data1=regex.search(data).group(number)+"}"
                    s=json.loads(data1)
                    traceback.print_exc()

                return s
            else:
                return {}

        elif flags ==2:
            s=json.loads(regex.search(data).group(1))
            return s



    def getScheduleIndex(self,data):
        pat_0=re.compile(r"\"(\w*sch\w*)\"",re.I)
        pat_1=re.compile(r"(\"schID\":\"\d{0,2}\")")
        if pat_0.search(data):
            if pat_0.search(data).group(1) == "schNtf":
                s=pat_1.search(data).group(1)
            else:
                s=pat_0.search(data).group(1)
        else:
            s=""
        return s

    def regexFindWetherNull(self,s,i):
        if s:
            return s.group(i)
        else:
            return ""

    def changeTformat(self,t):
        T=str(t).replace("T","  ")
        T1=T.replace(".","  ")
        return T1
    def getIdex(self,days):
        headindex="vdmp-online-"
        totalDays=[]
        totalIndex=[]
        today=datetime.utcnow()
        for i in range(0,days):
            totalDays.append((today-timedelta(i)).__format__('%Y-%m-%d'))
        for i in totalDays:
            totalIndex.append(headindex+i)
        return totalIndex
    def getBody(self,str):
        body = {}
        body["body1"] = {
            "size": 500,  # 返回查询条数
            "from": 0,  # 返回起始页
            "sort": {"T": {"order": "desc"}},
            "query": {
                "bool": {
                    "minimum_should_match": 3,
                    "must_not": {
                        "wildcard": {
                            "M": "*timer*"
                        }
                    },
                    "should": [
                        {
                            "match_phrase": {
                                "M": "send"
                            }
                        },
                        {
                            "match_phrase": {
                                "M": "received"
                            }
                        },
                        {
                            "match_phrase": {
                                "M": "operation"
                            }
                        },
                        {
                            "match_phrase": {
                                "M": "{}".format(self.CID)
                            }
                        }
                    ]
                }
            }
        }
        body["body1"]["size"] = self.size
        body["body1"]["from"] = self.fromsize

        return body[str]

# ss=VdmpLog(CID="0L_kgXuyzrH1nbwW21-Ctj92dQsn2iq3")