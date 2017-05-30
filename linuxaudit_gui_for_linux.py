from Tkinter import *
from tkMessageBox import *
import hashlib
import sys
import threading	#in order to refresh the gui
import time
import data
from lib import mongolib
#!-*- coding: utf-8 -*-

###########################
###########################
###########################
md5=hashlib.md5()
md5.update("11")
pwd=md5.hexdigest()
mainflag=0
data_com=data.data()
mono=mongolib.mongolib()
threadcontrol="None"
auditcontrol="None"
###########################
###########################
###########################

def change_auditconf(flag):
	a=open("auditcontrol.conf","w")
	a.write(str(flag))
	a.close()


def show():
    global mainflag
    global root
    global md5
    global pwd
    #print pwd
    global username_input
    global password_input
    u=str(username_input.get())
    p=str(password_input.get())
    md5=hashlib.md5()
    md5.update(p)
    pp=md5.hexdigest()
    #print u
    #print p
    #print pp
    if pwd==pp:
        print "[+]Login in"
        #root.close()#?
        #root.quit()#quit the loop next time will show again
        root.destroy()#close the login windows and start up the
        #root.withdraw()
        mainflag=1
    else:
        print "[-]Login out"


def scrollcall(moveto,pos):#smart
    log1.yview(moveto,pos)
    log2.yview(moveto,pos)
    log3.yview(moveto,pos)
    log4.yview(moveto,pos)
    log5.yview(moveto,pos)

def event_refresh():
	global root
	global procframe
	global fileframe
	global proc_info
	global file_info
	global threadcontrol

	global logframe#thread
	global log1,log2,log3,log4,log5#thread

	while True:
		proc_info.delete(0.0,END)
		file_info.delete(0.0,END)
		log1.delete(0,END)
		log2.delete(0,END)
		log3.delete(0,END)
		log4.delete(0,END)
		log5.delete(0,END)
		pinfo=data_com.get_proc_audit()
		sinfo=data_com.get_syslog_audit()
		finfo=data_com.get_filelog_audit()
		#print pinfo
		for i in range(0,len(pinfo)-1):
			proc_info.insert(INSERT,"======="+str(i)+"=======\n")
			a=str(pinfo[i]).replace('u','')
			a=a.replace('{','')
			a=a.replace('}','')
			a=a.replace(',','\n')
			proc_info.insert(INSERT,str(a))
			proc_info.insert(INSERT,"\n")
		#print sinfo
		for i in sinfo:
			log1.insert(END,i['day'])
			log2.insert(END,i['time'])
			log3.insert(END,i['user'])
			log4.insert(END,i['proc'])
			log5.insert(END,i['info'])
		for i in range(0,len(finfo)-1):
			file_info.insert(INSERT,"======="+str(i)+"=======\n")
			a=str(finfo[i]).replace('u','')
			file_info.insert(INSERT,str(a))
			file_info.insert(INSERT,str(a))
		if threadcontrol=="Exit":
			print "[-]event_refresh thread close"
			return
		else:
			time.sleep(1)
def startthread():
	#event
	global root
	global procframe
	global fileframe
	global proc_info
	global file_info
	global threadcontrol

	global logframe#thread
	global log1,log2,log3,log4,log5#thread
	t=threading.Thread(target=event_refresh)
	t.start()
	#event

def run():
	global mainflag
	global threadcontrol
	global username_input
	global password_input
	global root
	global procframe#thread
	global proc_info #thread
	global fileframe#thread
	global file_info#thread
	global logframe#thread
	global log1,log2,log3,log4,log5#thread
	global mono
	global auditcontrol
	######################################login###############################
	root=Tk()
	root.resizable(False,False)
	#height,width
	root.geometry('500x300+500+200')
	root.title('Linux Log Audit')
	title_label=Label(root,pady=25,text='Linux Log Audit Login',font=('',17,''))
	title_label.grid()
	frame=LabelFrame(root)
	frame.grid(padx=500/5-10,pady=300/5-52,sticky=N+W+E+S)
	username_label=Label(frame,text="Username",font=('Helvetica',12,'bold'))
	password_label=Label(frame,text="Password",font=('Helvetica',12,'bold'))
	username_input=Entry(frame,font=('',12,'bold'),borderwidth=3,highlightcolor='black',relief='sunken',width=15)
	password_input=Entry(frame,show='*',font=('',12,'bold'),borderwidth=3,highlightcolor='black',relief='sunken',width=15)
	confirm_button=Button(frame,text="Confirm",font=('Helvetica',15,'bold'),command=show)
	exit_button=Button(frame,text="   Exit   ",font=('Helvetica',15,'bold'),command=lambda threadcontrol="Exit":sys.exit(0))
	#grid
	username_label.grid(padx=10,pady=10,row=0,column=0,sticky=W)
	username_input.grid(padx=10,pady=10,row=0,column=1,sticky=W)
	password_label.grid(padx=10,pady=10,row=1,column=0,sticky=W)
	password_input.grid(padx=10,pady=10,row=1,column=1,sticky=W)
	confirm_button.grid(padx=20,pady=20,row=3,column=0,ipadx=5,ipady=5)
	exit_button.grid(padx=5,pady=20,row=3,column=1,ipadx=5,ipady=5)
	#tupian
	#root.iconbitmap('')
	root.mainloop()
	#print mainflag



	######################################main###############################
	main=Tk()
	main.resizable(False,False)
	main.geometry('960x560+300+200')
	main.title('linux log audit')
	##frame define
	titleframe=Frame(main)
	buttonframe=Frame(main)
	confframe=LabelFrame(main,text='Audit Configure')
	logframe=Frame(main)
	procframe=LabelFrame(main,text='Proc Monitor')
	fileframe=LabelFrame(main,text='File Monitor')
	sysframe=LabelFrame(main)
	##frame place
	titleframe.place(anchor=NW,x=0,y=0)
	buttonframe.place(anchor=NW,x=0,y=40)
	confframe.place(anchor=NW,x=10,y=110)
	logframe.place(anchor=NW,x=10,y=300)
	procframe.place(anchor=NW,x=350,y=0)
	fileframe.place(anchor=NW,x=650,y=0)
	sysframe.place(anchor=NW,x=350,y=250)


	#titleframe
	title=Label(titleframe,text='  Linux     Log     Audit',font=('',15,''))
	#buttonframe
	button1=Button(buttonframe,text='Start audit',command=lambda auditcontrol="Start": change_auditconf(auditcontrol))
	button2=Button(buttonframe,text='Stop audit',command=lambda auditcontrol="Stop":change_auditconf(auditcontrol))
	button3=Button(buttonframe,text='Kernel Mode',command=lambda:showinfo('Building','This module is not support'))
	button4=Button(buttonframe,text='Web Manage',command=lambda:showinfo('NO','no'))
	button5=Button(buttonframe,text=' Anaylsis ',command=startthread)
	button6=Button(buttonframe,text='     Exit     ',command=lambda threadcontrol="Exit":sys.exit(0))
	title.grid(row=0,column=0)
	button1.grid(row=1,column=0,sticky=W,padx=10)
	button2.grid(row=1,column=1,sticky=W,padx=10)
	button3.grid(row=1,column=2,sticky=W,padx=10)
	button4.grid(row=2,column=0,sticky=W,padx=10)
	button5.grid(row=2,column=1,sticky=W,padx=10)
	button6.grid(row=2,column=2,sticky=W,padx=10)
	#confframe
	file_label=Label(confframe,text='File Conf')
	proc_label=Label(confframe,text='Proc Audit')
	sys_label=Label(confframe,text='Sys Conf')
	time_label=Label(confframe,text='Time Filter')
	key_label=Label(confframe,text='Key Filter')
	file_input=Entry(confframe,width=10)
	proc_input=Entry(confframe,width=10)
	sys_input=Entry(confframe,width=10)
	time_conf=Entry(confframe,width=10)
	key_input=Entry(confframe,width=10)
	change_button=Button(confframe,text='Change',command=lambda:1)
	nochange_button=Button(confframe,text='No Change',command=lambda:1)
	file_label.grid(row=0,column=0,sticky=W,padx=25)
	file_input.grid(row=0,column=1,sticky=W)
	proc_label.grid(row=1,column=0,sticky=W,padx=25)
	proc_input.grid(row=1,column=1,sticky=W)
	sys_label.grid(row=2,column=0,sticky=W,padx=25)
	sys_input.grid(row=2,column=1,sticky=W)
	time_label.grid(row=3,column=0,sticky=W,padx=25)
	time_conf.grid(row=3,column=1,sticky=W)
	key_label.grid(row=4,column=0,sticky=W,padx=25)
	key_input.grid(row=4,column=1,sticky=W)
	change_button.grid(row=5,column=0,pady=10)
	nochange_button.grid(row=5,column=1,pady=10)
	##logframe
	label1=Label(logframe,text='Day')
	label2=Label(logframe,text='Time')
	label3=Label(logframe,text='User')
	label4=Label(logframe,text='Proc')
	label5=Label(logframe,text='Info')
	bar=Scrollbar(logframe,command=scrollcall)
	log1=Listbox(logframe,yscrollcommand=bar.set,width=6)
	log2=Listbox(logframe,yscrollcommand=bar.set,width=10)
	log3=Listbox(logframe,yscrollcommand=bar.set,width=8)
	log4=Listbox(logframe,yscrollcommand=bar.set,width=20)
	log5=Listbox(logframe,yscrollcommand=bar.set,width=70)
	label1.grid(row=0,column=0)
	label2.grid(row=0,column=1)
	label3.grid(row=0,column=2)
	label4.grid(row=0,column=3)
	label5.grid(row=0,column=4)
	log1.grid(row=1,column=0)
	log2.grid(row=1,column=1)
	log3.grid(row=1,column=2)
	log4.grid(row=1,column=3)
	log5.grid(row=1,column=4)
	bar.grid(row=1,column=5,ipady=67,sticky=W)
	'''
	for i in range(0,100):#insert data
	    log1.insert(END,i)
	    log2.insert(END,i)
	    log3.insert(END,i)
	    log4.insert(END,i)
	    log5.insert(END,i)
	'''
	##proc frame
	proc_info=Text(procframe,width=40,height=12)
	proc_info.insert(INSERT,"123\n")
	proc_info.insert(INSERT,"123")
	proc_info.grid()
	##file frame
	file_info=Text(fileframe,width=40,height=12)
	file_info.grid()
	##sysframe
	cleardb=Button(sysframe,text='Clear DB',command=mono.clearall)
	cleardb.grid()
	
	if mainflag==1:
	    main.mainloop()

if __name__=='__main__':
	run()