from flask import Flask, render_template, request, jsonify
from collections import OrderedDict
from database import init_db, create_user, get_all_users, search_users,fetch_users_from_dummy_api, save_users_to_database

app = Flask(__name__)

init_db()

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

import json

# ... (other code)

@app.route('/api/users', methods=['GET'])
def get_users():
    first_name = request.args.get('first_name')

    if not first_name:
        return jsonify({'error': 'Missing mandatory query parameter: first_name'}), 400
    
    users = search_users(first_name)

    if not users:
        # Fetch users from the external API
        api_response = fetch_users_from_dummy_api(first_name)

        if api_response:
            # Save the API response to the database
            save_users_to_database(api_response)
            users = api_response
        else:
            users = []

    field_order = ['id', 'first_name', 'last_name', 'age', 'gender', 'email', 'phone', 'birth_date']

    formatted_users = []
    for user in users:
        formatted_user = OrderedDict()
        for field in field_order:
            formatted_user[field] = user.get(field)
        formatted_users.append(formatted_user)

    response = {'users': formatted_users}
    
    # Manually construct the JSON response with sorted keys
    json_response = json.dumps(response, indent=2, sort_keys=False)

    return json_response


@app.route('/join', methods =['GET', 'POST'])
def join():
    if request.method == 'POST':
        # Extract from data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = int(request.form['age'])
        gender = request.form['gender']
        email = request.form['email']
        phone = request.form['phone']
        birth_date = request.form['birth_date']

        # Call the create_user function to insert data into the database
        create_user(first_name, last_name, age, gender, email, phone, birth_date)

        return render_template("index.html")
    else:
        return render_template('join.html')
    
@app.route('/participants')
def participants():
    data = get_all_users()
    return render_template("participants.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)