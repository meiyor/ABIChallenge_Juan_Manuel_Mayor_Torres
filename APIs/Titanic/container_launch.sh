#!/bin/bash

# turn on bash's job control
set -m

service postgresql restart
python app.py
