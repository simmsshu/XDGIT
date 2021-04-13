import datetime
import csv
from email_send import *
from sql import *
from configparser import RawConfigParser


#附件名称,默认无附件
annex           =   "wifiBT配网数据.csv"
#数据统计时间
now_time        =   datetime.datetime.now().date()
befor_7day      =   (datetime.datetime.now() - datetime.timedelta(days=7)).date()
#解析配置文件
config_info     =   RawConfigParser()
config_info.read("config.ini",encoding="utf-8")
# 发件人邮箱账号
my_sender       =   config_info.get("email","my_sender")
# 发件人邮箱密码
my_pass         =   config_info.get("email","my_pass")
# 收件人邮箱账号列表
to_receiver     =   eval(config_info.get("email","to_receiver"))
#抄送人员列表
cc_receiver     =   eval(config_info.get("email","cc_receiver"))
#邮件主题
subject         =   config_info.get("email","subject")
#数据库配置
Mysql_config().set_cofnig(config_info)
#获取数据
data0 = Mysql_config().get_data_by_sql(get_errcode_desc(befor_7day,now_time))
data1 = Mysql_config().get_data_by_sql(get_auth_count(befor_7day,now_time))
data2 = Mysql_config().get_data_by_sql(get_router_count(befor_7day,now_time))
data3 = Mysql_config().get_data_by_sql(get_wifibt_alldata(befor_7day,now_time))
#断开数据库连接
Mysql_config().close
#添加数据到表格
html0 = text_table_content(data0)
html1 = text_table_content(data1)
html2 = text_table_content(data2)
#邮件正文内容
context = f'''  <font size="5"><b>Hi All:</b></font><br>
                <font size="5"><b>本周wifi蓝牙配网统计如下</b></font><br><br>
                    <b>错误码描述统计</b>{html0}
                    <b>52,53,54加密方式统计</b>{html1}
                    <b>配网失败路由器RSSI统计</b>{html2}'''
#有附件
if annex:
    with open("wifiBT配网数据.csv", "w",newline= "", encoding = "utf-8-sig") as f:
        writer = csv.DictWriter(f,data3[0].keys())
        writer.writeheader()
        writer.writerows(data3)
        f.close()
    mail(context,my_sender,my_pass,to_receiver,cc_receiver,subject, annex = "wifiBT配网数据.csv")
#无附件
else:
    mail(context,my_sender,my_pass,to_receiver,cc_receiver,subject)
