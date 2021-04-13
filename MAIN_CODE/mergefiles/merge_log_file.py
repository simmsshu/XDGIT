#merge log files
#python ./merge_log_file.py ./logfiles.txt totalFiles
# from gevent import monkey
# monkey.patch_all()
# from gevent.pool import Pool
import requests
import sys
import os
import shutil
import struct
import threading
count = 0
totalFiles = 0

def download(url):
    path1 = os.getcwd()
    global count
    global totalFiles
    chrome = 'Mozilla/5.0 (X11; Linux i86_64) AppleWebKit/537.36 ' + '(KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    headers = {'User-Agent': chrome}
    filename = url.split('/')[-1].strip()
    print("filename:{}".format(filename))
    r = requests.get(url.strip(), headers=headers, stream=True)

    if os.path.exists(path1+"/mergefile/data/"):
        pass
    else:
        os.makedirs(path1+"/mergefile/data/")
    with open(path1+"/mergefile/data/" + filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    count += 1
    print("{} is downloaded totalFiles = {}, count = {}".format(filename, totalFiles, count))
    #All files download is complete
    if totalFiles == count:
        merge_log_files()

def removeLine(key, filename):
    os.system('sed -i /%s/d %s' % (key, filename))

def del_file(filepath):
    """
    :param filepath: 
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def removeTempFolder():
    path1 = os.getcwd()
    if os.path.exists(path1+"/mergefile/"):
        if os.path.exists(path1+"/mergefile/data/"):
            del_file("D:/mergefile/data/")
        if os.path.exists(path1+"/mergefile/output/"):
            del_file(path1+"/mergefile/output/")
    else:
        os.makedirs(path1+"/mergefile/")
def merge_log_files():
    path1 = os.getcwd() + "/mergefile"
    dataPath = path1 + '/data/'
    dataFiles = os.listdir(dataPath)

    numPartDic = {}
    for datafile in dataFiles :
        print ("file name = %s" %(datafile))
        fo = open(dataPath+datafile, "rb")
        dd = datafile.split(".")
        num = int(dd[len(dd) - 1])
        numPartDic[num] = dataPath+datafile
        fo.close()

    #sort dictionary
    sortPartDic = sorted(numPartDic.items(),key = lambda x: x[0])
    if os.path.exists(path1 + "/output/"):
        pass
    else:
        print("there is no dir")
        os.makedirs(path1 + "/output/")
    newFile = open(path1+"/output/data.zip", "wb")
    for item in sortPartDic :
        fileSize = os.path.getsize(item[1])
        fi = open(item[1], "rb")
    
        while fileSize > 0 :
            data = fi.read(1)
            newFile.write(data)
            fileSize -= 1
        else :
            fo.close()

    else :
        newFile.close()

if __name__ == "__main__":
    try:
        threads = []
        print("当前目录:{}".format(os.getcwd()))
        inputdata = input("请输入待合并文件下载地址(以[a,b]的形式输入)：")
        ARGS = eval(inputdata)
        totalFiles = len(ARGS)
        removeTempFolder()
        # p = Pool(4)
        for line in ARGS:
            if line:
                threads.append(threading.Thread(target=download,args=(line,)))
        for s in threads:
            s.start()
            s.join()
        input("按任意键退出")
        # p.join()
    except Exception as e:
        print(e)