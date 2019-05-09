FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk update && apk add curl
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 3000

COPY . .

HEALTHCHECK  --interval=5s --start-period=15s --timeout=3s CMD curl -f http://localhost:3000/blabs || exit 1

CMD ["uwsgi", "--http", "127.0.0.1:8000", "--wsgi-file", "API.py", "--callable", "app_dispatch"]
