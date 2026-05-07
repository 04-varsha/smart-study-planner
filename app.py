from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import random
import sqlite3

app = Flask(__name__)

# ---------------- HOME ----------------

@app.route("/")
def index():

    return render_template(
        "index.html",
        timetable=None,
        questions=None
    )

# ---------------- TIMETABLE GENERATION ----------------

@app.route("/add", methods=["POST"])
def add_task():

    timetable = []

    days = int(request.form["days"])

    subjects = []

    for i in range(1, 5):

        subject = request.form[f"subject{i}"]

        marks = int(request.form[f"marks{i}"])

        # AUTO STUDY HOURS BASED ON MARKS

        if marks >= 85:
            hours = 1

        elif marks >= 70:
            hours = 2

        elif marks >= 50:
            hours = 3

        else:
            hours = 4

        subjects.append({
            "name": subject,
            "hours": hours
        })

        # SAVE TO DATABASE

        conn = sqlite3.connect("database.db")

        conn.execute(
            "INSERT INTO tasks(name, marks, hours, completed) VALUES (?, ?, ?, ?)",
            (subject, marks, hours, 0)
        )

        conn.commit()
        conn.close()

    # AUTO TIMETABLE

    for day in range(1, days + 1):

        timetable.append({

            "day": f"Day {day}",

            "s1": f"{subjects[0]['name']} - {subjects[0]['hours']} hrs",

            "s2": f"{subjects[1]['name']} - {subjects[1]['hours']} hrs",

            "s3": f"{subjects[2]['name']} - {subjects[2]['hours']} hrs",

            "s4": f"{subjects[3]['name']} - {subjects[3]['hours']} hrs"

        })

    return render_template(

        "index.html",

        timetable=timetable,

        questions=None

    )

# ---------------- PDF QUIZ GENERATOR ----------------

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():

    file = request.files["pdf"]

    reader = PdfReader(file)

    text = ""

    # EXTRACT TEXT FROM PDF

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    # SPLIT INTO SENTENCES

    lines = text.split(".")

    questions = []

    # ---------------- CREATE WORD POOL ----------------

    all_words = []

    for line in lines:

        words = line.strip().split()

        for word in words:

            clean_word = word.strip(",.!?()[]{}").capitalize()

            # KEEP ONLY VALID WORDS

            if len(clean_word) > 3 and clean_word.isalpha():

                all_words.append(clean_word)

    # REMOVE DUPLICATES

    all_words = list(set(all_words))

    # ---------------- GENERATE QUESTIONS ----------------

    for line in lines[:20]:

        words = line.strip().split()

        if len(words) > 6:

            # CHOOSE ANSWER

            answer = words[0].strip(",.!?()[]{}").capitalize()

            # CREATE QUESTION

            question = line.replace(words[0], "___")

            # GENERATE WRONG OPTIONS FROM PDF WORDS

            available_words = [
                w for w in all_words if w != answer
            ]

            # ENSURE ENOUGH OPTIONS EXIST

            if len(available_words) >= 3:

                wrong_options = random.sample(
                    available_words,
                    3
                )

                options = wrong_options + [answer]

                random.shuffle(options)

                questions.append({

                    "question": question,

                    "options": options,

                    "answer": answer

                })

    return render_template(

        "index.html",

        timetable=None,

        questions=questions

    )

# ---------------- RUN APP ----------------

if (__name__) == "__main__":
    app.run(debug=True)