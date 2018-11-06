from flask import redirect
from flask import abort
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)






@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/')
def index():
    return render_template("html_learning.html")








if __name__ == '__main__':
    app.run()