#
# pluralsight flask job board project
# this app.py live in the /jobs dir 
#but can do flask run from root dir of project
#

from flask import Flask, render_template

# create a Flask instance
app = Flask(__name__)


#add route decorators
@app.route('/')
@app.route('/joobs')
def jobs():
    return render_template('index.html')
