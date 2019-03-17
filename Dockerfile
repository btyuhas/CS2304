FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 3000

COPY . .

CMD [ "python", "./API.py" ]