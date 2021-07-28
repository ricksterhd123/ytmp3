FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD [ "flask", "run" ]
EXPOSE 5000
