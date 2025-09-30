#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间:2019.9.21
#最近修改时间:
#本模块提供了textField快速创建
import pymel.core as pm
#提供了基本的textField的创建
class init:
	def __init__(self,W=100,H=20,label=u'标签'):
		with pm.rowLayout( w=W, h=H , numberOfColumns = 3 , adjustableColumn = 3 , columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)]):
			pm.text(l=label,w=W*0.25,h=H)
			self.textField = pm.textField( w=W*0.5, h=H , tcc = self.tcc)
			pm.button(label = u'载入' ,w=W*0.25,h=H,c=self.Load)
	def tcc(self,*asd):
		pass
	def Load(self,*asd):
		pass
	def get(self,*asd):
		return pm.textField(self.textField,q=1,tx=1)
	def set(self,Name=''):
		pm.textField(self.textField,e=1,tx=Name)
#提供了选择的textField的创建
class sel(init):
	def Load(self,*asd):
		try:
			sel = pm.selected(fl=1)[0]
		except:
			pm.error(u'错误至少选择一个物体')
		pm.textField(self.textField,e=1,tx=sel)
#提供了通道栏的textField的创建
class channelBox(init):
	def Load(self,*asd):
		try:
			sel = pm.selected()[0]
		except:
			pm.error(u'至少选择一个物体')
		try:
			attr = pm.channelBox('mainChannelBox',q=True,sma=True)[0]
		except:
			pm.error(u'至少选择一个属性')
		pm.textField(self.textField,e=1,tx=str(sel+'.'+attr))
