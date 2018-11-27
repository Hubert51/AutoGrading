from flask import request
from flask import Flask
from flask import make_response
from flask import redirect
from flask import abort
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap=Bootstrap(app)

class NameForm(Form):
    username = StringField('What is your username?', validators=[DataRequired()])
    password = StringField('Enter ur password', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    username = None
    password = None
    form = NameForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        form.username.data = ''
        form.password.data=''
    return render_template('index.html', form=form, username=username, password = password)



if __name__ == '__main__':
    app.run()