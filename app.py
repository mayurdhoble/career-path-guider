from flask import Flask, render_template, request, jsonify, session,redirect
from career_analyzer import CareerAnalyzer
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

analyzer = CareerAnalyzer()

# Career assessment questions
QUESTIONS = [
    "What subjects did you enjoy most in school?",
    "What do you like to do in your free time?",
    "Do you prefer working with people, data, or creative projects?",
    "What type of problems do you enjoy solving?",
    "Do you like to lead teams or work independently?",
    "What skills do you feel you're naturally good at?",
    "What kind of work environment motivates you most?",
    "What are your long-term career goals?",
    "Do you prefer routine tasks or constantly changing challenges?",
    "What impact do you want to make in your career?"
]

@app.route('/')
def index():
    session['current_question'] = 0
    session['responses'] = {}
    return render_template('index.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html', questions=QUESTIONS)

@app.route('/submit_response', methods=['POST'])
def submit_response():
    data = request.json
    question_idx = data['question_index']
    response = data['response']
    
    if 'responses' not in session:
        session['responses'] = {}
    
    session['responses'][QUESTIONS[question_idx]] = response
    session.modified = True
    
    return jsonify({'success': True})

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    if 'responses' not in session:
        return jsonify({'error': 'No responses found'})
    
    # Analyze responses
    analysis = analyzer.analyze_user_responses(session['responses'])
    
    # Store in session for roadmap generation
    session['analysis'] = analysis
    session.modified = True
    
    return jsonify(analysis)

@app.route('/roadmap/<career_path>')
def roadmap(career_path):
    if 'analysis' not in session:
        return redirect('/')
    
    # Generate detailed roadmap
    roadmap_content = analyzer.generate_career_roadmap(
        career_path, 
        session['analysis']['profile']
    )
    
    return render_template('roadmap.html', 
                         career_path=career_path,
                         roadmap=roadmap_content)

if __name__ == '__main__':
    app.run(debug=True)