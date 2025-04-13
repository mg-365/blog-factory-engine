from supabase import create_client, Client
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://mg-365.github.io"}})


SUPABASE_URL = "https://vyzpmuvueoqibapjmxrq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ5enBtdXZ1ZW9xaWJhcGpteHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5NTEyODgsImV4cCI6MjA1OTUyNzI4OH0.OjVZ_8Qdc3d7a9IIdUvEZ575RZbN2zykfHSsTVGBbM4"
TABLE_NAME = "blog-factory-realdb"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# 저품질 체크 파트1 (이것들도 여기서 필요해서 추가 선언함 from bs4 import BeautifulSoup import requests)
def check_daum_status(blog_url):
    search_url = f"https://search.daum.net/search?w=site&q={blog_url}"
    
    try:
        response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ 글 갯수 파악
        posts = soup.select("a.f_link_b")
        글수 = len(posts)

        # ✅ 사이트 노출 확인
        site_link = soup.select_one("a.f_url")
        사이트노출 = False

        if site_link:
            href = site_link.get("href", "")
            normalized_href = href.replace("https://", "").replace("http://", "").rstrip("/")
            normalized_blog = blog_url.replace("https://", "").replace("http://", "").rstrip("/")

            # ✅ 비교 로그 출력
            print(f"[사이트 비교] href: {normalized_href} / blog: {normalized_blog}")
            사이트노출 = normalized_blog in normalized_href
            print(f"[결과] 사이트 노출 여부: {사이트노출}")
        else:
            print("[경고] f_url 요소를 찾을 수 없습니다.")



        return {
            "글수진단": 글수,
            "사이트노출": 사이트노출,
            "검색링크": search_url
        }
    except Exception as e:
        print(f"[진단 오류] {blog_url} → {e}")
        return {
            "글수진단": 0,
            "사이트노출": False,
            "검색링크": search_url
        }

# 저품질 체크 파트2
@app.route("/diagnose")
def diagnose_all_blogs():
    print("💬 /diagnose 엔드포인트 실행됨")  # 이 줄 추가
    result = supabase.table(TABLE_NAME).select("*").execute()
    blogs = result.data

    for blog in blogs:
        url = blog.get("name")
        print(f"🔎 블로그 대상: {url}")  # 이 줄 추가
        if not url:
            continue

        
        print(f"[진단 대상] {url}")
        status = check_daum_status(url)
        print(f"[진단 결과] {status}")
        

        try:
            supabase.table(TABLE_NAME).update({
                "글수진단": status["글수진단"],
                "사이트노출": status["사이트노출"],
                "검색링크": status["검색링크"]
            }).eq("id", blog["id"]).execute()
            print(f"[업데이트 완료] ID={blog['id']}")
        except Exception as e:
            print(f"[업데이트 실패] ID={blog.get('id')} → {e}")

    return jsonify(
        {"message": f"{len(blogs)}개 블로그 진단 완료"},
        200,
        {'Content-Type': 'application/json; charset=utf-8'}
    )







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

@app.route('/delete', methods=['POST'])
def delete_blog():
    try:
        data = request.get_json()
        blog_id = data.get("id")
        if not blog_id:
            return jsonify({"error": "No blog id provided"}), 400

        result = supabase.table(TABLE_NAME).delete().eq("id", blog_id).execute()
        return jsonify({"message": "Blog deleted", "result": result.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 로컬 개발용 (배포에는 영향 없음)
if __name__ == "__main__":
    app.run(debug=True)

# 서버 슬립 방지 10분마다 호출
@app.route("/ping")
def ping():
    return "pong", 200
