from flask import *
from flask_mail import Mail, Message
from db.connection import Connection
import pickle
from DataFrameCreation import FeatureExtraction
import pandas as pd
import secrets
import string
import urllib.parse
import report
from report import report_phishing_url as rpu
model = pickle.load(open("gbcmodel.pkl", "rb"))
app = Flask(__name__)
app.secret_key = '16102002'  # Add a secret key for session management
conn = Connection()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'phishguard000@gmail.com'
app.config['MAIL_PASSWORD'] = 'jinp bbcy qwcp qzfp'
mail = Mail(app)
try:
    conn.create(3)
    conn.create(2)
except:
    print("table not created")

@app.route("/")
def splashScreen():
    return render_template("splashScreen.html")

@app.route("/welcome")
def welcomePage():
    return render_template("welcomePage.html")



@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    registration=False
    meth=request.method
    if 'username' in session:
        return render_template('homepage.html',username=session['username'],status=True,show_popup=True,meth=meth)
    if request.method == 'POST':
        uname = request.form.get('reg-username')
        email = request.form.get('reg-email')
        pwd = request.form.get('reg-password')
        confirm_pwd = request.form.get('confirm-password')
        
        # query = f"insert into users values('{uname}','{email}','{pwd}','{confirm_pwd}')"
        
        status = conn.insert("phishing_users_db", uname, email, pwd)
        print(status)
        if status==None:
            body="UserName already exists"
            print(body)
            return render_template('signup.html',registration=False,meth=meth,body=body)
        print(status)
        if status:
              # Set the username in session upon successful registration
            
            return render_template('login.html',registration=True,meth=meth,body="registration succesful !....")
        else:
            print("else",meth)
            return render_template('signup.html', registration=False,meth=meth,body="registration unsucessful!..")
    else:
        return render_template('signup.html',meth=meth,registration=registration)

@app.route('/login', methods=['POST', 'GET'])
def login_validate():
    head=""
    body=""
    meth=request.method
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        show_popup=False
        query = f"select * from phishing_users_db where uname='{username}' and pwd='{password}';"
        row = conn.execute(query)
        
        if row is not None:
            session['username'] = username  # Set the username in session upon successful login
            
            return render_template('homepage.html',username=username,status=True,show_popup=True,meth=meth)
        else:
            
            return render_template('login.html', show_popup=False,meth=meth)
    else:
        if 'username' in session:  # Check if the user is already logged in
            # return redirect(url_for('homepage'))
            return render_template("homepage.html",status=True, username=session['username'])
        else:
            return render_template('login.html')

@app.route("/homepage", methods=["POST", "GET"])
def homepage():
    if 'username' not in session:  # Check if the user is logged in
        return redirect(url_for('login_validate'))
    
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("homepage.html",status=True, username=session['username'])
        extractor=FeatureExtraction(url)
        
        if( not extractor.check_for_validity(url)):
            return render_template('homepage.html',status=False ,body="please Check the entered url!..... ",username=session['username'])
        else:
            url_extracted_data=extractor.create_extracted_list()

            print(url_extracted_data)
        
            url_status=model.predict(pd.DataFrame([url_extracted_data]))
            if not url_status:
                return render_template("homepage.html",status=True,warning_condition="yes")
            else:
                query = f"select * from phishingDataBase where url='{url}';"
                row = conn.execute(query)
                do = True
                if row is not None:
                    do = False
                if url_status[0]==1:
                    print("legitimate")
                    if do:
                        conn.insert("phishingDataBase",url,"Legitimate/Safe To Use")
                    return render_template("result.html",url=url,url_status="is safe to use")
                else:
                    print("phishing")
                    status=False
                    if do:
                        status = conn.insert("phishingDataBase",url,"Phishing/May not be Safe to use")
                    if status:
                        print("url succesfully saved in database")
                    else:
                        print("error in url saving to database")
                    return render_template("result.html",url=url,url_status="may not be safe to use.....")


    else: 
        print(session['username'])
        return render_template("homepage.html",status=True, username=session['username'])  # Pass the username to the template

@app.route('/update_warning', methods=['POST'])
def update_warning():
    global warning_condition
    warning_condition = "no"

@app.route('/devloper')
def devloper():
    return render_template('Devloper.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/welcome')

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form['forgot-email']
        # Encode the email address and store it in the session
        encoded_email = urllib.parse.quote_plus(email)
        session['reset_email'] = encoded_email
        # Generate a token and store it in the session
        token = generate_token()
        session['reset_token'] = token
        # Construct the password reset link with the token and encoded email
        password_reset_link = url_for('reset_password', token=token, email=encoded_email, _external=True)
        # Send the password reset link via email
        send_password_reset_email(email, password_reset_link)
        flash('Password reset link has been sent to your email.')
        return render_template('login.html',show_reset_popup=True,meth="POST")
    return render_template('forgot.html',show_reset_popup=False)



def generate_token(length=32):
    # Implement your token generation logic here
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(length))
    return token

def send_password_reset_email(email, password_reset_link):
    msg = Message('Password Reset', sender='phishguard000@gmail.com', recipients=[email])
    msg.body = f'Click the following link to reset your password: {password_reset_link}'
    mail.send(msg)

@app.route("/resetPassword", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        new_pwd = request.form.get("newpwd")
        # Retrieve the token and encoded email from the session
        token = session.get('reset_token')
        encoded_email = session.get('reset_email')
        # Decode the email address
        email = urllib.parse.unquote_plus(encoded_email)
        if token and encoded_email:
            # If token and email exist, use them to identify the user and update the password
            query = f"UPDATE phishing_users_db SET pwd = '{new_pwd}' WHERE email = '{email}' "
            row=conn.execute(query)
            conn.commit()
            if row:
                print("updated")
            flash("Your password has been reset successfully.")
            return redirect(url_for("login_validate"))  # Redirect to login page or any other page
        else:
            flash("Invalid or expired password reset token.")
            return redirect(url_for("forgot"))  # Redirect back to forgot page if token is invalid or expired

    return render_template("resetPassword.html")

@app.route('/popup')
def popup():
    return render_template('popup.html',popup_body="sahi",popup_head="sahithcis a good boy")

@app.route("/report",methods=["POST","GET"])
def report():
    if request.method=="POST":
        url=request.form.get("url")
        url_status=request.form.get("url_status")
        print(url)
        if rpu(url):
            print(rpu(url),url)
            return render_template("result.html",report_status=True,url=url,url_status=url_status)
        return render_template("result.html",report_status=False,url=url,url_status=url_status)
@app.route("/phishdb")
def phishdb():
    rows=conn.executeAll("select * from phishingDataBase")
    print("rows",rows)
    return render_template('viewdb.html',rows=rows)


if __name__ == "__main__":
    app.run(port=5002)
