import requests
from ts_mysql import MongoConfigDetailInfo
import re
import logging

def getroutermacVender_bynetreq(self,routermac):
    pat1=re.compile(r"<td bgcolor=\"#FFFFFF\" style=\"font-size:16px;\">(.*?).</td>")
    str1="http://mac.51240.com/"
    str2="__mac/"
    url=str1+routermac+str2
    header1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/80.0.3987.122 Safari/537.36"}
    header2 = {"User-Agent":"Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)\
            Version/5.1Safari/534.50"}
    header3 = {"User-Agent":"Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)\
            Version/5.1Safari/534.50"}
    header4 = {"User-Agent":"Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)\
            Chrome/17.0.963.56Safari/535.11"}
    header5 = {"User-Agent":"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)"}
    headers=[header1,header2,header3,header4,header5]
    header=choice(headers)
    resoponse=requests.get(url=url,headers=header)
    ss=resoponse.text
    try:
        macVender=pat1.search(ss).group(1)
    except Exception as e:
        macVender=e
    return macVender
def get_routermac_vender_netsql():
    url = "http://standards-oui.ieee.org/oui/oui.txt"
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
    response = requests.get(url=url,headers = header)
    return response.text


def inset_data_to_macvender():
    alldata = []
    table = "mac_vender"
    keys = ("mac","vender")
    d = get_routermac_vender_netsql()
    pat = re.compile("([0-9a-zA-Z]{2}-[0-9a-zA-Z]{2}-[0-9a-zA-Z]{2})\s+\(hex\)\s+(.*?)\s\n")
    rs = pat.findall(d)
    dd = 0
    for a in rs:
        print(a[0].replace("-",":"),a[1])
        alldata.append((a[0].replace("-",":"),a[1]))
        dd+=1
    alldata = tuple(alldata)
    logging.info("total:{}".format(dd))
    MongoConfigDetailInfo.insert_table_info(table, keys, alldata)
    MongoConfigDetailInfo.close()
