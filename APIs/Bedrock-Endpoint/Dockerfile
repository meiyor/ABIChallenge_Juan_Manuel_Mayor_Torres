FROM python:3.12.3

COPY . /app
COPY ./requirements.txt /app

WORKDIR /app

RUN apt update && apt --assume-yes install postgresql postgresql-* gcc python3-dev musl-dev sudo nano

RUN pip3 install -r requirements.txt

# don't run this from the container side
RUN sed -i 's/peer/md5/g' /etc/postgresql/15/main/pg_hba.conf

RUN sed -i 's/localhost/*/g' /etc/postgresql/15/main/postgresql.conf
RUN sed -i 's/#listen_addresses/listen_addresses/g' /etc/postgresql/15/main/postgresql.conf
RUN sed -i 's/md5/trust/g' /etc/postgresql/15/main/pg_hba.conf
RUN source export_credentials.sh

CMD ./container_launch.sh
