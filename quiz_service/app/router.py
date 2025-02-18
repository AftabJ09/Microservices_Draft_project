from flask import Flask ,request,jsonify
import mysql.connector
import model


app = Flask(__name__)
def update_score_db(name, topic, score):  
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        print(topic, name, score)
        query = """
        INSERT INTO quiz_scores (name, topic, score) 
        VALUES (%s, %s, %s) 
        ON DUPLICATE KEY UPDATE score = VALUES(score);
        """
        cursor.execute(query, (name, topic, score))
        conn.commit()
        return True  
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
'''
def get_quiz_scores(name):
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = """
        SELECT topic,score FROM quiz_scores WHERE name = %s
        """
        cursor.execute(query, (name,))
        conn.commit()
        scores = cursor.fetchall()
        return scores  
    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
'''


def get_quiz_scores(name):
    conn = model.get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        while cursor.nextset():
            cursor.fetchall()
        query = "SELECT topic, score FROM quiz_scores WHERE name = %s"
        cursor.execute(query, (name,))
        scores = cursor.fetchall()
        return scores  

    except mysql.connector.Error as err:
        print(f"Error while querying the database: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()


@app.route('/submit_score', methods=['POST'])
def update_score():
    data = request.form.to_dict()
    name = data.get('name')
    topic = data.get('topic')
    score = data.get('score')
    if not name or not topic or not score:
        return "Invalid Data"
    if update_score_db(name, topic, score):  
        return "Update Successful"
    return "Update Failed"



@app.route('/get_score_data', methods=['POST'])
def get_score_data():
    data = request.form.to_dict()
    name = data.get('name')
    print(name)
    if not name :
        return jsonify({"error": "Invalid Data"}), 400
    scores = get_quiz_scores(name)  
    if scores:
        print(scores)
        return jsonify(scores)
    return jsonify({"message": "No quiz scores found"}), 200

