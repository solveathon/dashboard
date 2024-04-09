import random
import string

def generatePassword(length=10):

    if length < 10:  length = 10
    
    digits = string.digits
    special_characters = '!@#$%^&*()_+=-'
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase

    password = [
        random.choice(digits),
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(special_characters),
    ]

    remaining_length = length - 4
    for _ in range(remaining_length):
        pool = [lowercase_letters, uppercase_letters, digits, special_characters]
        password.append(random.choice(random.choice(pool)))

    random.shuffle(password)

    password_str = ''.join(password)

    return password_str


from utils.db import Db
from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash

class User:

    def __init__(self, email, database):

        user = database.select(
            "SELECT * FROM users WHERE email = ?", email)
        
        if user:
            self.email, self.name, self.password, self.teamID, self.role  = user[0]

        else:
            self.email = None
            self.name = None
            self.password = None
            self.teamID = None
            self.role = None

    def checkPassword(self, password:str):
        return check_password_hash(self.password, password)
    
    def updatePassword(self, password:str, database:Db):
        self.password = generate_password_hash(password)
        database.query(
            "UPDATE users SET password = ? WHERE email = ?", 
            self.password, self.email, commit=True
        )


import smtplib
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmail(message, recipient, sender, subject, password):
    msg = MIMEMultipart('alternative')
    
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = formataddr((str(Header("Solve-A-Thon '24", 'utf-8')), sender))
    msg['To'] = recipient

    html_message = MIMEText(message, 'html')
    msg.attach(html_message)

    try:
        server = smtplib.SMTP_SSL('smtp.zoho.in', 465)
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email. Error:", str(e))


from redis import Redis
from itsdangerous import URLSafeTimedSerializer

def checkEmailToken(token:str, redisDB:Redis):

    if redisDB.exists(token):
        email = redisDB.get(token)
        redisDB.delete(token)
        return email.decode("utf-8")
    else:
        return False

def createPasswordResetLink(email, redisDB:Redis, serializer:URLSafeTimedSerializer):

    domain = "http://127.0.0.1:5000"

    token = serializer.dumps(
        salt="reset-password", obj={"email": email})

    redisDB.setex(token, 900, email) # Time to live of 15 minutes

    return domain + f"/reset-password/{token}"

