FROM python:3.12.3

COPY . /app
COPY ./requirements.txt /app

WORKDIR /app

RUN apt update && apt --assume-yes install postgresql postgresql-* gcc python3-dev musl-dev sudo nano

# COPY ./mounts/postgres/ /var/lib/postgresql/data/

RUN pip3 install -r requirements.txt

# don't run this from the container side
RUN sed -i 's/peer/md5/g' /etc/postgresql/15/main/pg_hba.conf

RUN sed -i 's/localhost/*/g' /etc/postgresql/15/main/postgresql.conf
RUN sed -i 's/#listen_addresses/listen_addresses/g' /etc/postgresql/15/main/postgresql.conf
RUN sed -i 's/md5/trust/g' /etc/postgresql/15/main/pg_hba.conf
# RUN echo "host  all  all  0.0.0.0/0   md5" >> /etc/postgresql/15/main/pg_hba.conf

# RUN service postgresql restart

CMD ./container_launch.sh
