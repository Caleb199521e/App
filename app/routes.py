from flask import Flask, request, render_template, redirect, url_for
from .inference_engine import InferenceEngine

app = Flask(__name__)
engine = InferenceEngine('app/symptom_data.json')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check-symptoms', methods=['POST'])
def check_symptoms():
    user_input = request.form['symptoms'].split(',')
    symptoms_input = [symptom.strip() for symptom in user_input]

    # Redirect to the associated symptoms page
    return redirect(url_for('associated_symptoms', symptoms=','.join(symptoms_input)))

@app.route('/associated-symptoms', methods=['GET', 'POST'])
def associated_symptoms():
    if request.method == 'POST':
        symptoms_input = request.form['symptoms'].split(',')
        duration_input = request.form['duration'].split(',')
        severity_input = request.form['severity'].split(',')
        associated_symptoms_input = request.form['associated_symptoms'].split(',')

        recommendations = engine.analyze_symptoms(
            [symptom.strip() for symptom in symptoms_input],
            [duration.strip() for duration in duration_input],
            [severity.strip() for severity in severity_input],
            [associated_symptom.strip() for associated_symptom in associated_symptoms_input]
        )
        return render_template('results.html', recommendations=recommendations)

    symptoms = request.args.get('symptoms')
    if symptoms:
        symptoms = symptoms.split(',')
    else:
        symptoms = []
    return render_template('associated_symptoms.html', symptoms=symptoms)

if __name__ == "__main__":
    app.run(debug=True)
