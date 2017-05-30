from lib import mongolib
class data:
	mono=mongolib.mongolib()
	def get_proc_audit(self):
		return self.mono.outputall('proc_audit')

	def get_syslog_audit(self):
		return self.mono.outputall('syslog')
		#pass
	def get_filelog_audit(self):
		return self.mono.outputall('file_audit')

