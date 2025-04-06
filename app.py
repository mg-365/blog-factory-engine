from supabase import create_client, Client
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SUPABASE_URL = "https://vyzpmuvueoqibapjmxrq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ5enBtdXZ1ZW9xaWJhcGpteHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5NTEyODgsImV4cCI6MjA1OTUyNzI4OH0.OjVZ_8Qdc3d7a9IIdUvEZ575RZbN2zykfHSsTVGBbM4"
TABLE_NAME = "blog-factory-realdb"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/add", methods=["POST"])
def add_blog():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    try:
        result = supabase.table(TABLE_NAME).insert(data).execute()
        return jsonify({"message": "Blog added!", "data": result.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/data", methods=["GET"])
def get_blogs():
    try:
        result = supabase.table(TABLE_NAME).select("*").order("id", desc=True).execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 로컬 개발용 (배포에는 영향 없음)
if __name__ == "__main__":
    app.run(debug=True)
