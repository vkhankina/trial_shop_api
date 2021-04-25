#!/bin/bash
cd /usr/src/app
# running migrations
python3 manage.py migrate
# starting http server
uwsgi --ini /usr/src/app/uwsgi.ini