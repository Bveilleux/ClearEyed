#Breanna Veilleux
#EE 551 Introduction to Python
# Final "Mini" Project -- ClearEyed
# I pledge my honor that I have abided by the Stevens Honor System
# Please refer to project report for github, video, summary, and references. Thank you!!


from datetime import datetime, date, time
from flask import Flask, render_template, request, session, url_for, redirect, flash
import database
import random, copy
import os
from copy import deepcopy
from random import choice, shuffle

#setting up the Flask application

app = Flask(__name__)
app.secret_key = os.urandom(24)
database.create_tables()

#Here is the directory for all of the pages of the app

@app.route('/')
@app.route("/home")    
def home():
    return render_template(
        'home.html',
        title = 'ClearEyed'
    )

@app.route('/about')    
def about():
    return render_template(
        'about.html',
        title = 'About'
    )

@app.route("/Symptomtracker")
def tracker():
    return render_template(
      'tracker.html',
       title = 'Track My Progress'
   )

@app.route("/blog", methods=["GET", "POST"])
def blog():
    if request.method == "POST":
        entry_content = request.form.get("content")
        database.create_entry(entry_content, datetime.today().strftime("%b %d"))
    return render_template("blog.html", entries=database.retrieve_entries(), 
    title="Blog"
    )


#Begin Symptom Tracker 

questions = {

'1': {'answer': '0 - Never!','question': 'Are you experiencing headaches?', 'options': ['3 - Constantly', '2 - Often', '1 - Sometimes','0 - Never!' ]}, 
'2': {'answer': '0 - Never!','question': 'Are you experiencing dizziness?', 'options': ['3 - Constantly', '2 - Often', '1 - Sometimes','0 - Never!' ]}, 
'3': {'answer': '0 - Never!','question': 'Are you experiencing sensitvity to light?', 'options': ['3 - Constantly', '2 - Often', '1 - Sometimes','0 - Never!' ]}, 
'4': {'answer': '0 - Never!','question': 'Are you experiencing sensitivity to noise?', 'options': ['3 - Constantly', '2 - Often', '1 - Sometimes','0 - Never!' ]}, 
'5': {'answer': '0 - Never!','question': 'Are you experiencing sadness?', 'options': ['3 - Constantly', '2 - Often', '1 - Sometimes','0 - Never!' ]}, 
'6': {'answer': '0 - Never!','question': 'Are you experiencing irritability?', 'options': ['3 - Constantly', '2 - Often', '1 - Sometimes','0 - Never!' ]}, 
'7': {'answer': '0 - Never!','question': 'Are you experiencing eye strain?', 'options': ['3 - Constantly', '2 - Often', '1 - Sometimes','0 - Never!' ]}

}

py_summary={}
py_summary["correct"]=[]
py_summary["wrong"]=[]
py_summary["currentq"]=1
app.nquestions=len(questions)

#From the tracker page, the user selects the option to take the symptoms quiz which redirects here

@app.route('/symptoms', methods=['GET', 'POST'])
def index():
    #	
  if request.method == "POST":
    entered_answer = request.form.get('answer_quiz', '')

    if not entered_answer:
      flash("Please choose an answer", "error") 
    else:
      curr_answer=request.form['answer_quiz']
      correct_answer=questions[session["current_question"]]["answer"]
      #logic for if answer is "correct", meaning if the patient does not have any symptoms for a specific exercise
      #Therefore, they can move on and not complete that exercise
 
      if curr_answer == correct_answer[:len(curr_answer)]: 
        py_summary["correct"].append(int(session["current_question"]))
      
      else:
        py_summary["wrong"].append(int(session["current_question"]))
		
      # set the current question to the next number when checked
      session["current_question"] = str(int(session["current_question"])+1)
      py_summary["currentq"]= max(int(session["current_question"]), py_summary["currentq"])	  
   
      if session["current_question"] in questions:
        # If the question exists in the dictionary, redirect to the question
        redirect(url_for('index'))
      
      else:
        # output quiz summary upon completion
        py_summary["wrong"]=list(set(py_summary["wrong"]))
        py_summary["correct"]=list(set(py_summary["correct"]))		
        return render_template("quiz_end.html",summary=py_summary)
 
  if "current_question" not in session:
    session["current_question"] = "1" #Quiz not started yet, so set quiz number to 1
#  
  elif session["current_question"] not in questions:
    # Meaning quiz has been completed; return summary
    py_summary["wrong"]=list(set(py_summary["wrong"]))
    py_summary["correct"]=list(set(py_summary["correct"]))	
    return render_template("quiz_end.html",summary=py_summary)
  
  # If GET request 
  currentN=int(session["current_question"])   
  currentQ =  questions[session["current_question"]]["question"]
  a1, a2, a3,a4 = questions[session["current_question"]]["options"] 
  #end of quiz
  return render_template('quiz.html',num=currentN,ntot=app.nquestions,question=currentQ,ans1=a1,ans2=a2,ans3=a3,ans4=a4)   




#Physical Therapy Tracker
questions2 = {

'1': {'answer2': '2 minutes','question2': 'How long did you complete the Brock String exercise?', 'options2': ['30 seconds', '1 minute', '1.5 minutes','2 minutes' ]}, 
'2': {'answer2': '2 minutes','question2': 'How long did you complete the VOR (Visual Ocular Reflex) exercise?', 'options2': ['30 seconds', '1 minute', '1.5 minutes','2 minutes' ]}, 
'3': {'answer2': '2 minutes','question2': 'How long did you complete the VMS (Visual Motion Sensitivity) exercise?', 'options2': ['30 seconds', '1 minute', '1.5 minutes','2 minutes' ]}, 
'4': {'answer2': '2 minutes','question2': 'How long did you complete the Saccades exercise?', 'options2': ['30 seconds', '1 minute', '1.5 minutes','2 minutes' ]}, 
'5': {'answer2': 'The whole chart!','question2': 'How many lines did you complete the Hart Chart?', 'options2': ['5 lines', '10 lines', '15 lines','The whole chart!' ]}, 
'6': {'answer2': '2 minutes','question2': 'How long did you complete your balance exercise?', 'options2': ['30 seconds', '1 minute', '1.5 minutes','2 minutes' ]}, 
'7': {'answer2': 'More than 30 minutes','question2': 'How long did you complete cardio exercise?', 'options2': ['Less than 10 minutes', '10-20 minutes', '20-30 minutes','More than 30 minutes' ]}, 
}

py_summary2={}
py_summary2["correct2"]=[]
py_summary2["wrong2"]=[]
py_summary2["currentq2"]=1
app.nquestions2=len(questions2)


@app.route('/pt', methods=['GET', 'POST'])
def index2():
  if request.method == "POST":
    #post request for quiz      
    entered_answer2 = request.form.get('answer_quiz2', '')
    if not entered_answer2:
      flash("Please choose an answer", "error") 
    else:

      curr_answer2=request.form['answer_quiz2']
      correct_answer2=questions2[session["current_question2"]]["answer2"]
      #logic for if answer is "correct", meaning if the patient does not have any symptoms for a specific exercise
      #Therefore, they can move on and not complete that exercise

      if curr_answer2 == correct_answer2[:len(curr_answer2)]: 
        py_summary2["correct2"].append(int(session["current_question2"]))
      else:
        py_summary2["wrong2"].append(int(session["current_question2"]))

      # set the current question to the next number when checked
      session["current_question2"] = str(int(session["current_question2"])+1)
      py_summary2["currentq2"]= max(int(session["current_question2"]), py_summary2["currentq2"])	  
   
      if session["current_question2"] in questions2:
        # If the question exists in the dictionary, redirect to the question
        redirect(url_for('index2'))
      
      else:
        # else redirect to the summary template as the quiz is complete.
        py_summary2["wrong2"]=list(set(py_summary2["wrong2"]))
        py_summary2["correct2"]=list(set(py_summary2["correct2"]))		
        return render_template("quiz2_end.html",summary2=py_summary2)

  if "current_question2" not in session:
    # Quiz page is loaded. Set current question to #1 
    session["current_question2"] = "1"
  
  elif session["current_question2"] not in questions2:
    # If the current question not there, quiz is over. Redirect to summaary page.
    py_summary2["wrong2"]=list(set(py_summary2["wrong2"]))
    py_summary2["correct2"]=list(set(py_summary2["correct2"]))	
    return render_template("quiz2_end.html",summary2=py_summary2)
  
  # GET request 
  currentN2=int(session["current_question2"])   
  currentQ2 =  questions2[session["current_question2"]]["question2"]
  a12, a22, a32, a42 = questions2[session["current_question2"]]["options2"] 
  
  return render_template('quiz2.html',num=currentN2,ntot=app.nquestions2,question=currentQ2,ans12=a12,ans22=a22,ans32=a32,ans42=a42)   

