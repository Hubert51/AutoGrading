
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__,template_folder="/Users/Bill 1/Dropbox/Flask_templates")
loged_in =  False;
@app.route('/')
def hello_world():
	return '<h1>This is Auto Grading</h1>'
	
@app.route('/secretPage')
def after_login_page():
	if not loged_in:
		return 'You can access this Page after you have log in'
	else:
		return 'Thank you for your login'
	
@app.route('/user/<username>', methods=['POST', 'GET'])
def user(username):
	return 'Hello,%s' % username

@app.route('/user/login',methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'GET':
		return render_template('login.html')
	else:
		username = request.form['username']
		password = request.form['password']
		if username == 'zhangcheng' and password == 'li':
			loged_in = True
			return redirect('/secretPage')
		else:
			error = 'Invalid Credentials. Please try again.'
		return render_template('login.html', error=error)
		
@app.route('/user/redirect', methods=['POST'])
def redirect_to_new_url():
	username = request.form['username']
	return redirect(url_for('user',username=username))

if __name__ == '__main__':
	app.run(debug=True)
	pass