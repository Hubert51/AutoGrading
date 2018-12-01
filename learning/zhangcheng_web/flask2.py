from flask import Flask
from flask import request
app = Flask(__name__)
#@app.route('/billy')
#def index():
#	return '<h1>Hello World</h1>'
@app.route('/')
def index():
	user_agent = request.headers.get('User_Agent')
	return '<h1> Your browser is\n\n%s</h1>' %user_agent

if __name__ == '__main__':
	app.run()
	pass