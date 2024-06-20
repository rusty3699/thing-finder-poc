from flask import Flask, request, jsonify, render_template, session
import json
import os
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interact', methods=['POST'])
def interact():
    user_input = request.form.get('user_input')
    
    if not user_input:
        return jsonify({"error": "Input is required"}), 400

    user_input = user_input.lower().strip()
    response = ""

    # Check if there is an ongoing session for logging an item
    if 'pending_item' in session:
        item = session.pop('pending_item')
        location = user_input.strip()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data = load_data()
        data[item] = {"location": location, "timestamp": timestamp}
        save_data(data)
        
        response = f"{item} logged at {location} on {timestamp}"
        return jsonify({"message": response}), 200

    # Check if there is an ongoing session for confirming item location
    if 'confirm_item' in session:
        item = session.pop('confirm_item')
        if user_input in ['yes', 'y']:
            # User confirmed the item is still there, update the timestamp
            data = load_data()
            data[item]['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_data(data)
            response = f"{item} location confirmed. Timestamp updated."
        elif user_input in ['no', 'n']:
            # User indicated the item is no longer there, prompt for new location
            session['pending_item'] = item
            response = f"Where is the {item} now?"
        else:
            # Invalid input, prompt again
            session['confirm_item'] = item
            response = "Please answer with 'yes' or 'no'. Is the item still there?"
        return jsonify({"message": response}), 200

    # Check for logging commands
    log_match = re.match(r'^(log|remember) (.+) at (.+)$', user_input)
    if log_match:
        item = log_match.group(2).strip()
        location = log_match.group(3).strip()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        data = load_data()
        data[item] = {"location": location, "timestamp": timestamp}
        save_data(data)
        
        response = f"{item} logged at {location} on {timestamp}"
        return jsonify({"message": response}), 200

    # Check for find commands
    find_match = re.match(r'^(find|where are my|where is my) (.+)$', user_input)
    if find_match:
        item = find_match.group(2).strip()
        data = load_data()
        item_data = data.get(item, None)
        
        if item_data:
            location = item_data['location']
            timestamp = item_data['timestamp']
            response = f"{item} is at {location}. Last information saved on {timestamp}. Is the item still there? (yes/no)"
            session['confirm_item'] = item
        else:
            response = "Item not found"
        
        return jsonify({"message": response}), 200

    # For any input, first check if the item is in the database
    data = load_data()
    item_data = data.get(user_input, None)
    if item_data:
        location = item_data['location']
        timestamp = item_data['timestamp']
        response = f"{user_input} is at {location}. Last information saved on {timestamp}. Is the item still there? (yes/no)"
        session['confirm_item'] = user_input
        return jsonify({"message": response}), 200

    # If the item is not in the database, ask for location
    session['pending_item'] = user_input
    response = f"Where do you want to keep {user_input}?"
    return jsonify({"message": response}), 200

if __name__ == '__main__':
    app.run(debug=True)
