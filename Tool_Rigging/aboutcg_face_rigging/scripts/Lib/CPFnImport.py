#!/usr/bin/python
#encoding:gbk
#作者：张隆鑫
#完成时间：2019.7.20
#最近修改时间：无
#曲线操作功能集
'''
变量：
无
函数：
importList 批量导入模块函数输入字符串列表
访问示例：
'''
import pymel.core as pm
import importlib
#批量导入模块函数输入字符串列表
def importList(All):
	if type(All)!=list:
		All=list(All)
	return [importlib.import_module(i) for i in All if type(i)==str]
def importRoot(root,All):
	if type(All)!=list:
		All=list(All)
	return [importlib.import_module(root+i) for i in All if type(i)==str]
