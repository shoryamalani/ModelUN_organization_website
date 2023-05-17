from dbs_scripts import write_and_read_to_database,execute_db,create_database
import Role, User, Event, Committee, DueDate
import dotenv
import os
import json
import psycopg2
import datetime
import pypika
from pypika import functions,Query
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )
def set_up_connection():
    # Path to .env file
    if not is_docker():
        dotenv_path = os.path.join(os.path.dirname(__file__), '../postgres/.env')
        # Load file from the path
        dotenv.load_dotenv(dotenv_path)
        # set up connection to postgres
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST_DEV'),
            database=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        )
        return conn

    else:

        # dotenv_path = os.path.join(os.path.dirname(__file__), '/postgres/.env')
        # print(dotenv_path)
        print(os.listdir())
        # # Load file from the path
        # print(dotenv.load_dotenv(dotenv_path,verbose=True))
        # print(dotenv.dotenv_values(dotenv_path).items())
        dotenv.load_dotenv()

        # set up connection to postgres
        print(os.environ)
        print(os.environ.get('DB_HOST'))

        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            port=os.environ.get('DB_PORT')
        )
        return conn

def get_db_version(conn):
    sys = pypika.Table("sys")
    query = Query.from_(sys).select('*')
    try:
        data = execute_db.execute_database_command(conn,query.get_sql())[1]
        return data.fetchone()[1]
    except:
        return 0    


def set_up_db_version_1(conn):
    sys_table = create_database.create_table_command("sys",[['id','int'],['version','int']],'id')
    try:
        conn = execute_db.execute_database_command(set_up_connection(),sys_table)
        conn[0].commit()
        sys = pypika.Table('sys')
        set_up_version = sys.insert([0,1])
        users_table = create_database.create_table_command("users",[['UUID','SERIAL'],['name','varchar(255)'],['email','varchar(255)'],['google_access_token','varchar(255)'],['date_created','timestamp'],['last_login','timestamp'],['role','integer'],['data','json']],'UUID')
        execute_db.execute_database_command(set_up_connection(),users_table)[0].commit()
        users_roles_table = create_database.create_table_command("users_roles",[['id','SERIAL'],['name','varchar(255)'],['data','json']],'id')
        execute_db.execute_database_command(set_up_connection(),users_roles_table)[0].commit()
        # create relation between 
        relation_between_roles_and_users = create_database.create_relation_in_tables("users","role","users_roles","id")
        execute_db.execute_database_command(set_up_connection(),relation_between_roles_and_users)[0].commit()
        
        # create committee table
        committee_table = create_database.create_table_command("committees",[['id','SERIAL'],['name','varchar(255)'],['data','json']],'id')
        execute_db.execute_database_command(set_up_connection(),committee_table)[0].commit()
        # create events and messages table
        events_table = create_database.create_table_command("events",[['id','SERIAL'],['name','varchar(255)'],['completed','bool'],['data','json']],'id')
        execute_db.execute_database_command(set_up_connection(),events_table)[0].commit()
        # due dates
        due_dates_table = create_database.create_table_command("due_dates",[['id','SERIAL'],['name','varchar(255)'],['data','json']],'id')
        execute_db.execute_database_command(set_up_connection(),due_dates_table)[0].commit()

        execute_db.execute_database_command(set_up_connection(),set_up_version.get_sql())[0].commit()

    except Exception as e:
        print(e)
        print("failed")
        pass


def db_init():
    conn = set_up_connection()
    print(get_db_version(conn))
    if get_db_version(conn) < 1:
        set_up_db_version_1(conn)
    
def get_all_users():
    conn = set_up_connection()
    users = pypika.Table('users')
    query = Query.from_(users).select('*')
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    return data.fetchall()

def get_all_committees():
    conn = set_up_connection()
    committees = pypika.Table('committees')
    query = Query.from_(committees).select('*')
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    return data.fetchall()

def get_all_events():
    conn = set_up_connection()
    events = pypika.Table('events')
    query = Query.from_(events).select('*')
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    return data.fetchall()

def get_all_due_dates():
    conn = set_up_connection()
    due_dates = pypika.Table('due_dates')
    query = Query.from_(due_dates).select('*')
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    return data.fetchall()

def get_all_roles():
    conn = set_up_connection()
    roles = pypika.Table('users_roles')
    query = Query.from_(roles).select('*')
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    return data.fetchall()

def get_users_role(user_id):
    # find the user and find the role associate with it
    conn = set_up_connection()
    users = pypika.Table('users')
    query = Query.from_(users).select('*').where(users.UUID == user_id)
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    user = data.fetchone()
    if user:
        users_roles = pypika.Table('users_roles')
        query = Query.from_(users_roles).select('*').where(users_roles.id == user[6])
        data = execute_db.execute_database_command(conn,query.get_sql())[1]
        role = data.fetchone()
        if role:
            return Role(role)
        else:
            return None

def get_user_by_id(user_id):
    conn = set_up_connection()
    users = pypika.Table('users')
    query = Query.from_(users).select('*').where(users.UUID == user_id)
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    user = data.fetchone()
    if user:
        return User(user)
    else:
        return None
    
def get_event_by_id(event_id):
    conn = set_up_connection()
    events = pypika.Table('events')
    query = Query.from_(events).select('*').where(events.id == event_id)
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    event = data.fetchone()
    if event:
        return Event(event)
    else:
        return None
    
def get_committee_by_id(committee_id):
    conn = set_up_connection()
    committees = pypika.Table('committees')
    query = Query.from_(committees).select('*').where(committees.id == committee_id)
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    committee = data.fetchone()
    if committee:
        return Committee(committee)
    else:
        return None

def get_due_date_by_id(due_date_id):
    conn = set_up_connection()
    due_dates = pypika.Table('due_dates')
    query = Query.from_(due_dates).select('*').where(due_dates.id == due_date_id)
    data = execute_db.execute_database_command(conn,query.get_sql())[1]
    due_date = data.fetchone()
    if due_date:
        return DueDate(due_date)
    else:
        return None
    
def add_user(name,email,google_access_token,role,data):
    """add a user to the database

    Args:
        name (string): name
        email (string): email
        google_access_token (string): token
        role (uuid): uuid of role
        data (object): any data
    """
    conn = set_up_connection()
    users = pypika.Table('users')
    query = Query.into(users).columns('name','email','google_access_token','role','data','date_created','last_login').insert(name,email,google_access_token,role,data,functions.Now(),functions.Now())
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def add_event(name,data):
    """add an event to the database

    Args:
        name (string): name
        completed (bool): completed
        data (object): any data
    """
    conn = set_up_connection()
    events = pypika.Table('events')
    query = Query.into(events).columns('name','completed','data').insert(name,False,data)
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def add_committee(name,data):
    """add a committee to the database

    Args:
        name (string): name
        data (object): any data
    """
    conn = set_up_connection()
    committees = pypika.Table('committees')
    query = Query.into(committees).columns('name','data').insert(name,data)
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def add_due_date(name,date,data):
    """add a due date to the database

    Args:
        name (string): name
        date (date): date
        data (object): any data
    """
    conn = set_up_connection()
    due_dates = pypika.Table('due_dates')
    query = Query.into(due_dates).columns('name','date','data').insert(name,date,data)
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def add_role(name,data):
    """add a role to the database

    Args:
        name (string): name
        data (object): any data
    """
    conn = set_up_connection()
    roles = pypika.Table('users_roles')
    query = Query.into(roles).columns('name','data').insert(name,data)
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def update_user(user_id,name,email,google_access_token,role,data):
    """update a user in the database

    Args:
        user_id (uuid): uuid of user
        name (string): name
        email (string): email
        google_access_token (string): token
        role (uuid): uuid of role
        data (object): any data
    """
    conn = set_up_connection()
    users = pypika.Table('users')
    query = Query.update(users).set(users.name,name).set(users.email,email).set(users.google_access_token,google_access_token).set(users.role,role).set(users.data,data).set(users.last_login,functions.Now()).where(users.UUID == user_id)
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def update_event(event_id,name,completed,data):
    """update an event in the database

    Args:
        event_id (uuid): uuid of event
        name (string): name
        completed (bool): completed
        data (object): any data
    """
    conn = set_up_connection()
    events = pypika.Table('events')
    query = Query.update(events).set(events.name,name).set(events.completed,completed).set(events.data,data).where(events.UUID == event_id)
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def update_committee(committee_id,name,data):
    """update a committee in the database

    Args:
        committee_id (uuid): uuid of committee
        name (string): name
        data (object): any data
    """
    conn = set_up_connection()
    committees = pypika.Table('committees')
    query = Query.update(committees).set(committees.name,name).set(committees.data,data).where(committees.UUID == committee_id)
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def update_due_date(due_date_id,name,date,data):
    """update a due date in the database

    Args:
        due_date_id (uuid): uuid of due date
        name (string): name
        date (date): date
        data (object): any data
    """
    conn = set_up_connection()
    due_dates = pypika.Table('due_dates')
    query = Query.update(due_dates).set(due_dates.name,name).set(due_dates.date,date).set(due_dates.data,data).where(due_dates.UUID == due_date_id)
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def update_role(role_id,name,data):
    """update a role in the database

    Args:
        role_id (uuid): uuid of role
        name (string): name
        data (object): any data
    """
    conn = set_up_connection()
    roles = pypika.Table('users_roles')
    query = Query.update(roles).set(roles.name,name).set(roles.data,data).where(roles.UUID == role_id)
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def delete_user(user_id):
    """delete a user from the database

    Args:
        user_id (uuid): uuid of user
    """
    conn = set_up_connection()
    users = pypika.Table('users')
    query = Query.from_(users).where(users.UUID == user_id).delete()
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def delete_event(event_id):
    """delete an event from the database

    Args:
        event_id (uuid): uuid of event
    """
    conn = set_up_connection()
    events = pypika.Table('events')
    query = Query.from_(events).where(events.UUID == event_id).delete()
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def delete_committee(committee_id):
    """delete a committee from the database

    Args:
        committee_id (uuid): uuid of committee
    """
    conn = set_up_connection()
    committees = pypika.Table('committees')
    query = Query.from_(committees).where(committees.UUID == committee_id).delete()
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def delete_due_date(due_date_id):
    """delete a due date from the database

    Args:
        due_date_id (uuid): uuid of due date
    """
    conn = set_up_connection()
    due_dates = pypika.Table('due_dates')
    query = Query.from_(due_dates).where(due_dates.UUID == due_date_id).delete()
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()

def delete_role(role_id):
    """delete a role from the database

    Args:
        role_id (uuid): uuid of role
    """
    conn = set_up_connection()
    roles = pypika.Table('users_roles')
    query = Query.from_(roles).where(roles.UUID == role_id).delete()
    execute_db.execute_database_command(conn,query.get_sql())[0].commit()
