FROM python:3.12.3

COPY . /app
COPY ./requirements.txt /app

WORKDIR /app

RUN apt update && apt --assume-yes install postgresql-16 gcc python3-dev musl-dev

# COPY ./mounts/postgres/ /var/lib/postgresql/data/

RUN pip3 install -r requirements.txt

RUN sed -i 's/peer/md5/g' /etc/postgresql/16/main/pg_hba.conf

RUN service postgresql restart

CMD ./container_launch.sh
