from flask import request
from flask import Flask
from flask import make_response
from flask import redirect
from flask import abort

app=Flask(__name__)


@app.route('/')
def index():
 return "hello"

@app.route('/user/<id>')
def get_user(id):

 if id!='jia':
  abort(404)
 return '<h1>Hello, %s</h1>' % id

if __name__=="__main__":
    app.run()