FROM python:3.10-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/lib/chromium/:$PATH"
ENV CHROME_BIN="/usr/bin/chromium"

# 프로젝트 복사
WORKDIR /app
COPY . /app

# 의존성 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
