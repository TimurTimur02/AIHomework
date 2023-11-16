from flask import Flask, request, render_template, redirect, url_for
import csv
import json

app = Flask(__name__)

with open('retail_system_survey_questions.json', 'r', encoding='utf-8') as file:
    survey_questions = json.load(file)

def save_answers(answers):
    with open('survey_responses.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(answers)

@app.route('/')
def survey():
    return render_template('survey.html', survey_questions=survey_questions)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        answers = [request.form.get(question['question']) for question in survey_questions]
        save_answers(answers)
        return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return "Спасибо за участие в опросе!"

if __name__ == '__main__':
    app.run(debug=True)
