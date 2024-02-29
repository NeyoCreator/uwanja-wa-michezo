from flask import Flask, render_template, request, session, redirect, url_for
from firebase_admin import credentials, firestore
import firebase_admin
from flask_mail import Mail, Message


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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods = ['GET','POST'])
def index():
    print("Hello")
    if request.method == 'POST':
        name =  request.form.get('name')
        email = request.form.get('email')
        location = request.form.get('location')

        session['user_data'] = {'name': name, 'email': email, 'location': location}
        print(session)
        return redirect(url_for('consumption'))


    return render_template('index.html')

@app.route('/consumption', methods = ['GET','POST'])
def consumption():
    if request.method == 'POST':
        selected_appliances = request.form.get('selectedAppliances')
        total_wattage = request.form.get('totalWatt')

        consumption_data = {
            # 'selected_appliances': selected_appliances.split(','),
            'selected_appliances': "",

            'total_wattage': total_wattage
        }
        session['consumption_data'] = consumption_data
        print(session)

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
        # if request.method == 'POST':
            # Send email
# Extract data from the session cookie
        user_data = session.get('user_data', {})
        consumption_data = session.get('consumption_data', {})
        device_data = session.get('device_data', {})

        # Format the data for email
        email_body = f"Hello {user_data.get('name', '')},\n\n"
        email_body += "New order made!\n\n"
        email_body += "Here are the details:\n"
        email_body += f"Name: {user_data.get('name', '')}\n"
        email_body += f"Email: {user_data.get('email', '')}\n"
        email_body += f"Location: {user_data.get('location', '')}\n\n"
        email_body += "Consumption Information:\n"
        email_body += f"Selected Appliances: {', '.join(consumption_data.get('selected_appliances', []))}\n"
        email_body += f"Total Wattage: {consumption_data.get('total_wattage', '')}\n\n"
        email_body += "Device Information:\n"
        email_body += f"Component List: {', '.join(device_data.get('component_list', []))}\n"

        # Send email
        msg = Message('Delivery Information', sender='noreply@app.com', recipients=['neo.andersonseb@gmail.com'])
        msg.body = email_body
        mail.send(msg)
        
        return render_template('delivery.html')



if __name__ == '__main__':
    app.run(debug=True)
