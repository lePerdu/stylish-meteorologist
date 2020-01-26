#!/bin/bash

dir=$(dirname $0)
port=${PORT:=5000}

source $dir/venv/bin/activate
source .env

gunicorn --bind=127.0.0.1:$port camera.server:app
