FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/lib/chromium/:$PATH"
ENV CHROME_BIN="/usr/bin/chromium"

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 10000   # <-- 이 줄 추가!!

CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]

ENV PATH="/usr/bin/chromedriver:${PATH}"
