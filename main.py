from flask import Flask, render_template, request, flash, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import sqlite3
import json
import datetime
import sqlite3
import json
import os
import pdb
from dotenv import load_dotenv

load_dotenv()

# Replace these with your actual values
instance_url = os.getenv("MASTODON_INSTANCE_URL")
access_token = os.getenv("MASTODON_ACCESS_TOKEN")
account_id = os.getenv("AUTHENTICATED_USER_ID")

# Set up headers
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Write you code below

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
auth = HTTPBasicAuth()

users = {
    os.getenv("USERNAME"): os.getenv("PASSWORD"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    
@app.route('/')
@auth.login_required
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect('thoughts.db')
    cursor = conn.cursor()

    # Fetch titles from the database
    cursor.execute('SELECT id, created_at, title, content FROM thoughts WHERE is_deleted = 0') # Adjust the query accordingly
    notes = cursor.fetchall()
    # pdb.set_trace()

    # Close the database connection
    conn.close()

    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
@auth.login_required
def add_note():
    if request.method == 'POST':
        created_at = request.form['created_at']
        title = request.form['title']
        content = request.form['content']
        categories = request.form['tags']
        
        conn = sqlite3.connect('thoughts.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO thoughts (created_at, title, content, categories) VALUES (?, ?, ?, ?)', 
                       (created_at, title, content, categories))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_note.html')

@app.route('/delete_note/<int:id>')
@auth.login_required
def delete_note(id):
    conn = sqlite3.connect('thoughts.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE thoughts SET is_deleted = 1 WHERE id = ?', (id,))
    conn.commit()
    # pdb.set_trace()

    conn.close()
    
    return redirect(url_for('index'))

@app.route('/categories')
@auth.login_required
def categories():
    # Connect to the SQLite database
    conn = sqlite3.connect('thoughts.db')
    cursor = conn.cursor()

    # Fetch titles from the database
    cursor.execute('SELECT categories FROM thoughts WHERE is_deleted = 0') # Adjust the query accordingly
    categories = cursor.fetchall()
    # pdb.set_trace()

    # Close the database connection
    conn.close()

    return render_template('categories.html', categories=categories)

if __name__ == "__main__":
    app.run(debug=True)