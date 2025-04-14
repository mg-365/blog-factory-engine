FROM python:3.10-slim

# 🛠 필수 패키지 설치 + 심볼릭 링크 생성까지
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/lib/chromium/chromium /usr/bin/chrome  # 👈 chrome 실행 파일을 PATH에 등록

# 환경 변수 설정
ENV PATH="/usr/lib/chromium/:$PATH"
ENV CHROME_BIN="/usr/bin/chrome"  # 👈 binary_location에 명시할 경로

# 작업 디렉토리 설정
WORKDIR /app
COPY . /app

# pip 최신화 및 requirements 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Render에서 포트 노출 명시
EXPOSE 10000  # 👈 이 줄 꼭 있어야 서비스가 감지됨

# 앱 실행 명령어
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
