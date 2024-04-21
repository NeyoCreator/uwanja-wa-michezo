from flask import Flask, render_template, request, session, redirect, url_for
from firebase_admin import credentials, firestore
from firebase_admin import auth as auth_user
import firebase_admin
from flask_mail import Mail, Message
import pyrebase


# App initialisation
app = Flask(__name__)
app.secret_key = 'secret_data'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'  # Change this to your SMTP server
app.config['MAIL_PORT'] = 587  # Change this to your SMTP port
app.config['MAIL_USE_TLS'] = True  # Change this according to your SMTP configuration
app.config['MAIL_USERNAME'] = 'neo.andersonseb@gmail.com'  # Change this to your email username
app.config['MAIL_PASSWORD'] = 'bchq cmov kqtm ixcx'  # Change this to your email password
mail = Mail(app)


# Database intergration
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Authentication
config = {
    "apiKey": "AIzaSyBz7_W4p3rmppxhCXNHZzj3yC7MQzPeMSY",
    "authDomain": "mwanga-445c6.firebaseapp.com",
    "databaseURL": "https://mwanga-445c6-default-rtdb.firebaseio.com",
    "projectId": "mwanga-445c6",
    "storageBucket": "mwanga-445c6.appspot.com",
    "messagingSenderId": "252500288391",
    "appId": "1:252500288391:web:18b843348ecafc9bf5a922"
  }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print("loading")
        email = request.form.get('email')
        password = request.form.get("password")
        try:
            # Assuming auth is already defined somewhere in your code
            user = auth.sign_in_with_email_and_password(email, password)
            print("Successfully signed in.")
            session['user'] = email
            return render_template("delivery.html")
        except:
            return "Failed to login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/index', methods = ['GET','POST'])
def index():
    if ('user' in session):
        return render_template("delivery.html")
    if request.method == 'POST':
        name =  request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        location = request.form.get('location')
        session['user'] = email
        user = auth.create_user_with_email_and_password(email, password)
        print("#Successfully Registred user",user)
        session['user_data'] = {'name': name, 'email': email, 'location': location}
        return redirect(url_for('consumption'))
    return render_template('index.html')

@app.route('/register', methods = ['GET','POST'])
def register():
    print("Info: Redirecting to register page")
    return render_template('register.html')

@app.route('/register_user', methods = ['GET','POST'])
def register_user():
    print("Info: Registering user")
    return render_template('pass.html')

@app.route('/consumption', methods = ['GET','POST'])
def consumption():
    if request.method == 'POST':
        # package = request.form.get('email')
        selected_package = request.form.get('exampleRadios')
        print("The selected package is ",selected_package)
        session['selected_package'] = selected_package
        user_information = [session['user_data'],session['selected_package']]

        # session['consumption_data'] = consumption_data
        db.collection(session['user_data']['email']).document("data").set(session)
        print("INFO : Database updated ")

        return redirect(url_for('delivery'))
    
    return render_template('consumption.html')

@app.route('/device', methods=['GET', 'POST'])
def device():
    if request.method == 'POST':
        component_list = request.form.get('componentList')

        device_data = {
            'component_list': component_list.split(',')
        }
        session['device_data'] = device_data
        print("session",session)

        return redirect(url_for('delivery'))


    return render_template('device.html')



@app.route('/delivery', methods=['GET','POST'])
def delivery():
    # Extract data from the session cookie
        user_data = session.get('user_data', {})
        # consumption_data = session.get('consumption_data', {})
        # device_data = session.get('device_data', {})

        # Format the data for email
        email_body = f"Hello {user_data.get('name', '')},\n\n"
        email_body += "New order made!\n\n"
        email_body += "Here are the details:\n"
        email_body += f"Name: {user_data.get('name', '')}\n"
        email_body += f"Email: {user_data.get('email', '')}\n"
        email_body += f"Location: {user_data.get('location', '')}\n\n"
        email_body += f"Selected package: {session['selected_package']}\n\n"
        email_body += f"Your delivery is being processed , our agents will get back to you regarding additional information. Thank you for chossing Mwanga.\n\n"

        link = auth_user.generate_email_verification_link('neos25722@gmail.com', action_code_settings=None)
        
        # Send email
        msg = Message('Delivery Information', sender='noreply@app.com', recipients=['neo.andersonseb@gmail.com',session['user_data']['email']])
        msg.body = link
        mail.send(msg)
        
        return render_template('delivery.html')


@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(debug=True)
