#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间:2019.11.2
#最近修改时间:
#本模块提供了进度条快速创建
import pymel.core as pm
#提供了基本的进度条的创建
class init(object):
	def __init__(self,Max=10):
		with pm.window(t="进度条",wh=(335,25)) as self.win:
			with pm.columnLayout():
				self.progressControl = pm.progressBar(w=300,h=25,st="进度",min=0,max=Max,width=333)
			pm.showWindow()
		pm.progressBar(self.progressControl,e=1,step=1)
	def init(self):
		pm.progressBar(self.progressControl,e=1,pr=0)
	def schedule(self,schedule=0):
		pm.progressBar(self.progressControl,e=1,pr=schedule)
	def addSchedule(self):
		pm.progressBar(self.progressControl,e=1,step=1)
	def delete(self):
		pm.deleteUI(self.win)
