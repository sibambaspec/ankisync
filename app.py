from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('anki.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cards (
                        id INTEGER PRIMARY KEY,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Route to add a new card
@app.route('/add_card', methods=['POST'])
def add_card():
    data = request.json
    question = data.get('question')
    answer = data.get('answer')
    
    if not question or not answer:
        return jsonify({"error": "Question and answer are required"}), 400
    
    conn = sqlite3.connect('anki.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cards (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Card added successfully"}), 201

# Route to get all cards
@app.route('/cards', methods=['GET'])
def get_cards():
    conn = sqlite3.connect('anki.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards")
    cards = cursor.fetchall()
    conn.close()
    
    return jsonify(cards)

# Route to sync with AnkiDroid
@app.route('/sync', methods=['POST'])
def sync():
    # Here you would handle the sync logic with AnkiDroid
    return jsonify({"message": "Sync successful"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
