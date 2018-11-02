from flask import request
from flask import Flask
from flask import make_response
from flask import redirect
from flask import abort
from flask import Flask, render_template

app=Flask(__name__)


@app.route('/')
def index():
    return render_template("html_learning.html")

@app.route('/user/<name>')
def user(name):
 return render_template('user.html', name=name)


@app.route('/users/<id>')
def get_user(id):

 if id!='jia':
  abort(404)
 return '<h1>Hello, %s</h1>' % id

if __name__=="__main__":
    app.run()