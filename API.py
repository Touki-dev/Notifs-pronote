from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid
from Crawler.Crawling import crawl

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/crawl', methods=['GET'])
def get_crawling():
    user_id = request.args.get('user_id')
    if user_id is None:
        return jsonify({"error": "Missing user_id parameter"}), 400

    result = crawl(user_id)
    print(jsonify(result))
    return jsonify(result)

@app.route('/newUser', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'pseudo' not in data or 'id_ent' not in data or 'password' not in data:
        return jsonify({"error": "Missing parameters in JSON body"}), 400

    pseudo, id_ent, password = data['pseudo'], data['id_ent'], data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Users (id, pseudo, id_ent, password) VALUES (?, ?, ?, ?)', (str(uuid.uuid4()), pseudo, id_ent, password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User created successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)