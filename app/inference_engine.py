import json

class InferenceEngine:
    def __init__(self, knowledge_base_file):
        with open(knowledge_base_file, 'r') as f:
            self.knowledge_base = json.load(f)
        print(f"Loaded knowledge base: {self.knowledge_base}")  # Debug print

    def analyze_symptoms(self, symptoms_input, severity_input):
        best_recommendation = "No matches found. Please visit a doctor for further evaluation."
        
        for rule in self.knowledge_base['symptoms']:
            if self._check_rule(rule, symptoms_input, severity_input):
                best_recommendation = self._generate_advice(rule)
                break
        
        recommendations = [best_recommendation]
        
        print(f"Generated recommendations: {recommendations}")  # Debug print
        return recommendations

    def _check_rule(self, rule, symptoms_input, severity_input):
        # Check basic symptom match
        if 'symptom' in rule and rule['symptom'] not in symptoms_input:
            return False
        
        # Check duration if applicable
        if 'duration' in rule and rule['duration'] not in severity_input:
            return False

        # Check severity if applicable
        if 'severity' in rule and rule['severity'] not in severity_input:
            return False

        # Check comorbidity (e.g., multiple symptoms together)
        if 'comorbid_symptoms' in rule:
            if not all(symptom in symptoms_input for symptom in rule['comorbid_symptoms']):
                return False

        return True

    def _generate_advice(self, rule):
        if 'advice' in rule:
            return rule['advice']
        elif 'condition' in rule:
            return f"Possible condition: {rule['condition']}"
