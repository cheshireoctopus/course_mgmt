#GitHub Course Management

A simple application for teaching a class using GitHub.

Set up for your own course:

1. `npm install`
2. Create a `.env` file at project root containing:
  - `githubUsername='YOURGITHUBUSERNAME'`
  - `PORT=1337`
3. Start node server: `npm run dev` or `nodemon`
4. Start webpack bundling/watching `npm run bundle`

# Python setup
Set up for your own course (Skip steps 1 and 2 if you don't wish to run this in a virtualenv)

1. virtualenv
2. source venv/bin/activate
3. python setup.py
4. nosetests course_mgmt/system_tests.py
5. python run.py