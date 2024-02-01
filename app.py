from flask import Flask, render_template, request, session, redirect, url_for
from firebase_admin import credentials, firestore
import firebase_admin


# App initialisation
app = Flask(__name__)
app.secret_key = 'secret_data'

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
            'selected_appliances': selected_appliances.split(','),
            'total_wattage': total_wattage
        }
        session['consumption_data'] = consumption_data
        print(session)

        return redirect(url_for('device'))
    
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

        return redirect(url_for('installer'))


    return render_template('device.html')

@app.route('/installer',methods = ['GET','POST'])
def installer():
    if request.method == 'POST':
        installer_name = request.form.get('installer_name')
        installer_rating = request.form.get('installer_rating')

        installer_data = {
            'installer_name': installer_name,
            'installer_rating': installer_rating
        }
        session['installer_data'] = installer_data

        db.collection(session['user_data']['email']).document("data").set(session)
        print(session['user_data']['email'])
        

        return redirect(url_for('delivery'))
    return render_template('installer.html')

@app.route('/delivery', methods=['GET','POST'])
def delivery():
    return render_template('delivery.html')



if __name__ == '__main__':
    app.run(debug=True)
