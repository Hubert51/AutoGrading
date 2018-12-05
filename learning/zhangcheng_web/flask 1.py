import flask
from flask import Flask, url_for
app = Flask(__name__)

#the '/*****' tell flask which part trigers the module
# if we define the route with a slash in the end, even we enter the URL with without Slash, it direct the user to the page we defined with slash
@app.route('/zhangcheng')
def noSlash():
	return '<h1>no slash</h1>.'
	
	
@app.route('/zhangcheng/')
def index():
	return '<h1>with slash</h1>.'
	
	
# for this one, if we enter the URL with slash in the end and we did not define the one with slash, it shows 404. For example, if I enter '0.0.0.0:5000/hello/' it shows 404
@app.route('/hello')
def hello():
	return "<h1>say hello</h1>."
	
	
#the context in the angle bracket is the argument, we can pass that to the function
@app.route('/user/<username>')
def show_user_profile(username):
	return 'User %s' % username
	

# 'int:' convert the input in the URL into INTEGER type
@app.route('/user/<int:post_id>')
def show_post(post_id):
	return 'Post ID is %d' %post_id
	

with app.test_request_context():
	pass
if __name__ == '__main__':
#	debug=True
#	debug  = True is the debug mode, when we change the code, the page automatically reload
	app.run(host = '0.0')
	