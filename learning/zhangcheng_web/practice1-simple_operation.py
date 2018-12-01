#!/usr/bin/python

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)
@app.route('/')
def index():
	return '<h1>you should enter something like this 127.0.1:5000/sum/float/a/b</h1>'
@app.route('/sum/float/<float:a>/<float:b>/')
def getFloatSum(a,b):
#	test url: http://127.0.0.1:5000/sum/float/12.1/15.1/
	c = a + b
	return '<h1>the sum of this two number is %f </h1>' %c

if __name__ == '__main__':
	app.run()
	pass