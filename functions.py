import pymongo
import hashlib
import uuid
from pymongo import MongoClient
cluster = MongoClient("mongodb://localhost:27017")
db = cluster["auth"]
collection = db["auth"]


def checkUn(un):
	results = collection.find_one({"_id": un})
	if results:
		return True
	else:
		return False

def addSession(un):
	session_id = str(uuid.uuid1())
	session_id_encrypted = hashlib.sha256(session_id.encode())
	add_session = collection.update_one({"_id": un}, {"$set":{"session_id":session_id_encrypted.hexdigest()}})
	return session_id

def signup(un, pw):
	if checkUn(un)==True:
		return False
	elif checkUn(un)==False:	
		pw = hashlib.sha256(pw.encode())
		post = {"_id": un, "password": pw.hexdigest()}
		collection.insert_one(post)

def login(un, pw):
	results = collection.find_one({"_id": un})
	if results:
		pw = hashlib.sha256(pw.encode())
		if results["password"]==pw.hexdigest():
			return True
		else:
			return False
	else:
		return False

def getUser(session):
	session_id_encrypted = hashlib.sha256(session.encode())
	session_id_encrypted = session_id_encrypted.hexdigest()
	results = collection.find_one({"session_id": session_id_encrypted})
	user_data = {"username": results["_id"]}
	return user_data