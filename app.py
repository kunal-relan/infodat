from flask import Flask,render_template,Response,session,request,redirect,url_for
import os
import json
from pymongo import MongoClient,GEO2D,uri_parser
import datetime
from bson.son import SON
from datetime import date, timedelta
from bson.son import SON
from bson import json_util
from bson.objectid import ObjectId
from bson.json_util import dumps

connection = MongoClient('mongodb://127.0.0.1/infodat')

db = connection.infodat
app = Flask(__name__)

app.secret_key = 'Fuckedupworld'
class Encoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, ObjectId):
			return str(obj)
		else:
			return obj

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
       if hasattr(obj, 'isoformat'):
           return obj.isoformat()
       elif isinstance(obj, ObjectId):
			return str(obj)
       else:
           return json.JSONEncoder.default(self, obj)

#Just Some Ping Tests
@app.route('/ping')
def ping():

	return "Hello World"

@app.route('/login',methods=['POST'])
def login():
	data = request.json
	username = data['email']
	password = data['password']
	print username
	user_exists = db.users.find({"email":username,"password":password}).count()
	if user_exists > 0:
			
			user_role = db.users.find({"Email":username,"Password":password})
			result = json.dumps({"error":False,"message":"User Signed In"},default=json_util.default)
			resp = Response(response=result,
				status=200,
				mimetype="application/json")
			return(resp)

	else :
		result = json.dumps({"error":True,"message":"Email/Password Wrong"},default=json_util.default)
		resp = Response(response=result,
			status=200,
			mimetype="application/json")
		return(resp)

@app.route('/signup',methods=['POST'])
def signup():
	data = request.json
	name = data['name']
	phone = data['phone']
	email = data['email']
	password = data['password']
	if email and password:
		checkExists = db.users.count({'email':email})
		if checkExists > 0:
			result = json.dumps({"error":True,"message":"Email Already Exists"},default=json_util.default)
			resp = Response(response=result,
				status=200,
				mimetype="application/json")
			return(resp)
		else:		
			saveUser = db.users.insert({'name':name,'phone':phone,'email':email,'password':password})
			if saveUser:
				result = json.dumps({"error":False,"message":"User Created :) "},default=json_util.default)
				resp = Response(response=result,
					status=200,
					mimetype="application/json")
				return(resp)	
			else:
				result = json.dumps({"error":True,"message":"Error Creating User"},default=json_util.default)
				resp = Response(response=result,
					status=200,
					mimetype="application/json")
				return(resp)
	else:
		result = json.dumps({"error":True,"message":"Email/Password not provided"},default=json_util.default)
		resp = Response(response=result,
			status=200,
			mimetype="application/json")
		return(resp)		
@app.route('/logout',methods=['GET'])
def logout():
	Getsession = session.get('Role')
	session.pop(Getsession)
	return redirect(url_for('main'))



if __name__ == "__main__":
	app.run(debug=True,host= '0.0.0.0')
