[![Stories in Ready](https://badge.waffle.io/cheshireoctopus/course_mgmt.png?label=ready&title=Ready)](https://waffle.io/cheshireoctopus/course_mgmt)
[![Build Status](https://travis-ci.org/cheshireoctopus/course_mgmt.png)](https://travis-ci.org/cheshireoctopus/course_mgmt)
[![Coverage Status](https://coveralls.io/repos/github/cheshireoctopus/course_mgmt/badge.png?branch=master)](https://coveralls.io/github/cheshireoctopus/course_mgmt?branch=master)
[![Code Health](https://landscape.io/github/cheshireoctopus/course_mgmt/master/landscape.svg?style=flat)](https://landscape.io/github/cheshireoctopus/course_mgmt/master)

#GitHub Course Management

A simple application for teaching a class using GitHub.

Set up for your own course:

1. `pip install -r requirements.txt` at root (use of [virutal environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/) is recommended):

2. Create a `.env` file at `course_mgmt/front_end/` root containing:
  - `githubUsername='YOURGITHUBUSERNAME'`

To boot the webserver, at project root run `python run.py`. Project is hosted on `localhost:5000`

To boot webpack for bundling/watching of frontend assets, run `npm run bundle` at `course_mgmt/front_end/` root. This will bundle JavaScript and CSS assets into `course_mgmt/front_end/public/js/build/bundle.js`.