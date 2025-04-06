from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

DATA_FILE = 'data.json'

@app.route('/')
def home():
    return '🚀 Blog Dashboard API is running!'

@app.route('/add', methods=['POST'])
def add_blog():
    new_blog = request.get_json()
    if not new_blog:
        return jsonify({'error': 'No data received'}), 400

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            blogs = json.load(f)
    except FileNotFoundError:
        blogs = []

    blogs.append(new_blog)

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(blogs, f, ensure_ascii=False, indent=2)

    return jsonify({'message': 'Blog added!', 'total': len(blogs)}), 200
