from UI.needBase import *
import csv
body = {
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "request.data": "upschedule"
          }
        },
        {
          "match": {
            "request.context.method": "bypassV2"
          }
        }
      ]
    }
  }
}
starttime = "2021-03-23T05:58:18"
endtime = "2021-03-30T05:58:18"
# alldata_ = []
# cid_list = []
# def getTimeBystamp(timestamp):
#     try:
#         return datetime.utcfromtimestamp(int(timestamp))
#     except:
#         return datetime.utcfromtimestamp(int(0))
#
# def getneeddata(data):
#     global alldata_
#     for x in data["hits"]["hits"]:
#         if DictAndStrTransfer.get_data_byindex(x["_source"],["request","data","cid"]) not in cid_list and \
#             int(DictAndStrTransfer.get_data_byindex(x["_source"],["request","data","payload","data","startTs"])) < 1615274373\
#             and int(DictAndStrTransfer.get_data_byindex(x["_source"],["request","data","payload","data","startTs"])) != 0:
#             alldata_.append({})
#             cid_list.append(DictAndStrTransfer.get_data_byindex(x["_source"],["request","data","cid"]))
#             alldata_[-1]["cid"] = DictAndStrTransfer.get_data_byindex(x["_source"],["request","data","cid"])
#             alldata_[-1]["time"] = DictAndStrTransfer.get_data_byindex(x["_source"],["@timestamp"])
#             alldata_[-1]["timezone"] = DictAndStrTransfer.get_data_byindex(x["_source"],["request","context","timeZone"])
#             alldata_[-1]["phoneos"] = DictAndStrTransfer.get_data_byindex(x["_source"],["request","context","phoneOS"])
#             alldata_[-1]["configmodule"] = DictAndStrTransfer.get_data_byindex(x["_source"],["request","data","configModule"])
#             alldata_[-1]["startTs"] = DictAndStrTransfer.get_data_byindex(x["_source"],["request","data","payload","data","startTs"])
#             alldata_[-1]["startUTCtime"] = getTimeBystamp(DictAndStrTransfer.get_data_byindex(x["_source"],["request","data","payload","data","startTs"]))
#             alldata_[-1]["traceid"] = DictAndStrTransfer.get_data_byindex(x["_source"],["request","context","traceId"])
#         else:
#             pass
#
# def getElasticsearchDataByTime(starttime):
#     return GetElasticsearchData(body=body,index= getsearchindex(index="cloud-appserver-new")).\
#         get_data_by_time(starttime=starttime,endtime= endtime)
#
# total = 1
# while total:
#     try:
#         data1 = getElasticsearchDataByTime(starttime)
#         total = data1["hits"]["total"]
#         starttime = data1["hits"]["hits"][-1]["_source"]["@timestamp"]
#         getneeddata(data1)
#     except Exception as f:
#         print(f)
#
#
#
# with open("./upschedule.csv","w",newline= "",encoding = "utf-8-sig") as k:
#     writer = csv.DictWriter(k,fieldnames= alldata_[0].keys())
#     writer.writeheader()
#     writer.writerows(alldata_)
#     k.close()
Elasticsearch_5601.body = body

Elasticsearch_5601.index = "cloud-appserver-new"
# Elasticsearch_5601.getdata()
# print(Elasticsearch_5601.endtime)
# Elasticsearch_5601.getdata()
# print(Elasticsearch_5601.endtime)
# Elasticsearch_5601.getdata()
# print(Elasticsearch_5601.endtime)
for x in Elasticsearch_5601.getdata()["hits"]["hits"]:
  print(x)
for y in Elasticsearch_5601.getdata()["hits"]["hits"]:
  print(y)
for z in Elasticsearch_5601.getdata()["hits"]["hits"]:
  print(z)
