from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

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
    
    parts = user_input.split(' ', 1)
    command = parts[0].lower()
    response = ""

    if command in ["log", "remember"]:
        if len(parts) < 2:
            return jsonify({"error": "Please provide the item and location in the format 'log item at location'"}), 400
        
        item_parts = parts[1].rsplit(' at ', 1)
        if len(item_parts) < 2:
            return jsonify({"error": "Please provide the item and location in the format 'log item at location'"}), 400
        
        item = item_parts[0].strip()
        location = item_parts[1].strip()
        
        data = load_data()
        data[item] = location
        save_data(data)
        
        response = f"{item} logged at {location}"
    
    elif command in ["find", "where"]:
        if len(parts) < 2:
            return jsonify({"error": "Please provide the item to find in the format 'find item'"}), 400
        
        item = parts[1].strip()
        data = load_data()
        location = data.get(item, "Item not found")
        
        response = f"{item} is at {location}"
    
    else:
        return jsonify({"error": "Unrecognized command. Use 'log item at location' or 'find item'"}), 400

    return jsonify({"message": response}), 200

if __name__ == '__main__':
    app.run(debug=True)
