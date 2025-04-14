FROM python:3.10-slim

# ✅ 크롬 & 크롬드라이버 설치 (경로 지정은 바로 여기!)
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# ✅ 환경변수 추가 - PATH에 chrome/chromedriver 경로 포함
ENV PATH="/usr/lib/chromium/:/usr/bin/:${PATH}"
ENV CHROME_BIN="/usr/bin/chromium"

# ✅ 프로젝트 복사
WORKDIR /app
COPY . /app

# ✅ 의존성 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ✅ 포트 열기
EXPOSE 10000

# ✅ 실행 명령
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
