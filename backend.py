from flask import Flask, request, render_template, redirect, url_for,flash,jsonify,session
import psycopg2
from psycopg2 import Error
from flask_cors import CORS
from app import find_match,query_refiner,get_conversation_string,generate_alternative_questions,conversation,session_state
app = Flask(__name__)
# CORS(app)

app.secret_key='password'
username=None
@app.route('/')
def index():
    return render_template('login&signup.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        global username
        username = request.form.get('username')
        password = request.form.get('password')
        connection = psycopg2.connect(
            dbname="Project",
            user="postgres",
            password="22122001",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT name,last_qs1 FROM user_login WHERE email = %s and password=%s", (username,password))
        result = cursor.fetchone()
        # Redirect to a success page or handle login logic here
        if result:
            flash(f'Welcome {result[0]}','name')
            print(result[1])
            print(type(result[1]))
            last_qs1 = result[1] if result[1] else ""
            list = last_qs1.split(";") if last_qs1 else []
            list = [req for req in list if req]  # Remove empty strings
            list.pop()
            return render_template('new.html',list=list)
        else:
            flash('Incorrect email or password', 'error')
        cursor.close()
        connection.close()
        return redirect(url_for('error'))
    except (Exception, Error) as error:
        print("Error while fetching data from PostgreSQL", error)

@app.route('/error')
def error():
    return render_template('login&signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        email=request.form.get('email')
        name=request.form.get('name')
        phno=request.form.get('phno')
        password = request.form.get('password')
        connection = psycopg2.connect(
            dbname="Project",
            user="postgres",
            password="22122001",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        cursor.execute("INSERT into user_login values(%s,%s,%s,%s,%s)",(email,name,password,phno,'NULL'))
        connection.commit()
        flash('Data submitted successfully, Kindly login now','info')

        return render_template('login&signup.html')

        
    except (Exception, Error) as error:
        print("Error while fetching data from PostgreSQL", error)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json 
    user_message = data.get('message')
    print("User Message:", user_message)

    session_state['requests'].append(user_message)
    conversation_string = get_conversation_string(session_state['responses'], session_state['requests'])
    print("Conversation String:", conversation_string)

    if user_message.lower() in ["hi", "hello", "hey"]:
        response = "Hello! How can I help you?"
        refined_query=None
        alternatives=None
    elif user_message.lower() in ["thanks","great","thank you"]:
        response = "You are most welcome."
        refined_query=None
        alternatives=None
    elif user_message.lower() in ["How are you?","How are you"]:
        response= "I am fine, please let me know how may I help you."
        refined_query=None
        alternatives=None
    else:
        refined_query = query_refiner(conversation_string, user_message)
        print("Refined Query:", refined_query)

        context = find_match(refined_query)
        print("Context:", context)

        response = conversation.predict(input=f"Context:\n{context}\n\nQuery:\n{user_message}")
        print("Response:", response)
        #response = format_bold_text(response)
        alternatives=generate_alternative_questions(refined_query)
    session_state['responses'].append(response)

    return jsonify({
        "response": response,
        "related_questions":alternatives
    })

@app.route('/logout')
def logout():
    try:
        connection = psycopg2.connect(
            dbname="Project",
            user="postgres",
            password="22122001",
            host="localhost",
            port="5432"
        )
        session_state['requests']=[x for x in session_state['requests'] if x.lower() not in ["hi", "hello","hey","thanks","great"]]
        print(session_state['requests'])
        print(username)
        cursor = connection.cursor()
        update_query = "UPDATE user_login SET last_qs1 = COALESCE(last_qs1, '') || %s WHERE email = %s"
        for item in session_state['requests']:
            cursor.execute(update_query, (item + '; ', username))
        connection.commit()
        print('Data Updated Succesfully')
        cursor.close()
        connection.close()
        session_state.clear()
        flash("You have been logged out.", "info")
        return render_template('login&signup.html')
    except (Exception, Error) as error:
        print("Error while fetching data from PostgreSQL", error)

if __name__ == '__main__':
    app.run(debug=True,port=5004)
