import os
import flask
import dotenv
import pyrebase
from redis import Redis
from datetime import datetime
from config import firebaseConfig

from utils import User
from utils.db import Db
from utils import sendEmail
from utils import checkEmailToken
from utils import generatePassword
from utils import createPasswordResetLink

from flask import request
from flask import redirect
from flask import session
from flask import render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from string import Template
from itsdangerous import URLSafeTimedSerializer

dotenv.load_dotenv()
database = Db('database.db')
redisDB = Redis(host='localhost', port=6379)
app = flask.Flask(__name__, static_url_path='/static')
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sessionDB.sqlite3'
app.config['SESSION_TYPE'] = 'sqlalchemy'

sessionDB = SQLAlchemy(app)
with app.app_context():
    sessionDB.create_all()

app.config['SESSION_SQLALCHEMY'] = sessionDB
_session = Session(app)

serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
firebase = pyrebase.initialize_app(firebaseConfig).database()

@app.route('/')
def dashboard():

    if 'logged_in' in session:

        eventDetails = firebase.child('eventDetails').get().val()

        if session['role'] == 'participant':

            colors = [
                'bg-label-danger',
                'bg-label-warning',
                'bg-label-success',
                'bg-label-primary',
            ]
            
            teamInfo = firebase.child('teams').child(session['teamID']).get().val()

            scores, rounds = {}, ['round1', 'round2', 'round3']
            comments = list(teamInfo['comments'].values())

            for _round in rounds:

                _rounds = teamInfo['score']

                if _rounds.get(_round):

                    score = _rounds.get(_round).values()

                    scores[_round] = round(sum(score) / len(score), 2)

                else:   scores[_round] = 0

            return render_template('dashboard.html', teamInfo=teamInfo,
                scores=scores, comments=comments, colors=colors, eventDetails=eventDetails)

        elif session['role'] == 'judge':
            judgeID = request.args.get('judgeID')
            return render_template('judges.html',
                judgeID=session['teamID'], eventDetails=eventDetails)
        else:
            return render_template('admin.html')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User(email, database)

        if user.email is None:
            return render_template('login.html', error=True)
        elif not user.checkPassword(password):
            return render_template('login.html', error=True)
        else:

            session.permanent = True
            session['logged_in'] = True
            session['role'] = user.role
            session['email'] = user.email
            session['teamID'] = user.teamID
            
            return redirect('/')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('role', None)
    session.pop('email', None)
    session.pop('teamID', None)

    return redirect('/login')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgotPassword():

    if request.method == 'POST':

        email = request.form['email']
        user = User(email, database)

        if user.email is None:
            return render_template('forgot-password.html', error=True)
        else:

            link = createPasswordResetLink(user.email, redisDB, serializer)

            HTML = Template(open(r"./templates/reset.html").read())

            message = HTML.safe_substitute(link=f"{link}")

            recipient = user.email
            sender = 'info@solveathon.in'
            subject = 'Password Reset'
            password = os.getenv('password')

            sendEmail(message, recipient, sender, subject, password)

            return render_template('forgot-password.html', success=True)
        
    return render_template('forgot-password.html', )

@app.route('/reset-password/<token>', methods=["GET"])
def resetPassword(token):

    email = checkEmailToken(token, redisDB)
    
    if email:

        user = User(email, database)

        if user.email is None:
            return redirect('/login')
        
        password = generatePassword()

        user.updatePassword(password, database)

        HTML = Template(open(r"./templates/password.html").read())
        message = HTML.safe_substitute(password=f"{password}", email=f"{email}")

        recipient = user.email
        sender = 'info@solveathon.in'
        subject = 'New Password'
        password = os.getenv('password')

        sendEmail(message, recipient, sender, subject, password)

        return render_template('login.html', newPassword=True)
    
    else:
        return redirect('/login')

@app.route('/team')
def team():

    if 'logged_in' in session:

        if session['role'] == 'participant':
            return redirect('/')
        else:
            teamID = request.args.get('teamID')

            eventDetails = firebase.child('eventDetails').get().val()
            teamInfo = firebase.child('teams').child(f'team_{teamID}').get().val()

            return render_template('team.html', teamInfo=teamInfo,
                    judgeID=session['teamID'], eventDetails=eventDetails)
    else:
        return redirect('/login')

@app.route('/submitGitHubLink', methods=['POST'])
def submitGitHubLink():

    teamID = session['teamID']

    commitLink = request.json['commitLink']
    
    try:
        firebase.child('teams').child(teamID).child(
            'githubLink').set(commitLink)
        return "Response <200>"
    
    except Exception as e:
        return f"Response <500>", 500

@app.route('/submitScore', methods=["POST"])
def submitScore():

    response = request.json

    judgeID = response['judgeID'].split('_')[-1]

    scores = list(map(int, [response['conceptScore'],
                            response['presentationScore'], response['executionScore']]))

    avgScore = round(sum(scores) / len(scores), 2)

    try:
        firebase.child('teams').child(f'team_{response["teamID"]}').child(
            'score').child(response['roundSelection']).child(f'judge{judgeID}').set(avgScore)
    except Exception as e:
        return "Response <500>", 500

    return "Response <200>", 200

@app.route('/addComment', methods=["POST"])
def addComment():

    teamID = request.json['teamID']
    comment = request.json['comment']
    judgeID = 'judge' + request.json['judgeID'].split('_')[-1]

    try:
        firebase.child('teams').child(f'team_{teamID}').child('comments').push({
            'judgeID' : judgeID,
            'comment' : comment,
            'timestamp' : datetime.now().strftime("%H:%M")
        })

    except Exception as e:
        print(e)
        return "Response <500>", 500

    return "Response <200>", 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0',
            port=os.getenv('PORT'))

