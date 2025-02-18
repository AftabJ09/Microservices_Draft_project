from flask import Flask ,request,jsonify
import mysql.connector
import model

def add(topic,queastions,A,B,C,D,answer):
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = "INSERT INTO questions (topic,questions,A,B,C,D,answer) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (topic,queastions,A,B,C,D,answer))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            return True
    return True



def update(queastions, A, B, C, D, answer, id):
    conn = model.get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        query = "UPDATE questions SET questions = %s, A = %s, B = %s, C = %s, D = %s, answer = %s WHERE id = %s;"
        cursor.execute(query, (queastions, A, B, C, D, answer, id))
        conn.commit()
        return True  
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()  



def get_topics():
    topics = []
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = "SELECT DISTINCT topic from questions"
        cursor.execute(query)
        topics = cursor.fetchall()
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
    return topics

def get_questions(topic):
    questions = []
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        print('This is the topic',topic)
        query = "SELECT id,topic,questions,A,B,C,D,answer from questions WHERE topic = %s"
        cursor.execute(query,(topic,))
        questions = cursor.fetchall()
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
    return questions

def specific_question_data(question_id):
    question_data = []
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = "SELECT id,topic,questions,A,B,C,D,answer from questions WHERE id = %s"
        cursor.execute(query,(question_id,))
        question_data = cursor.fetchall()
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
    return question_data

def delete_specific_data(question_id):
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM questions WHERE id = %s"
        cursor.execute(query,(question_id,))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
    return True

def delete_topic(topic):
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM questions WHERE topic = %s"
        cursor.execute(query,(topic,))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
    return True



app = Flask(__name__)

@app.route('/add_queastion',methods = ['GET','POST'])
def add_queastion():
    queastions_data = request.form
    topic = queastions_data.get('topic')
    queastions = queastions_data.get('question')
    A = queastions_data.get('A')
    B = queastions_data.get('B')
    C = queastions_data.get('C')
    D = queastions_data.get('D')
    answer = queastions_data.get('answer')
    
    if add(topic,queastions,A,B,C,D,answer):
        return 'Question is added Sucessfully'
    else:
        return 'Try again'

@app.route('/get-topics',methods = ['GET','POST'])
def get_topics_data():
    topics = get_topics()
    return jsonify(topics)


@app.route('/get-questions',methods = ['GET','POST'])
def get_questions_data():
    topic = request.form
    questions = get_questions(topic.get('topic'))
    print('This is the topic',topic)
    return jsonify(questions)

@app.route('/get-specific-question-data',methods = ['GET','POST'])
def get_specific_question_data():
    question_id = request.form
    questions = specific_question_data(question_id.get('id'))
    return jsonify(questions)

@app.route('/delete-specific-question-data',methods = ['GET','POST'])
def delete_specific_question_data():
    question_id = request.form
    if delete_specific_data(question_id.get('id')):
        return jsonify({"message": "Update successful"}), 200
    return  jsonify({"error": "Update failed"}), 500 


@app.route('/delete-a-topic',methods = ['GET','POST'])
def delete_specific_topic():
    topic = request.form
    topic = dict(topic)
    if delete_topic(topic.get('topic')):
        return jsonify({"message": "Update successful"}), 200
    return  jsonify({"error": "Update failed"}), 500 





@app.route('/update-specific-question-data', methods=['POST'])
def update_queastion():
    print('Reached the UPDATE QUESTION')
    queastions_data = request.get_json()
    question_id = queastions_data.get('question_id')
    queastions = queastions_data.get('question')
    A = queastions_data.get('A')
    B = queastions_data.get('B')
    C = queastions_data.get('C')
    D = queastions_data.get('D')
    answer = queastions_data.get('answer')
    print(queastions, A, B, C, D, answer, question_id)
    if update(queastions, A, B, C, D, answer, question_id):
        return jsonify({"message": "Update successful"}), 200
    return  jsonify({"error": "Update failed"}), 500 



