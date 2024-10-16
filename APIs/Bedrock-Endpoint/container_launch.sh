#!/bin/bash

# turn on bash's job control
set -m

service postgresql restart
sh export_credentials.sh
python app.py
