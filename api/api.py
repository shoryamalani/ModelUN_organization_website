import time
from flask import Flask, jsonify, request , redirect, url_for, request
import dbs_worker
import os
import json
from functools import wraps
from flask import g, request, redirect, url_for
app = Flask(__name__, static_folder='../build', static_url_path='/')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


@app.route('/')
def index():
    return app.send_static_file('index.html')







if __name__ == "__main__":
    # app = Flask(__name__, static_folder='../src',static_url_path= '/')
    # data = dbs_worker.get_all_recent_bills(dbs_worker.set_up_connection())
    # for bill in data:
    #     print(bill["lastActionDate"])
    # print(congress_data_api.get_all_relevant_bill_info(dbs_worker.get_all_bills(dbs_worker.set_up_connection())))
    app.run(port=5003, debug=True)