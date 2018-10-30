from flask import Flask
app=Flask(__name__)
# using this file to learn basic knowledge about flask web

@app.route("/")
def index():
    return "Index Page"

@app.route("/hello")
def hello_world():
    return "<h1>hello world!</h1>"

@app.route("/user/<username>")
def show_username(username):
    return "User: %s" % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')  #if enter "/about/", u will get 404
def about():
    return 'The about page'
#


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
