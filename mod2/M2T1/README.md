# M2T1 - Webapp #1

## Goals:
- to learn basic Flask programming
- to be able to repeat a server config
- maybe have fun

## Lessons Learned:
- Typing --app before --debug doesn't work
- ctrl-shift-p, python: interpreter location, .venv/bin/python3

## Instructions:

Initial tutorial: https://blog.pythonanywhere.come/121/

Install library:
- First setup:
    - pip install virtualenv
    - py -m venv $PATH (path to venv)
    - source venv/bin/activate
- Start installing requirements:
    - pip install flask
    - pip freeze > requirements.txt

Use pip install -r requirements.txt

to start:
- flask --debug --app hello run