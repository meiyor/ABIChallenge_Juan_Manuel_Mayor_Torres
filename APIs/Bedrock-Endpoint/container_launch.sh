#!/bin/bash

# turn on bash's job control
set -m

service postgresql restart
source export_credentials.sh
python app.py
