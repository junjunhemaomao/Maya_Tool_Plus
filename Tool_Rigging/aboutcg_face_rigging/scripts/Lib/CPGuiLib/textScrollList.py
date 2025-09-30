#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间:2019.9.21
#最近修改时间:
#本模块提供了textScrollList快速创建
import pymel.core as pm
#提供了基本的textScrollList的创建
class init:
	def __init__(self,W=200,H=100,label=u'text'):
		buW = W/3
		with pm.columnLayout(w=W,h=400):
			self.text = pm.text(l=label,w=W,h=H*0.2)
			self.textScrollList = pm.textScrollList(w=W,h=H*0.6 , numberOfRows=10000, allowMultiSelection=True, showIndexedItem=4 )
			with pm.rowLayout( w=W, h=H*0.2 , numberOfColumns = 3 , adjustableColumn = 3 , columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)]):
				pm.button(label = u'载入接口' ,w=buW,h=H*0.2,c=self.add)
				pm.button(label = u'删除接口' ,w=buW,h=H*0.2,c=self.Delete)
				pm.button(label = u'清空接口' ,w=buW,h=H*0.2,c=self.empty)
	def add(self,*asd):
		pass
	def Delete(self,*asd):
		idList = pm.textScrollList(self.textScrollList,q=1,sii=1)
		[pm.textScrollList(self.textScrollList,e=1,rii=i) for i in idList[::-1]]
	def empty(self,*asd):
		pm.textScrollList(self.textScrollList,e=1,ra=1)
	def get(self,*asd):
		return pm.textScrollList(self.textScrollList,q=1,ai=1)
#提供了选择的textScrollList的创建
class sel(init):
	def add(self,*asd):
		pm.textScrollList(self.textScrollList,e=1,append=pm.selected(fl=1))
#提供了通道栏的textScrollList的创建
class channelBox(init):
	def add(self,*asd):
		try:
			select = pm.selected()[0]
		except:
			pm.error(u'至少选择一个物体')
		attr = pm.channelBox('mainChannelBox',q=True,sma=True)
		[pm.textScrollList(sel.textScrollList,e=1,append=str(select+'.'+i)) for i in attr]
