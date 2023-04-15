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