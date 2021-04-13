import requests
from random import choice
import os
import threading

class Deal_data():
	def __init__(self,header,cookie):
		self.header=header
		self.cookie=cookie
		self.creatfolder()
	def creatfolder(self):
		folder=os.path.exists("D:/Excel_data/")
		if folder:
			pass
		else:
			try:
				os.makedirs("D:/Excel_data/")
			except:
				folder = os.path.exists("D:\\Excel_data\\")
				if folder:
					pass
				else:
					os.makedirs("D:\\Excel_data\\")
	def get_url_data(self,url=None,params=None):
		try:
			resoponse=requests.get(url=url,headers=self.header,cookies=self.cookie,params=params)
			return resoponse.content
		except Exception as x:
			return x

	def write_excel_data(self,data,name="data"):
		try:
			file=open("D:/Excel_data/"+name+".xlsx","wb")
		except:
			file=open("D:\\Excel_data\\"+name+".xlsx","wb")
		file.write(data)
		file.close
	def read_excel_data(self):
		pass
	def deal_data(self):
		pass

