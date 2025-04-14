from supabase import create_client, Client
from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import chromedriver_autoinstaller  # 👈 이미 설치되어 있음
import tempfile


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://mg-365.github.io"}})


SUPABASE_URL = "https://vyzpmuvueoqibapjmxrq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ5enBtdXZ1ZW9xaWJhcGpteHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM5NTEyODgsImV4cCI6MjA1OTUyNzI4OH0.OjVZ_8Qdc3d7a9IIdUvEZ575RZbN2zykfHSsTVGBbM4"
TABLE_NAME = "blog-factory-realdb"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)






# 저품질 체크용, 크롬드라이버 설정 함수
def get_headless_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    
    # ✅ 이 라인을 추가해줘!
    import tempfile
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f'--user-data-dir={user_data_dir}')

    driver = webdriver.Chrome(options=options)
    return driver



def check_daum_status(blog_url):
    try:
        print(f"🧪 check_daum_status 실행 시작: {blog_url}")  # 추가
        driver = get_headless_driver()
        search_url = f"https://search.daum.net/search?w=site&q={blog_url}"
        driver.get(search_url)
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        posts = soup.select("a.f_link_b")
        글수 = len(posts)

        site_section = soup.select_one(".f_url")
        사이트노출 = False
        if site_section:
            href = site_section.get("href", "")
            비교값 = blog_url.replace("https://", "").rstrip("/")
            사이트노출 = 비교값 in href
        else:
            # a 태그 기반으로 대체 시도
            anchors = soup.find_all("a", href=True)
            for a in anchors:
                if blog_url.replace("https://", "").rstrip("/") in a["href"]:
                    사이트노출 = True
                    break

        driver.quit()
        return {
            "글수진단": 글수,
            "사이트노출": 사이트노출,
            "검색링크": search_url
        }

    except Exception as e:
        print(f"❌ [진단 에러 발생]: {e}")  # 반드시 이 줄 넣기
        driver.quit()  # finally가 아니므로 여기서 꼭 종료시켜야 함
        return None





# 저품질 체크 파트2
@app.route("/diagnose")
def diagnose_all_blogs():
    print("📌 diagnose 진입함")
    print("💬 /diagnose 엔드포인트 실행됨")

    result = supabase.table(TABLE_NAME).select("*").execute()
    blogs = result.data
    print(f"📌 블로그 {len(blogs)}개 로딩됨")

    for blog in blogs:
        url = blog.get("name")
        print(f"🔎 블로그 대상: {url}")
        if not url:
            continue

        print(f"[진단 대상] {url}")
        status = check_daum_status(url)
        print(f"[진단 결과] {status}")

        # ✅ 에러 방지: status가 None이면 건너뜀
        if not status or not isinstance(status, dict):
            print(f"[❌ 오류] status가 None이거나 dict 아님 → {status}")
            continue

        try:
            supabase.table(TABLE_NAME).update({
                "글수진단": status.get("글수진단", 0),
                "사이트노출": status.get("사이트노출", False),
                "검색링크": status.get("검색링크", "")
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
    app.run(host="0.0.0.0", port=10000)


# 서버 슬립 방지 10분마다 호출
@app.route("/ping")
def ping():
    return "pong", 200
