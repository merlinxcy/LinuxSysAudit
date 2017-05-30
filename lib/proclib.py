import os
import sys
import re
import psutil
import subprocess
import time
from mongolib import *
class proclib:
	dic=''
	db=' '
	def __init__(self):
		self.db=mongolib()
	def __call__(self):
		self.run()
	'''
	def getProcessinfo(self,p):#bug!!!!!!!!!!!!!
		try:
			cpu=int(p.get_cpu_percent(interval=0))
			rss,vms=p.getmemory_infO()
			name=p.name
			pid=p.pid
		except psutil.error.NoSuchProcess,e:
			name='Closed_Process'
			pid=0
			rss=0
			vms=0
			cpu=0
		return [name.upper(),pid,rss,vms,cpu]

	def getAllProcessInfo(self):#bug!!!!!!!!!
		instances=[]
		all_processes=list(psutil.process_iter())
		for proc in all_processes:
			proc.get_cpu_percent(interval=0)
		time.sleep(1)
		for proc in all_processes:
			instances.appeed(getProcessinfo(proc))
		return instances
	'''
	def getProcInfoBypid(self,pid):
		try:
			pid=int(pid)
			p=psutil.Process(pid)
			p_name=p.name()
			p_path=p.exe()
			p_cwd=p.cwd()
			p_stat=p.status()
			p_starttime=p.create_time()
			p_cpu=p.cpu_times()
			p_mem=p.memory_percent()
			p_io=p.io_counters()
			p_conn=p.connections()
			p_thread=p.num_threads()
			p_user=p.username()
			info_list=[pid,p_name,p_path,p_cwd,p_stat,p_starttime,p_cpu,p_mem,p_io,p_conn,p_thread,p_user]
		except Exception as e:
			#print e
			#print '\n---------------------------------'
			pid=int(pid)
			p=psutil.Process(pid)
			p_name='Closed_Process'
			p_path='None'
			p_cwd='None'
			p_stat='None'
			p_starttime='None'
			p_cpu='None'
			p_mem='None'
			p_io='None'
			p_conn='None'
			p_thread='None'
			p_user=p.username()
			info_list=[pid,p_name,p_path,p_cwd,p_stat,p_starttime,p_cpu,p_mem,p_io,p_conn,p_thread,p_user]
		return info_list

	def getAllProcInfo(self):
		pid_list=psutil.pids()
		for i in pid_list:
			a=self.getProcInfoBypid(i)
			dic=self.tranListToDict(a)
			self.analysisProcInfo(dic)
			self.saveInfoInDB(dic)


	def tranListToDict(self,l):
		dic=dict()
		#print l
		dic={
		'pid':l[0],
		'p_name':l[1],
		'p_path':l[2],
		'p_cwd':l[3],
		'p_stat':l[4],
		'p_starttime':l[5],
		'p_cpu':l[6],
		'p_mem':l[7],
		'p_io':l[8],
		'p_conn':l[9],
		'p_thread':l[10],
		'p_user':l[11]
		}
		#print dict
		return dic
	def saveInfoInDB(self,dic):
		if self.db==' ':
			self.db=mongolib()
		#print dic['pid']
		#time.sleep(3)
		self.db.delete_same_update('proc',dic['pid'],dic)

	def saveAnalysisInDB(self,dic,collect):
		if self.db==' ':
			self.db=mongolib()
		self.db.input(dic,collect)

	#analysis
	def analysisProcInfo(self,dic):
		#analysis name:if passwd is existed,if 
		if str(dic['p_name'])=='passwd':
			newdic={
			'Time':str(time.asctime()),
			'Type':'Proc Event',
			'Level':'Warning',
			'Pid':str(dic['pid']),
			'Process Name':str(dic['p_name']),
			'Process User':str(dic['p_user']),
			'Info':'passwd process has been created.You password may be changed!'
			}
			self.saveAnalysisInDB(newdic,collect='proc_audit')
		if str(dic['p_name'])=='wget':
			newdic={
			'Time':str(time.asctime()),
			'Type':'Proc Event',
			'Level':'Info',
			'Pid':str(dic['pid']),
			'Process Name':str(dic['p_name']),
			'Process User':str(dic['p_user']),
			'Info':'wget process has been created.Evil script may be downloaded!'
			}
			self.saveAnalysisInDB(newdic,collect='proc_audit')

	def run(self):
		while True:
			self.getAllProcInfo()
			time.sleep(1)


if __name__=='__main__':
	a=proclib()
	#a.getAllProcessInfo()
	#ans=a.getProcInfoBypid(2085)
	#print ans
	#a.getAllProcInfo()
	a.run()
	print '==========================================================='




