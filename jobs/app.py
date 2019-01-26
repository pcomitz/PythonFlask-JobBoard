#
# pluralsight flask job board project
# this app.py live in the /jobs dir 
#but can do flask run from root dir of project
#
# see https://www.pluralsight.com/guides/git-for-projects-101
# git commit -am 'Completed the module'
# git push origin master
#
# module 3 adds sqlite
# to provide access throughout the application, import
# the global helper g from flask
# https://www.reddit.com/r/flask/comments/5ggh7j/what_is_flaskg/
#

import sqlite3
from flask import Flask, render_template, g

# Constant is path to already created
# db, jobs.sqlite
PATH= 'db/jobs.sqlite'

# create a Flask instance
app = Flask(__name__)

def open_connection():
    # http://effbot.org/zone/python-getattr.htm
    connection = getattr(g,'_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    # to make row indexing easier    
    connection.row_factory = sqlite3.Row
    return connection

# function to make it easier to query database
def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results=connection.commit()
    else:
        # ternary if
        results = cursor.fetchone() if single else cursor.fetchall()
    cursor.close()
    return results

# ensure db connection is closed when app torndown
@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()


#add route decorators
@app.route('/')
@app.route('/jobs')
def jobs():
    jobs=execute_sql('SELECT job.id, job.title, job.description,\
                      job.salary, employer.id as employer_id,\
                      employer.name as employer_name\
                      FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)





