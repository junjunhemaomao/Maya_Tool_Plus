#!/usr/bin/python
#encoding:gbk
#本模块实现了自定义字符串操作函数集
#以下为函数功能说明
'''
Modify_the_program_name(Name,inStr,outName=r'')
在输入的字符串内搜索输入的名称替换为输出名称
搜索替换逻辑搜索前面没有.的单词替换为输出名称
返回字符串
'''
import re
def Modify_the_program_name(Name,inStr,outName=r''):
	return re.sub(r'(?<!\.)\b'+Name+r'\b',outName,inStr)
#print Modify_the_program_name(Name,inStr,r'namabi')