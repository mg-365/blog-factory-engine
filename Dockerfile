FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
 && ln -s /usr/bin/chromium /usr/bin/google-chrome \
 && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/bin/:${PATH}"
ENV CHROME_BIN="/usr/bin/google-chrome"

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 10000

CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
