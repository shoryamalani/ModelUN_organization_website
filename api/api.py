import time
from flask import Flask, jsonify, request , redirect, url_for, request, session
import dbs_worker
from User import User
from Committee import Committee
from Role import Role
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
    return jsonify({'userToken': session['user'],'userData': session['userData'],'userRole': session['userData']['role']})

@app.route('/api/getAllUsers')
def getAllUsers():
    return jsonify({'users': [User.from_data(a).convertUserDataToDictionary()  for a in dbs_worker.get_all_users()], 'roles': [Role(a,a[0]).convertRoleDataToDictionary() for a in dbs_worker.get_all_roles()]})

@app.route('/api/updateUserRole', methods=['POST'])
def updateUserRole():
    j = request.get_json()
    if j is None:
        return jsonify({'error': 'bad request'}), 400
    if(not session['userData']['role']['data']['seeOtherUsers']):
        return jsonify({'error': 'bad request'}), 400
    user_id = j.get('user_id', None)
    role_id = j.get('role_id', None)
    dbs_worker.set_user_role(user_id,role_id)
    return jsonify({'users': [User.from_data(a).convertUserDataToDictionary()  for a in dbs_worker.get_all_users()], 'roles': [Role(a,a[0]).convertRoleDataToDictionary() for a in dbs_worker.get_all_roles()]})

@app.route('/api/getAllCommittees')
def getAllCommittees():
    if("none" in session['userData']['role']['data']['permissions']):
        return jsonify({'error': 'bad request'}), 400
    return jsonify({'committees': [Committee.from_data(x).convertUserDataToDictionary() for x in dbs_worker.get_all_committees_with_permissions(session['userData']['role']['data']['permissions'])]})

@app.route('/api/getCommittee/<committee_id>')
def getCommittee(committee_id):
    print(committee_id)
    if committee_id is None:
        return jsonify({'error': 'bad request'}), 400
    if("chairing" in session['userData']['role']['data']):
        if(session['userData']['role']['data']['chairing']['committee_id'] == committee_id):
            return jsonify({'committee': Committee(committee_id).convertUserDataToDictionary()})
    committee = Committee(committee_id)
    if(committee.convertUserDataToDictionary()['type'] in session['userData']['role']['data']['permissions'] or "all" in session['userData']['role']['data']['permissions']):
        return jsonify({'committee': committee.convertUserDataToDictionary()})
    if("none" in session['userData']['role']['data']['permissions']):
        return jsonify({'error': 'bad request'}), 400
    return jsonify({'error': 'bad request'}), 400
@app.route('/api/addCommittee', methods=['POST'])
def addCommittee():
    j = request.get_json()
    if j is None:
        return jsonify({'error': 'bad request'}), 400
    if("none" in session['userData']['role']['data']['permissions']):
        return jsonify({'error': 'bad request'}), 400
    committee_name = j.get('name', None)
    committee_email = j.get('email', None)
    committee_type = j.get('type', None)
    Committee.create_committee(committee_name,committee_email,committee_type)
    return jsonify({'committees': [Committee.from_data(x).convertUserDataToDictionary() for x in dbs_worker.get_all_committees_with_permissions(session['userData']['role']['data']['permissions'])]})

@app.route('/api/updateCommitteeType', methods=['POST'])
def updateCommitteeType():
    j = request.get_json()
    if j is None:
        return jsonify({'error': 'bad request'}), 400
    if("none" in session['userData']['role']['data']['permissions']):
        return jsonify({'error': 'bad request'}), 400
    committee_id = j.get('committee_id', None)
    committee_type = j.get('type', None)
    val = Committee(committee_id)
    val.update_committee_type(committee_type)
    return jsonify({'committees': [Committee.from_data(x).convertUserDataToDictionary() for x in dbs_worker.get_all_committees_with_permissions(session['userData']['role']['data']['permissions'])]})
@app.route('/api/updateCommitteeBackgroundGuide', methods=['POST'])
def updateCommitteeBackgroundGuide():
    j = request.get_json()
    if j is None:
        return jsonify({'error': 'bad request'}), 400
    if("none" in session['userData']['role']['data']['permissions']):
        return jsonify({'error': 'bad request'}), 400
    committee_id = j.get('committee_id', None)
    committee_background_guide = j.get('background_guide', None)
    val = Committee(committee_id)
    val.update_committee_background_guide(committee_background_guide)
    return jsonify({'committee': Committee.from_data(x).convertUserDataToDictionary() for x in dbs_worker.get_all_committees_with_permissions(session['userData']['role']['data']['permissions'])})


if __name__ == "__main__":
    app.run(port=5003, debug=True)