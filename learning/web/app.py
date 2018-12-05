# import processData
import mysql.connector
from mysql.connector import errorcode

import os
import sys
# two file is created by developers
# from main import grading
# from helperFunction import readAndSaveAnswerFile
# from sample.web.helperFunction import saveImage, writeAnswer
import flask
from flask import Flask, render_template, request
from flask import url_for, redirect
# from flask_dropzone import Dropzone
import threading
import time
from multiprocessing import Process, Pool
# for user login
# from flask_wtf import FlaskForm
# from wtforms import StringField, BooleanField, PasswordField
# from wtforms.validators import DataRequired
import mysql.connector
# connect database
app = Flask(__name__)
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True )
