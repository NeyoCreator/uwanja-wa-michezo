from flask import Flask, render_template, request, session, redirect, url_for
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to an actual secret key for production use

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
def index():
    return render_template('index.html')

@app.route('/consumption')
def consumption():
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
