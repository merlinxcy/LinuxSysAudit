import linuxaudit_gui_for_linux
import lib
import threading
import sys
from lib import mongolib
from lib import rsyslog
from lib import proclib
from lib import filelib
SysModule=rsyslog.rsysloglib()
ProcModule=proclib.proclib()

def SysHandle():
	global SysModule
	
	#print a
	while True:
		#print a
		a=open("auditcontrol.conf","r")
		aa=a.readline().strip('\n')
		a.close()
		if aa=="Start":
			print "[+]Start SysModule......"
			SysModule.run()
			break

def ProcHandle():
	global ProcHandle
	
	while True:
		a=open("auditcontrol.conf","r")
		aa=a.readline().strip('\n')
		a.close()
		if aa=="Start":
			print "[+]Start ProcModule......"
			ProcHandle.run()
			break

def FileHandle():

	while True:
		a=open("auditcontrol.conf","r")
		aa=a.readline().strip('\n')
		a.close()
		if aa=="Start":
			print "[+]Start FileModule......"
			filelib.FSMoitor('/home/a')
			break


if __name__=='__main__':
	print "[+]Reading the configure......"
	print "[*]Waiting for......."
	Syst=threading.Thread(target=SysHandle)
	Proct=threading.Thread(target=ProcModule)
	Filet=threading.Thread(target=FileHandle)
	Syst.setDaemon(True)
	Proct.setDaemon(True)
	Filet.setDaemon(True)
	Syst.start()
	Proct.start()
	Filet.start()
	print "[+]Start GUI........"
	linuxaudit_gui_for_linux.run()
	Syst.join()
	Proct.join()
	Filet.join()
	#pass
else:
	print "[-]The main file cannot be imported"
	sys.exit(0)