import time
from flask import Flask, jsonify, request , redirect, url_for, request, session
import dbs_worker
from User import User
import os
import json
from functools import wraps
from flask import g, request, redirect, url_for

from flask_session import Session
app = Flask(__name__, static_folder='../build', static_url_path='/')
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.get("user",None) is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(404)
def not_found(e):
    print(e)
    return app.send_static_file('index.html')


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/about')
def about():
    print("about")
    return app.send_static_file('about.html')

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("login")
        j = request.get_json()
        if j is None:
            return jsonify({'error': 'bad request'}), 400
        token = j.get('userToken', None)
        g.user = token
        session['user'] = token
        print(g.get("user",None))
        # g.userData = User(j.get('name'),j.get('email', None),j.get('userToken', None)).convertUserDataToDictionary()
        session['userData'] = User(j.get('name'),j.get('email', None),j.get('userToken', None)).convertUserDataToDictionary()
        
        return jsonify({'userToken': g.get("user",None),'userData': g.get("userData",None)})
    else:
        return jsonify({'error': 'bad request'}), 400

@app.route('/api/getUserData')
def getUserData():
    print("getUserData")
    if 'user' not in session or "userData" not in session:
        print("no user")
        return jsonify({'error': 'bad request'}), 400
    print(session['user'])
    return jsonify({'userToken': session['user'],'userData': session['userData']})




if __name__ == "__main__":
    # app = Flask(__name__, static_folder='../src',static_url_path= '/')
    # data = dbs_worker.get_all_recent_bills(dbs_worker.set_up_connection())
    # for bill in data:
    #     print(bill["lastActionDate"])
    # print(congress_data_api.get_all_relevant_bill_info(dbs_worker.get_all_bills(dbs_worker.set_up_connection())))
    app.run(port=5003, debug=True)