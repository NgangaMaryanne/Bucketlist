#!/bin/bash
export WORKSPACE='pwd'
export SECRET_KEY='thissecretkey'
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
nosetests