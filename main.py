from flask import Flask, flash, request, render_template, session, url_for, redirect
from functions import *

app = Flask(__name__)

@app.route('/sign-up')
def signUp():
	return render_template("signup.html")

@app.route('/log-in')
def logIn():
	return render_template("login.html")

@app.route('/')
def home():
	try:
		session_id_encrypted = hashlib.sha256(session["user"].encode())
		user = collection.find_one({"session_id": session_id_encrypted.hexdigest()})
		if user:
			return "Hi "+ user["_id"]
		else:
			return redirect(url_for("logIn"))
	except:
		return redirect(url_for("logIn"))

@app.route('/sup', methods=['GET', 'POST'])
def sup():
	if request.method == 'POST':
		un=request.form.get('un')
		pw=request.form.get('pw')
		if signup(un, pw)==False:
			flash("Username already in use")
			return redirect(url_for("signUp"))
		else:
			flash("You were signed up successfully")
			return redirect(url_for("logIn"))
	else:
		return redirect(url_for("signUp"))

@app.route('/lin', methods=['GET', 'POST'])
def lin():
	if request.method == 'POST':
		un=request.form.get('un')
		pw=request.form.get('pw')
		if login(un, pw)==True:
			flash("Logged in successfully")
			session["user"]=addSession(un)
			return redirect(url_for("home"))
		else:
			flash("Username or password incorrect")
			return redirect(url_for("log_in"))
	else:
		try:
			if session["user"]:
				session_id_encrypted = hashlib.sha256(session["user"].encode())
				if collection.find_one({"session_id": session_id_encrypted.hexdigest()}):
					return redirect(url_for("home"))
				else:
					return redirect(url_for("log_in"))
		except:
			return redirect(url_for("log_in"))

if __name__=="__main__":
	app.config['SECRET_KEY'] = '8092u3489u5hy234u9ohy5239487uy5heruiwgyhwioudhjfgnsd98fgiuhjsdfg-=3#$%3429034#$%0928#$%#$%@#$^@$%#^$%#&%$(*dfgklijskdfghouiphjnsujihngouidfghjupo4i5uyt409568435069jirtojykioertyj4058096345860-3485634%^#$%^#$%^#$%^#$%^$%#^+$%)_^+$%_^%^)&(%^$&*/*/*-/-+*3456/3-*45kjahsfdjoiukhnajskdhfiuasdfhasdfFASDFASDFASDF@#@@!!~~~///xcv*@%$#4532%@#$TERWQTERWIEWRTIETWROEWRTOsrfgp'   
	app.run()