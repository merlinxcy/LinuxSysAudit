import re

def find_in_list(target,str):
	ans=list()
	for i in target:
		if i.find(str)!=-1:
			#print "string has been find in target"
			ans.append(i)
	return ans

def find_in_str(target,str):
	pass

def tran_dic_to_list(dic):
	pass