from flask import Flask, render_template, request, redirect, url_for, session
import requests
import html
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def fetch_questions(amount=10):
    url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
    response = requests.get(url)
    data = response.json()
    questions = []
    for item in data["results"]:
        question = html.unescape(item["question"])
        correct = html.unescape(item["correct_answer"])
        incorrect = [html.unescape(i) for i in item["incorrect_answers"]]
        options = incorrect + [correct]
        random.shuffle(options)
        questions.append({
            "question": question,
            "options": options,
            "answer": correct
        })
    return questions

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start', methods=['POST'])
def start():
    session['questions'] = fetch_questions()
    session['current'] = 0
    session['score'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        selected = request.form.get('option')
        current_q = session['current']
        correct = session['questions'][current_q]['answer']
        if selected == correct:
            session['score'] += 1
        session['current'] += 1

    if session['current'] >= len(session['questions']):
        return redirect(url_for('result'))

    q = session['questions'][session['current']]
    return render_template('quiz.html', qnum=session['current'] + 1, question=q['question'], options=q['options'])

@app.route('/result')
def result():
    return render_template('result.html', score=session['score'], total=len(session['questions']))

if __name__ == '__main__':
    app.run(debug=True)
