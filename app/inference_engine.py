import json

class InferenceEngine:
    def __init__(self, knowledge_base_file):
        with open(knowledge_base_file, 'r') as f:
            self.knowledge_base = json.load(f)
        print(f"Loaded knowledge base: {self.knowledge_base}")  # Debug print

    def analyze_symptoms(self, symptoms_input, severity_input, risk_factors_input):
        highest_match = 0
        best_recommendation = "No matches found. Please visit a doctor for further evaluation."
        
        for rule in self.knowledge_base['symptoms']:
            match_rate = self._calculate_match_rate(rule, symptoms_input, severity_input, risk_factors_input)
            if match_rate > highest_match:
                highest_match = match_rate
                best_recommendation = self._generate_advice(rule)
        
        recommendations = [(best_recommendation, highest_match)]
        
        print(f"Generated recommendations: {recommendations}")  # Debug print
        return recommendations

    def _calculate_match_rate(self, rule, symptoms_input, severity_input, risk_factors_input):
        total_checks = 0
        matches = 0

        # Check basic symptom match
        if 'symptom' in rule:
            total_checks += 1
            if rule['symptom'] in symptoms_input:
                matches += 1

        # Check duration if applicable
        if 'duration' in rule:
            total_checks += 1
            if rule['duration'] in severity_input:
                matches += 1

        # Check severity if applicable
        if 'severity' in rule:
            total_checks += 1
            if rule['severity'] in severity_input:
                matches += 1

        # Check comorbidity (e.g., multiple symptoms together)
        if 'comorbid_symptoms' in rule:
            total_checks += len(rule['comorbid_symptoms'])
            matches += sum(1 for symptom in rule['comorbid_symptoms'] if symptom in symptoms_input)

        # Check risk factors if applicable
        if 'risk_factors' in rule:
            total_checks += len(rule['risk_factors'])
            matches += sum(1 for risk_factor in rule['risk_factors'] if risk_factor in risk_factors_input)

        if total_checks == 0:
            return 0
        return (matches / total_checks) * 100

    def _generate_advice(self, rule):
        if 'advice' in rule:
            return rule['advice']
        elif 'condition' in rule:
            return f"Possible condition: {rule['condition']}"
