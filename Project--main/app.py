from flask import Flask, render_template, request, redirect, session, url_for 
from backend import GameManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
game_manager = GameManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    session['game_type'] = request.form['game_type']
    session['category'] = request.form['category']
    session['score'] = 0
    session['streak'] = 0
    session['difficulty'] = 'easy'
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = session.get('correct_answer')

        if game_manager.check_answer(user_answer, correct_answer):
            session['score'] += 1
            session['streak'] += 1
            feedback = "Correct!"
        else:
            session['streak'] = 0
            feedback = f"Incorrect! The correct answer was {correct_answer}."

        session['difficulty'] = game_manager.adjust_difficulty(session['streak'])
        
        return render_template(
            'feedback.html', 
            feedback=feedback, 
            score=session['score'], 
            streak=session['streak'], 
            difficulty=session['difficulty']
        )

    # GET method - show new question
    game_type = session.get('game_type')
    category = session.get('category')
    difficulty = session.get('difficulty')

    question_data = game_manager.get_question(game_type, category, difficulty)
    session['correct_answer'] = question_data.get('answer')

    return render_template('question.html', question=question_data, game_type=game_type)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


