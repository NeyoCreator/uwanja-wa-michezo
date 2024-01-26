from flask import Flask, render_template, request, session, redirect, url_for
import json
import os
from google.cloud import firestore
from firebase_admin import credentials, firestore

import firebase_admin

app = Flask(__name__)
app.secret_key = 'secret_data'  # Change this to an actual secret key for production use

# database intergration
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

# Database
db = firestore.client()

def save_to_json(data):
    file_path = 'data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
        existing_data.append(data)
        with open(file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)
    else:
        with open(file_path, 'w') as file:
            json.dump([data], file, indent=4)

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
        # redirect(url_for('consumption'))
        return redirect(url_for('consumption'))


    return render_template('index.html')

@app.route('/consumption', methods = ['GET','POST'])
def consumption():
    if request.method == 'POST':
        # Retrieve data from the form
        selected_appliances = request.form.get('selectedAppliances')
        total_wattage = request.form.get('totalWatt')

        # Do something with the data, for example, save it to a JSON file
        consumption_data = {
            'selected_appliances': selected_appliances.split(','),
            'total_wattage': total_wattage
        }
        session['consumption_data'] = consumption_data
        print(session)
        # save_to_json(consumption_data)

        # Redirect to the next page or perform other actions
        return redirect(url_for('device'))
    
    return render_template('consumption.html')

@app.route('/device', methods=['GET', 'POST'])
def device():
    if request.method == 'POST':
        # Retrieve data from the form
        component_list = request.form.get('componentList')

        # Do something with the data, for example, save it to a JSON file
        device_data = {
            'component_list': component_list.split(',')
        }
        session['device_data'] = device_data
        print("session",session)
        # save_to_json(device_data)

        # Redirect to the next page or perform other actions
        return redirect(url_for('installer'))


    return render_template('device.html')

@app.route('/installer',methods = ['GET','POST'])
def installer():
    if request.method == 'POST':
        # Retrieve data from the form
        installer_name = request.form.get('installer_name')
        installer_rating = request.form.get('installer_rating')

        # Do something with the data, for example, save it to a JSON file
        installer_data = {
            'installer_name': installer_name,
            'installer_rating': installer_rating
        }
        session['installer_data'] = installer_data
        # print("session", session)

        db.collection(session['user_data']['email']).document("data").set(session)
        print(session['user_data']['email'])
        

        # Redirect to the next page or perform other actions
        return redirect(url_for('delivery'))
    return render_template('installer.html')

@app.route('/delivery', methods=['GET','POST'])
def delivery():
    return render_template('delivery.html')



if __name__ == '__main__':
    app.run(debug=True)
