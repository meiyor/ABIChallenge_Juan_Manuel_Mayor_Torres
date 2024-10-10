FROM python:3.12.3

COPY . /app
COPY ./requirements.txt /app

WORKDIR /app

RUN apt update && apt --assume-yes install postgresql gcc python3-dev musl-dev

COPY /var/lib/postgresql/16/ /var/lib/postgresql/data/

RUN pip3 install -r requirements.txt

CMD python app.py

