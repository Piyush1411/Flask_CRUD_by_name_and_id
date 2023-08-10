from flask import Flask, render_template, request, jsonify
from database import init_db, create_user, get_all_users

app = Flask(__name__)

init_db()

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

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