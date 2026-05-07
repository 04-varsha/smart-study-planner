from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import random

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

    # AUTO TIMETABLE

    for day in range(1, days + 1):

        timetable.append({

            "day": f"Day {day}",

            "s1": subjects[0]["name"],

            "s2": subjects[1]["name"],

            "s3": subjects[2]["name"],

            "s4": subjects[3]["name"]

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

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    lines = text.split(".")

    questions = []

    for line in lines[:20]:

        words = line.strip().split()

        if len(words) > 6:

            answer = words[0]

            question = line.replace(answer, "_____")

            options = [
                answer,
                "Computer",
                "Database",
                "Network"
            ]

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

if __name__ == "__main__":
    app.run(debug=True)