import datetime
import time
import sys
import os
import logging
logging.basicConfig(level=logging.INFO)
sys.path.append("./ConfigDataAnalys/")
from ConfigDataAnalys.getConfigData import *
from configparser import RawConfigParser

if __name__ == "__main__":
    config_info = RawConfigParser()
    config_info.read("config.ini")
    starttime = datetime.datetime.strptime("{}".format(config_info.get("time","starttime")),"%Y-%m-%dT%H:%M:%S")
    # while True:
    endtimenow = datetime.datetime.utcnow()
    logging.info("endtimenow:{}".format(endtimenow))
        # time.sleep(60)
        #10分钟执行一次
        # if datetime.datetime.now().minute%10 == 0:

    daynum = (endtimenow - starttime).days
    if daynum >= 1:
        for x in range(daynum):
            try:
                if x == 0:
                    starttime = starttime
                else:
                    # starttime = (starttime + datetime.timedelta(days=1))
                    pass
                endtime   = (starttime + datetime.timedelta(days = 1))
                logging.debug("insert data by day")
                main_enter(starttime.strftime("%Y-%m-%dT%H:%M:%S"),endtime.strftime("%Y-%m-%dT%H:%M:%S"),config_info)
                starttime = endtime
            except Exception as f:
                logging.info("there is an exception in main code:{}".format(f))
        try:
            config_info.set("time", "starttime", "{}".format(starttime.strftime(("%Y-%m-%dT%H:%M:%S"))))
            with open("config.ini", "w") as k:
                config_info.write(k)
                k.close()
        except Exception as l:
            logging.info("writting file failed........")
    else:
        try:
            main_enter(starttime.strftime("%Y-%m-%dT%H:%M:%S"), endtimenow.strftime("%Y-%m-%dT%H:%M:%S"),config_info)
            starttime = endtimenow
            config_info.set("time","starttime","{}".format(starttime.strftime(("%Y-%m-%dT%H:%M:%S"))))
            with open("config.ini","w") as k:
                config_info.write(k)
                k.close()
        except Exception as d:
            logging.info("waring exception:{}".format(d))



