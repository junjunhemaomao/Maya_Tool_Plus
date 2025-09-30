#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间:2019.9.7
#最近修改时间:
#本模块提供了节点链表的实现
import pymel.core as pm
#本类实现了加减节点的列表初始化输入为链表节点数、链表维度。可选参数链表名称
class addLinkedList():
	#初始化
	def __init__(self,size,Dimension,**Inname):
		sel = pm.selected()
		name = 'plusMinusAverage'
		Dimension = str(Dimension)
		if 'n' in Inname:
			name=Inname['n']
		if 'name' in Inname:
			name=Inname['name']
		out = [pm.createNode('plusMinusAverage',n=name+str(i+1)) for i in range(size)]
		for i in range(len(out)-1):
			outAttr = pm.general.PyNode(out[i]+'.o'+Dimension)
			inAttr = pm.general.PyNode(out[i+1]+'.i'+Dimension)
			outAttr>>inAttr[0]
		self.Dimension = Dimension#维度
		self.name = name#链表名称
		self.size = size#DG节点数
		self.DG = out#DG节点列表
		self.ID = [0]+[1 for i in range(1,size)]#ID列表
		self.currentDG = self.DG[0]#当前DG节点
		self.current=0#当前节点号
		pm.select(sel,r=1)
	#设置链表属性数值
	def set(self,value,attr):
		for i in self.DG:
			Attr = pm.general.PyNode(i+'.'+attr)
			Attr.set(value)
		return 0
	#获得链表属性数值
	def get(self,attr):
		out = []
		for i in self.DG:
			Attr = pm.general.PyNode(i+'.'+attr)
			out.append(Attr.get())
		return out
	#连接链表节点
	def con(self,outattr,inattr):
		outattr=pm.general.PyNode(outattr)
		for i in self.DG:
			Attr = pm.general.PyNode(i+'.'+inattr)
			outattr>>Attr
		return 0
	#删除链表
	def delete(self):
		pm.delete(self.DG)
		self.DG = []
		self.ID = []
		self.size = 0
	#添加链表数
	def add(self):
		sel = pm.selected()
		self.DG.append(pm.createNode('plusMinusAverage',n=self.name+str(self.size)))
		outAttr = pm.general.PyNode(self.DG[-2]+'.o'+self.Dimension)
		inAttr = pm.general.PyNode(self.DG[-1]+'.i'+self.Dimension)
		outAttr>>inAttr[0]
		self.size=self.size+1
		pm.select(sel,r=1)
		return 0
	#获得链表每属性列表
	def getattr(self,attr):
		return [pm.general.PyNode(i+'.'+attr) for i in self.DG]
	#迭代器
	def it(self):
		if self.current<self.size-1:
			self.current = self.current+1
			self.currentDG = self.DG[self.current]
		else:
			return 1
		return 0
	#当前DG节点
	def getItDG(self):
		if self.currentDG==None:
			pm.error('迭代未开始')
		return self.currentDG
	#输入连接
	def inCon(self,inAttr):
		inAttr=pm.general.PyNode(inAttr)
		Attr = pm.general.PyNode(self.currentDG+'.i'+str(self.Dimension))
		inAttr>>Attr[self.ID[self.current]]
		self.ID[self.current]=self.ID[self.current]+1
		return 0
	#输出连接
	def outCon(self,inAttr):
		inAttr=pm.general.PyNode(inAttr)
		Attr = pm.general.PyNode(self.currentDG+'.o'+str(self.Dimension))
		Attr>>inAttr
		return 0
	#初始化
	def initIt(self):
		self.current = 0
		self.currentDG = self.DG[self.current]
		return 0
	#反转
	def Reverse(self):
		self.DG = self.DG[::-1]
		self.ID = self.ID[::-1]
		return 0
#本类实现了乘除节点的列表初始化输入为链表节点数。可选参数链表名称
class multiplyDivideLinkedList():
	#初始化
	def __init__(self,size,**Inname):
		sel = pm.selected()
		name = 'multiplyDivide'
		if 'n' in Inname:
			name=Inname['n']
		if 'name' in Inname:
			name=Inname['name']
		out = [pm.createNode('multiplyDivide',n=name+str(i+1)) for i in range(size)]
		for i in range(len(out)-1):
			outAttr = pm.general.PyNode(out[i]+'.o')
			inAttr = pm.general.PyNode(out[i+1]+'.i1')
			outAttr>>inAttr
		self.name = name#链表名称
		self.size = size#DG节点数
		self.DG = out#DG节点列表
		self.DgIf = [0 for i in range(0,size)]#连接判断列表 
		self.currentDG = self.DG[0]#当前DG节点
		self.current=0#当前节点号
		pm.select(sel,r=1)
	#设置链表属性数值
	def set(self,value,attr):
		for i in self.DG:
			Attr = pm.general.PyNode(i+'.'+attr)
			Attr.set(value)
		return 0
	#获得链表属性数值
	def get(self,attr):
		out = []
		for i in self.DG:
			Attr = pm.general.PyNode(i+'.'+attr)
			out.append(Attr.get())
		return out
	#连接链表节点
	def con(self,outattr,inattr):
		outattr=pm.general.PyNode(outattr)
		for i in self.DG:
			Attr = pm.general.PyNode(i+'.'+inattr)
			outattr>>Attr
		return 0
	#删除链表
	def delete(self):
		pm.delete(self.DG)
		self.DG = []
		self.DgIf = []
		self.size = 0
	#添加链表数
	def add(self):
		sel = pm.selected()
		self.DG.append(pm.createNode('multiplyDivide',n=self.name+str(self.size)))
		outAttr = pm.general.PyNode(self.DG[-2]+'.o')
		inAttr = pm.general.PyNode(self.DG[-1]+'.i1')
		outAttr>>inAttr
		self.size=self.size+1
		pm.select(sel,r=1)
		return 0
	#获得链表每属性列表
	def getattr(self,attr):
		return [pm.general.PyNode(i+'.'+attr) for i in self.DG]
	#迭代器
	def it(self):
		if self.current<self.size-1:
			self.current = self.current+1
			self.currentDG = self.DG[self.current]
		else:
			return 1
		return 0
	#当前DG节点
	def getItDG(self):
		if self.currentDG==None:
			pm.error('迭代未开始')
		return self.currentDG
	#输入连接
	def inCon(self,inAttr):
		inAttr=pm.general.PyNode(inAttr)
		Attr = pm.general.PyNode(self.currentDG+'.i2')
		if self.DgIf[self.current]!=0:
			pm.warning('警告节点已被连接自动跳过')
			return 1
		inAttr>>Attr
		self.DgIf[self.current]=1
		return 0
	#输出连接
	def outCon(self,inAttr):
		inAttr=pm.general.PyNode(inAttr)
		Attr = pm.general.PyNode(self.currentDG+'.o')
		Attr>>inAttr
		return 0
	#初始化
	def initIt(self):
		self.current = 0
		self.currentDG = self.DG[self.current]
		return 0
	#反转
	def Reverse(self):
		self.DG = self.DG[::-1]
		self.DgIf = self.DgIf[::-1]
		return 0
