import requests
import re
from random import  choice
class FromIpgetLocation():
    def __init__(self,ip):
        self.ip=ip
    def getlocation(self):
        # pat1=re.compile("</li><li>参考数据1：(.*?)\s(.*?)</li><li>")
        # url="http://www.ip138.com/iplookup.asp"
        # payload={"ip":"{}".format(self.ip),"action":2}
        # header1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        # Chrome/80.0.3987.122 Safari/537.36"}
        # header2 = {"User-Agent":"Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)\
        #         Version/5.1Safari/534.50"}
        # header3 = {"User-Agent":"Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)\
        #         Version/5.1Safari/534.50"}
        # header4 = {"User-Agent":"Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)\
        #         Chrome/17.0.963.56Safari/535.11"}
        # header5 = {"User-Agent":"Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)"}
        # headers=[header1,header2,header3,header4,header5]
        # header=choice(headers)
        # resoponse=requests.get(url=url,params=payload,headers=header)
        # # resoponse.encoding="utf-8"
        # ss=resoponse.content
        # aa=str(ss.decode("gbk"))
        # try:
        #     # print(pat1.search(aa))
        #     locationC=pat1.search(aa).group(1)
        # except Exception as e:
        #     locationC=e
        #
        # return locationC

        return ""
# if __name__ == "__main__":
#     ss=FromIpgetLocation("99.203.145.199")
#     ss.getlocation()
class FromRouterGetVender():
    def __init__(self,routermac):
        self.routermac=routermac
    def getroutermacVender(self):
        pat1=re.compile(r"<td bgcolor=\"#FFFFFF\" style=\"font-size:16px;\">(.*?).</td>")
        str1="http://mac.51240.com/"
        str2="__mac/"
        url=str1+self.routermac+str2
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
        # html = etree.HTML(ss)
        # print(html)
        # print("xpath",html.xpath('//*[@id="main_content"]/table/tbody/tr/td/table/tbody/tr[2]/td[2]'))
        try:
            # print(pat1.search(ss))
            macVender=pat1.search(ss).group(1)
        except Exception as e:
            macVender=e

        return macVender
if  __name__=="__main__":
    dd=FromRouterGetVender("c0:89:ab:5d:7e:30")
    print(dd.getroutermacVender())