from pyinotify import WatchManager,Notifier,ProcessEvent,IN_DELETE,IN_CREATE,IN_MODIFY
import os
import mongolib
import time
class EventHandler(ProcessEvent):
	"""event handle"""
	mono=mongolib.mongolib()
	def process_IN_CREATE(self,event):
		mess=time.asctime()+" Create file: "+str(os.path.join(event.path,event.name))
		print mess
		dic={'Info':str(mess)}
		self.mono.input(dic,'file_audit')

	def process_IN_DELETE(self,event):
		mess=time.asctime()+" Delete file: "+str(os.path.join(event.path,event.name))
		print mess
		dic={'Info':str(mess)}
		self.mono.input(dic,'file_audit')

	def process_IN_MODIFY(self,event):
		mess=time.asctime()+" Modify file: "+str(os.path.join(event.path,event.name))
		print dic
		dic={'Info':str(mess)}
		self.mono.input(dic,'file_audit')


def FSMoitor(path):
	wm=WatchManager()
	mask=IN_DELETE | IN_CREATE | IN_MODIFY
	notifier=Notifier(wm,EventHandler())
	wm.add_watch(path,mask,auto_add=True,rec=True)
	print '[+]Now starting monitor %s' % (path)
	while True:
		try:
			notifier.process_events()
			if notifier.check_events():
				notifier.read_events()
		except Exception as e:
			notifier.stop()
			print e
			break

if __name__=='__main__':
	FSMoitor('/home/a')