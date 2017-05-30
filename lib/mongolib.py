from pymongo import MongoClient
import time
class mongolib:
	mongo=''
	db=''
	def __init__(self):
		self.mongo=MongoClient('mongodb://localhost:27017/')
		self.db=self.mongo['audit']

	def input(self,data,collection='audit'):
		try:
			collection=self.db[collection]
			results=collection.insert(data)
		except Exception as e:
			print e

	def delete(self,query,collection='audit'):
		try:
			query=eval(query)
			collection=self.db[collection]
			results=collection.remove(query)
		except Exception as e:
			print e

	def clearall(self):
		try:
			collection=self.db['proc_audit']
			results=collection.remove()
			collection=self.db['file_audit']
			results=collection.remove()
			collection=self.db['proc_log']
			results=collection.remove()
			collection=self.db['syslog']
			results=collection.remove()
			print "clear]]]"
		except Exception as e:
			print e
	def output(self,query,collection='audit'):
		try:
			query=eval(query)
			collection=self.db[collection]
			cursor=collection.find(query)
			return self.displayCursor(cursor)
		except Exception as e:
			print e
			return None

	def outputall(self,collection='audit'):
		try:
			collection=self.db[collection]
			cursor=collection.find(dict())
			return self.displayCursor(cursor)
		except Exception as e:
			print e

	def delete_same_update(self,module='',para=None,dic=None):
		#try:
			if module=='proc':
				collection=self.db['proc_log']
				#find
				query={'pid':int(para)}
				cursor=collection.find(query)
				if cursor.count():
					#self.displayCursor(cursor)
					flag=True
				else:
					print 'no find'
					flag=False
					#pass
				#delete insert or only insert
				if flag==True:
					#time.sleep(10)
					collection.remove(query)
					collection.insert(dic)
				else:
					collection.insert(dic)
		#except Exception as e:
			#print e
	def displayCursor(self,cursor):
		a=list()
		for doc in cursor:
			print doc
			a.append(doc)
			print '---------------------------------'
		return a


if __name__=='__main__':
	a=mongolib()
	#dic={'3':'3'}
	#a.delete_same_update('proc',3,dic)
	#a.output('dict()','proc_audit')
	tmp=a.outputall('syslog')
	print len(tmp)
	for i in tmp[0]:
		print i