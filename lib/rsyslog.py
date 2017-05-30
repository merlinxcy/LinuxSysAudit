import syslog
import os
from utils.utils import *
import re
from mongolib import *
import time
class rsysloglib:
	log_path=""
	log_type=""
	log=""
	mongo=''
	conf=''
	filepoint={'authlog':0,'kernlog':0,'userlog':0,'daemonlog':0}
	def __init__(self):
		self.mongo=mongolib()
	def logline_trans(self,line):
		try:
			#get day
			log_list=list()
			day=re.findall(r'(.*?) [0-9][0-9]:',line)[0]
			#get time
			log_list.append(day)
			time=re.findall(r'..:..:..',line)[0]
			log_list.append(time)
			user=re.findall(r'..:..:.. (.*?) ',line)[0]
			log_list.append(user)
			proc=re.findall(r'..:..:.. (.*?) (.*?): ',line)[0][1]
			log_list.append(proc)
			info=re.findall(r'..:..:.. (.*?) (.*?) (.*)',line)[0][2]
			log_list.append(info)
			return log_list#return a list
		except Exception as e:
			print e
			print 'gg'
	def read_logfile(self):
		try:
			userlog=open(self.log_path,"r")
			if self.log_type=='kern':
				if self.filepoint['kernlog']==0:
					self.log=userlog.readlines()
					self.filepoint['kernlog']=userlog.tell()
				else:
					userlog.seek(int(self.filepoint['kernlog']),0)
					self.log=userlog.readlines()
					self.filepoint['kernlog']=userlog.tell()
				#pass
			if self.log_type=='user':
				if self.filepoint['userlog']==0:
					self.log=userlog.readlines()
					self.filepoint['userlog']=userlog.tell()
				else:
					userlog.seek(int(self.filepoint['userlog']),0)
					self.log=userlog.readlines()
					self.filepoint['userlog']=userlog.tell()
				#pass
			if self.log_type=='mail.log':
				pass
			if self.log_type=='daemon':
				if self.filepoint['daemonlog']==0:
					self.log=userlog.readlines()
					self.filepoint['daemonlog']=userlog.tell()
				else:
					userlog.seek(int(self.filepoint['daemonlog']),0)
					self.log=userlog.readlines()
					self.filepoint['daemonlog']=userlog.tell()
				#pass
			if self.log_type=='authpriv':
				if self.filepoint['authlog']==0:
					self.log=userlog.readlines()
					self.filepoint['authlog']=userlog.tell()
				else:
					userlog.seek(int(self.filepoint['authlog']),0)
					self.log=userlog.readlines()
					self.filepoint['authlog']=userlog.tell()
				#pass
			if self.log_type=='syslog':
				pass
			if self.log_type=='messages':
				pass


			for i in self.log:
				#print i
				pass
			userlog.close()
		except Exception as e:
			print e

	def tran_dic(self,l):
		try:
			dic={
			'day':str(l[0]),
			'time':str(l[1]),
			'user':str(l[2]),
			'proc':str(l[3]),
			'info':str(l[4])
			}
		except Exception as e:
			print e
			dic=None
		return dic

	def find_log_info(self,target):
		if self.log:
			a=find_in_list(self.log,target)
			if a!=[]:#show log in console to debug
				for i in a:
					#print i
					l=self.logline_trans(i)
					dic=self.tran_dic(l)
					print dic
					if dic!=None:
						self.save_in_db(dic,'syslog')
						pass
			else:
				print "no	["+target+"]	log found"
				pass
	def set_log_type(self,type):
		if type==0:
			self.log_type="kern"
			self.log_path="/var/log/kern.log"
		elif type==1:
			self.log_type="user"
			self.log_path="/var/log/user.log"
		elif type==2:
			self.log_type="mail"
			self.log_path="/var/log/mail.log"
		elif type==3:
			self.log_type="daemon"
			self.log_path="/var/log/daemon.log"
		elif type==4:
			self.log_type="authpriv"
			self.log_path="/var/log/auth.log"
		elif type==5:
			self.log_type="syslog"
			self.log_path="/var/log/syslog"
		elif type==6:
			self.log_type=" lpr"
		elif type==7:
			self.log_type="news"
		elif type==8:
			self.log_type="uucp"
		elif type==9:
			self.log_type="cron"
		elif type==10:
			self.log_type="mark"
		elif type==11:
			self.log_type="message"#safe 
			self.log_path="/var/log/messages"
		else:
			self.log_type=""

	def set_conf(self):
		conf_path="/etc/rsyslog.conf"
		try:
			conf_file=open(conf_path,"a+")
			conf_file.writelines("local7.*		/var/log/boot.log")
		except Exception as e:
			print e

	def restart_service(self):
		os.system("service rsyslog restart")

	def save_in_db(self,dic,collect):
		self.mongo.input(dic,collection=collect)

	def config(self,parameter):
		self.conf=parameter

	def run(self):
		while True:
			print '===================================='
			self.set_log_type(4)
			self.read_logfile()
			self.find_log_info('fail')
			time.sleep(3)




if __name__=='__main__':
	a=rsysloglib()
	a.run()
	
	

