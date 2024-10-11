FROM python:3.12.3

COPY . /app
COPY ./requirements.txt /app

WORKDIR /app

RUN apt update && apt --assume-yes install postgresql gcc python3-dev musl-dev

# COPY ./mounts/postgres/ /var/lib/postgresql/data/

RUN pip3 install -r requirements.txt

# don't run this from the container side
#RUN sed -i 's/peer/md5/g' /etc/postgresql/15/main/pg_hba.conf

RUN sed -i 's/localhost/*/g' /etc/postgresql/15/main/postgresql.conf

RUN service postgresql stop
RUN service postgresql start

CMD ./container_launch.sh
