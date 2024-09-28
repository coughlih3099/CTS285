# MadMath

This project is a recreation of the 1977 classic Texas Instruments Dataman
This project aims to deliver functionality similar to that of the Dataman but updated
to the modern day and presented as a web app.

# Requirements
MadMath is required to implement the Answer Checker, Memory Bank, and Electro Flash
functions from the original Dataman.

## Math Master
- Default mode
- Requires both the problem and answer to be entered, e.g. 1 + 1 = 2
- Will signal whether or not the answer is right or wrong, and will allow two wrong answers before before displaying the correct answer
- Only problems with one or two digit numbers and answers with up to three digits are allowed
- Negative numbers are not allowed so subtraction that results in a negative number is rejected
- If subtraction would occur that would result in a negative, i.e. 7 - 8,
    the second operand will need to be updated to a number that won't produce a negative or the input needs to be reset
- Answers to division problems are displayed with a remainder, the whole part needs to be input and the remainder will be added
- Score is kept, after ten problems, the number of correct answers and amount of questions are displayed

# How to run
- create a python virtual environment:
    - python -m venv env (or .venv on linux)
- source env/bin/activate.bat (.venv/bin/activate)
- pip install -r requirements.txt
- cd src
- uvicorn main:app --reload
- open link to MadMath website
