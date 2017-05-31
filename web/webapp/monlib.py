from pymongo import MongoClient
import time
class monlib:
	mongo=''
	db=''
	def __init__(self):
		self.mongo=MongoClient('mongodb://localhost:27017/')
		self.db=self.mongo['audit']
	def outputall(self,collection='audit'):
		try:
			collection=self.db[collection]
			cursor=collection.find(dict())
			return self.displayCursor(cursor)
		except Exception as e:
			print e
	def displayCursor(self,cursor):
		a=list()
		for doc in cursor:
			#print doc
			a.append(doc)
			#print '---------------------------------'
		return a