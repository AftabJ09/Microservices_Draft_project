from flask import Flask ,request,jsonify
import mysql.connector
import user_data_validation as validate
import model
def sighnup_validation(email):
    conn = model.get_db_connection()
    if conn is None:
        print('Connection Fail')
        return False
    try:
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
    
        if result[0] > 0:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            
def add_user(email,password,username):
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = "INSERT INTO users (email, password,username) VALUES (%s, %s, %s)"
        cursor.execute(query, (email,password,username))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()

def Login_validation(email,password):
    conn = model.get_db_connection()
    if conn is None:
        print('Connection Fail')
        return False
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        print(user)
        if user:
            if user[2] == password:
                return 'Allow'
            else:
                return 'wrong_password'
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()


def get_session_data(email):
    conn = model.get_db_connection()
    if conn is None:
        print('Connection Fail')
        return 'Connection Fail'
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        print('user data:   ',user)
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
    return user
    


app = Flask(__name__)


@app.route('/Validation',methods = ['GET','POST'])
def Validation():
    user_data = request.form
    email = user_data.get('email')
    password = user_data.get('password')
    name = user_data.get('name')
    if validate.is_valid_email(email) and validate.is_valid_password(password) and sighnup_validation(email):
        return 'Account Present'
    elif validate.is_valid_email(email) and validate.is_valid_password(password):
        add_user(email,password,name)
        return 'Login'
    else:
        return 'Invalid'


@app.route('/Login',methods = ['GET','POST'])
def Login():
    user_data = request.form
    email = user_data.get('email')
    password = user_data.get('password')
    if validate.is_valid_email(email) and validate.is_valid_password(password) and Login_validation(email,password) == 'Allow':
        user_data = get_session_data(email)
        return jsonify(user_data)
    elif validate.is_valid_email(email) and validate.is_valid_password(password) and Login_validation(email,password) == 'wrong_password':
        return 'Wrong_password'
    else:
        return 'Invalid'

