#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间:2019.7.29
#最近修改时间:
'''
属性：
方法：
函数：
listCompleteBreakDown() 列表完全分解函数（当前列表及列表下所有列表进行分解）：警告使用递归:超出限制输出[None]
listBreakDown() 列表分解函数（仅当前列表分解）
Deduplication() 列表去重复函数
SearchType() 列表类型查找
访问示例：
listCompleteBreakDown(列表,分解深度限制)
listBreakDown(列表)
Deduplication(列表)
SearchType(列表,类型)ps:类型为类型类型
'''
def SearchType(iList,Type):
	return [i for i in iList if type(i)==Type]
def listCompleteBreakDown(iList,limit):
	if limit<=0:
		return [None]
	print limit
	o = []
	if type(iList)!=type([]):
		o.append(iList)
	else:
		[o.append(i) if type(i)!=type([]) else o.extend(listCompleteBreakDown(i,limit-1)) for i in iList]	
	return o
def listBreakDown(iList):
	o = []
	[o.append(i) if type(i)!=type([]) else o.extend(i) for i in iList]
	return o
def Deduplication(iList):
	return list(set(iList))
