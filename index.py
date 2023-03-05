# /index.py
from flask import Flask, session, redirect, url_for,  request, flash, jsonify, render_template
import os
import dialogflow
import requests
import json
#import pusher

app = Flask(__name__)
app.config['SECRET_KEY'] = "thisisasecret!!!!"


@app.route("/logout")
def logout():
    data = {}
    data['fname']=session['fname']
    data['lname']=session['lname']
    data['email']=session['email']
    session.clear()
    return render_template('logout.html',data=data)


@app.route('/index')
def index():
    flash("welcome")
    return render_template('index.html',session=session)

@app.route('/login',methods=['GET','POST'])
def login():
  if request.method == 'POST':
        
        fname = request.form['firstname']
        lname = request.form['lastname']
        email = request.form['email']
        session['fname']=fname
        session['lname']=lname
        session['email']=email
        flash('You were successfully logged in!')
        return redirect(url_for('index'))

  elif request.method == 'GET':
    return render_template('login.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    print(data)
    reply = {"fulfillment":"FROM WEBHOOK!"}
    return jsonify(reply)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)


# run Flask app
if __name__ == "__main__":
    app.run()
