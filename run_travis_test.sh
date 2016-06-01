#!/usr/bin/env bash
python run.py > /dev/null &
nosetests --with-coverage
curl https://intake.opbeat.com/api/v1/organizations/f9912cfead99443481626ec8571446dc/apps/bf410a53b2/releases/ -H "Authorization: Bearer f76c0fc391048436e4bfc5dd8d7df07835adfe25" -d rev=`git log -n 1 --pretty=format:%H` -d branch=`git rev-parse --abbrev-ref HEAD` -d status=completed