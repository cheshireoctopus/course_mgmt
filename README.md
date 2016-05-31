#GitHub Course Management

A simple application for teaching a class using GitHub.

Set up for your own course:

1. `pip install` the following at root (use of [virutal environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/) is recommended):
  - `flask`
  - `flask_sqlalchemy`
  - `pyjade`
2. Create a `.env` file at `course_mgmt/front_end/` root containing:
  - `githubUsername='YOURGITHUBUSERNAME'`
  - `PORT=1337`

To boot webserver, at project root run `python run.py`. Project is hosted on `localhost:5000`

To boot webpack for bundling/watching of frontend assets, run `npm run bundle` at `course_mgmt/front_end/` root. This will bundle JavaScript and CSS assets into `course_mgmt/front_end/public/js/build/bundle.js`.

# Python setup
Set up for your own course (Skip steps 1 and 2 if you don't wish to run this in a virtualenv)

1. virtualenv
2. source venv/bin/activate
3. python setup.py
4. nosetests course_mgmt/system_tests.py
5. python run.py
