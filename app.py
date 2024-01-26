from flask import Flask, render_template, request, session, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_data'  # Change this to an actual secret key for production use

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
        print('consumtion_data',consumption_data)
        # save_to_json(consumption_data)

        # Redirect to the next page or perform other actions
        return redirect(url_for('device'))
    
    return render_template('consumption.html')

@app.route('/device')
def device():
    return render_template('device.html')

@app.route('/installer')
def installer():
    return render_template('installer.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')



if __name__ == '__main__':
    app.run(debug=True)
