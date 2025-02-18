from flask import Flask ,request,jsonify
import requests

app = Flask(__name__)

@app.route('/api-register',methods=['GET','POST'])
def register():
    api_url = 'http://127.0.0.1:5003/Validation'
    user_data = request.form
    response = requests.post(api_url,data=user_data)
    return response.text


@app.route('/api-login',methods=['GET','POST'])
def login():
    api_url = 'http://127.0.0.1:5003/Login'
    user_data = request.form
    response = requests.post(api_url,data=user_data)
    return response.text


@app.route('/api-add-queastion',methods = ['GET','POST'])
def add_queastion():

    api_url = 'http://127.0.0.1:5004/add_queastion'
    queastions_data = request.form
    response = requests.post(api_url,data = queastions_data)
    return response.text


@app.route('/api-get-topics',methods = ['GET','POST'])
def get_topics():
    api_url = 'http://127.0.0.1:5004/get-topics'
    response = requests.post(api_url)
    return response.text

@app.route('/api-get-questions',methods = ['GET','POST'])
def get_questions():
    api_url = 'http://127.0.0.1:5004/get-questions'
    topic = request.form.to_dict()
    response = requests.post(api_url,data = topic)
    return response.text


@app.route('/api-get-question_data',methods = ['GET','POST'])
def get_specific_question_data():
    api_url = 'http://127.0.0.1:5004/get-specific-question-data'
    question_id = request.form.to_dict()
    response = requests.post(api_url,data = question_id)
    return response.text

@app.route('/api-delete-question_data',methods = ['POST'])
def delete_specific_question_data():
    api_url = 'http://127.0.0.1:5004/delete-specific-question-data'
    question_id = request.form.to_dict()
    response = requests.post(api_url,data = question_id)
    return response.text

@app.route('/api-delete-topic',methods = ['POST'])
def delete_tpic():
    api_url = 'http://127.0.0.1:5004/delete-a-topic'
    question_id = request.form.to_dict()
    response = requests.post(api_url,data = question_id)
    return response.text

@app.route('/api-update_question', methods=['POST'])
def update_specific_question_data():
    api_url = 'http://127.0.0.1:5004/update-specific-question-data'
    queastions_data = request.get_json()
    print("The update function is having following data:")
    response = requests.post(api_url, json=queastions_data)
    return jsonify(response.json()), response.status_code


@app.route('/api-submit-result',methods = ['POST'])
def submit_result():
    api_url = 'http://127.0.0.1:5005/submit_score'
    score_data = request.form.to_dict()
    response = requests.post(api_url,data = score_data)
    return response.status_code


@app.route('/api-get-score',methods = ['POST'])
def get_score():
    api_url = 'http://127.0.0.1:5005/get_score_data'
    score_data = request.form.to_dict()
    response = requests.post(api_url,data = score_data)
    return response.text





