from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TOP-SECRET'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
responses = []

@app.route('/')
def survey_home():
    return render_template('survey_home.html', survey=survey)

@app.route('/begin', methods=['POST'])
def survey_start():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def handle_question():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/finish')
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route('/questions/<int:qid>')
def display_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template('questions.html', question_num=qid, question=question)

@app.route('/finish')
def finish():
    return render_template('finish.html')
