from flask import Flask, request, render_template
from .inference_engine import InferenceEngine

app = Flask(__name__)
engine = InferenceEngine('app/symptom_data.json')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-symptoms', methods=['POST'])
def check_symptoms():
    user_input = request.form['symptoms'].split(',')
    severity_input = request.form['severity'].split(',')
    
    print(f"User input: {user_input}")  # Debug print
    print(f"Severity input: {severity_input}")  # Debug print
    
    recommendations = engine.analyze_symptoms(
        [symptom.strip() for symptom in user_input],
        [severity.strip() for severity in severity_input]
    )
    print(f"Recommendations passed to template: {recommendations}")  # Debug print
    
    return render_template('results.html', recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
