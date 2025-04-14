FROM python:3.10-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgcc1 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# 환경변수 지정 (필수)
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$CHROME_BIN:$PATH

# 프로젝트 복사
WORKDIR /app
COPY . /app

# 의존성 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 포트 오픈
EXPOSE 10000

# 실행
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
