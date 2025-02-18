from flask import Flask ,request,render_template,session,jsonify, redirect,url_for
import requests


app = Flask(__name__)

app.secret_key = 'afu50100'

def get_name():
    user_name = session.get('name',None)
    return user_name

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup_page',methods=['GET'])
def signup():
    return render_template('index.html')

@app.route('/login_page')
def login():
    return render_template('login.html')

@app.route('/admin_login_page')
def admin_login():
    return render_template('admin.html')

@app.route('/add-queastion')
def add_queastion():
    return render_template('add_questions.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/edit_specific_question')
def edit_specific_question():
    api_url = 'http://127.0.0.1:5002/api-get-question_data'
    question_id = request.args.get('edit')
    data = {'id':question_id}
    response = requests.post(api_url,data = data)
    session['question_id'] = question_id
    question_data = response.json()
    print(question_data,'Aftab Data tested')
    if int(question_id) == question_data[0][0]:
        return render_template('editor.html',question_data = question_data[0])


@app.route('/quiz_questions')
def get_quiz_question():
    api_url = 'http://127.0.0.1:5002/api-get-questions'
    button_id = request.args.get('choose_btn')
    data = {'topic':button_id}
    response = requests.post(api_url,data=data)
    questions_data = response.json()
    questions_data = [questions for questions in questions_data]
    answers = [question[7] for question in questions_data]
    session['correct_answers'] = answers
    print('The answers are',answers)
    return render_template('quiz_portal.html',questions = questions_data,topic = button_id)


@app.route('/delete_specific_question')
def delete_specific_question():
    button_id = request.args.get('edit_btn')
    api_url = 'http://127.0.0.1:5002/api-get-questions'
    data = {'topic':button_id}
    response = requests.post(api_url,data=data)
    questions_data = response.json()
    questions_data = [questions for questions in questions_data]
    return render_template('question_list.html',questions = questions_data,topic = button_id)




@app.route('/update_question', methods=['POST'])
def update_question():
    if 'question_id' not in session:
        return jsonify({'error': 'Session expired or not set'}), 400

    print('This is the data for the question details', session['question_id'])
    api_url = 'http://127.0.0.1:5002/api-update_question'
    question_id = session['question_id']

    data = request.form  
    queastions_data = {
        'question_id': question_id,
        'question': data.get('question'),
        'A': data.get('option1'),
        'B': data.get('option2'),
        'C': data.get('option3'),
        'D': data.get('option4'),
        'answer': data.get('answer')
    }
    print(queastions_data)
    response = requests.post(api_url, json=queastions_data)  
    if response.status_code == 200:
        return render_template('admin_dashboard.html', user_name=session['name'])



@app.route('/Edit-Topics')
def edit():
    api_url = 'http://127.0.0.1:5002/api-get-topics'
    response = requests.post(api_url)
    topics = response.json()
    topics = [topic[0] for topic in topics]
    count = len(topics)
    return render_template('topic_list.html',topics = topics,count = count)


@app.route('/Delete-Topics')
def delete():
    api_url = 'http://127.0.0.1:5002/api-get-topics'
    response = requests.post(api_url)
    topics = response.json()
    topics = [topic[0] for topic in topics]
    count = len(topics)
    return render_template('delete_topic.html',topics = topics,count = count)

@app.route('/quiz-topics')
def choose_topic():
    api_url = 'http://127.0.0.1:5002/api-get-topics'
    response = requests.post(api_url)
    topics = response.json()
    topics = [topic[0] for topic in topics]
    count = len(topics)
    return render_template('choose_topic.html',topics = topics,count = count)



@app.route('/Delete-Topic')
def delete_topic():
    api_url = 'http://127.0.0.1:5002/api-delete-topic'
    topic = request.args.get('delete_btn')
    data = {'topic':topic}
    response = requests.post(api_url,data = data)
    if response.status_code == 200:
        return render_template('admin_dashboard.html', user_name=session['name'])


@app.route('/Edit-Questions')
def edit_question():
    button_id = request.args.get('edit_btn')
    api_url = 'http://127.0.0.1:5002/api-get-questions'
    data = {'topic':button_id}
    response = requests.post(api_url,data=data)
    questions_data = response.json()
    questions_data = [questions for questions in questions_data]
    return render_template('question_list.html',questions = questions_data,topic = button_id)

@app.route('/submit_quiz',methods=['POST'])
def submit():
    api_url = 'http://127.0.0.1:5002/api-submit-result'
    quiz_answers = [request.form[key] for key in request.form]
    correct_answers = session['correct_answers']
    score = 0
    for i in range(len(correct_answers)):
        if correct_answers[i] == quiz_answers[i+1]:
            score += 1
    name = session['name']
    topic = quiz_answers[0]
    data = {
        'name': name,
        'topic': topic,
        'score': score
    }
    response = requests.post(api_url,data=data)
    print(response.status_code)
    if response.status_code == 200:
        return render_template('dashboard.html', user_name=session['name'])
    return render_template('dashboard.html', user_name=session['name'])


@app.route('/open_score_board', methods=['GET'])
def score_board():
    message = ''
    api_url = 'http://127.0.0.1:5002/api-get-score'
    name = session.get('name') 
    data = {'name': name}
    response = requests.post(api_url, data=data)
    try:
        scores = response.json()
    except ValueError:
        scores = []
    if not isinstance(scores, list):
        scores = []
    count = len(scores)
    if count == 0:
        message = "You have not attended any quiz yet."

    return render_template('scoreboard.html', scores=scores, name=name, message=message, count=count)

'''
@app.route('/open_score_board',methods=['GET'])
def score_board():
    message = ''
    api_url = 'http://127.0.0.1:5002/api-get-score'
    name = session['name']
    data = {'name':name}
    response = requests.post(api_url,data=data)
    scores = response.json()
    count = len(scores)
    if not scores:
        message = "You have not attended any quiz yet."
    return render_template('scoreboard.html', scores=scores,name=session['name'], message=message,count = count)
    
'''


@app.route('/registration',methods=['GET','POST'])
def register():
    api_url = 'http://127.0.0.1:5002/api-register'
    email = request.args.get('email')
    password = request.args.get('password')
    name = request.args.get('name')
    user_data = {'email':email,'password':password,'name':name}
    response = requests.post(api_url,data=user_data)

    if response.text == 'Login':
        return render_template('login.html')
    elif response.text == 'Account Present':
        message1 = "Account present please Login"
        return render_template('index.html', message=message1)
    else:
        message2 = "Please fill in the details again."
        return render_template('index.html', message=message2)




@app.route('/Login', methods=['GET', 'POST'])
def Login():
    api_url = 'http://127.0.0.1:5002/api-login'
    email = request.args.get('email') 
    password = request.args.get('password')
    user_data = {'email': email, 'password': password}
    response = requests.post(api_url, data=user_data)
    try:
        data = response.json()          
        if data[1] == email and data[2] == password:
            session['user_id'] = data[0]
            session['email'] = data[1]
            session['name'] = data[3]
            user_name = get_name() 
            return render_template('dashboard.html', user_name=user_name)
        else:
            message = 'Unexpected response from the user service'
            return render_template('login.html', message=message)
    
    except ValueError:
        if response.text == 'Wrong_password':
            message = "The password is wrong, please try again"
        elif response.text == 'Invalid':
            message = 'The user with this email address not found'
        else:
            message = 'An unexpected error occurred. Please try again.'
        
        return render_template('login.html', message=message)




@app.route('/Admin_Login',methods=['GET','POST'])
def AdminLogin():
    api_url = 'http://127.0.0.1:5002/api-login'
    email = request.args.get('email')
    password = request.args.get('password')
    code = request.args.get('code')
    user_data = {'email':email,'password':password}
    response = requests.post(api_url,user_data)
    try:
        data = response.json()          
        if data[1] == email and data[2] == password and code == 'Admin':
            session['user_id'] = data[0]
            session['email'] = data[1]
            session['name'] = data[3]
            user_name = get_name() 
            return render_template('admin_dashboard.html', user_name=user_name)
        else:
            message = 'Unexpected response from the user service'
            return render_template('login.html', message=message)
    
    except ValueError:
        if response.text == 'Wrong_password':
            message = "The password or the admin code is wrong, please try again"
        elif response.text == 'Invalid':
            message = 'The user with this email address not found'
        else:
            message = 'An unexpected error occurred. Please try again.'
        
        return render_template('admin.html', message=message)


@app.route('/Add_datas',methods=['GET','POST'])
def addQueastions():
    api_url = 'http://127.0.0.1:5004/add_queastion'
    topic =  request.args.get('topic')
    queastions = request.args.get('question')
    A = request.args.get('option1')
    B = request.args.get('option2')
    C = request.args.get('option3')
    D = request.args.get('option4')
    answer = request.args.get('answer')
    queastions_data = {'topic':topic,'question':queastions,'A':A,'B':B,'C':C,'D':D,'answer':answer}
    response = requests.post( api_url, data=queastions_data)
    message = response.text
    return render_template('add_questions.html',message=message)

@app.route('/Add_data',methods=['GET'])
def testing():
    api_url = 'http://127.0.0.1:5002/api-add-queastion'
    topic =  request.args.get('topic')
    queastions = request.args.get('question')
    A = request.args.get('option1')
    B = request.args.get('option2')
    C = request.args.get('option3')
    D = request.args.get('option4')
    answer = request.args.get('answer')
    print(topic,queastions,A,B,C,D,answer)
    queastions_data = {'topic':topic,'question':queastions,'A':A,'B':B,'C':C,'D':D,'answer':answer}
    response = requests.post( api_url, data=queastions_data)
    return render_template('add_questions.html',message = response.text)
