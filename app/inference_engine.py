import json
import json
import nltk
from nltk.corpus import wordnet

# Ensure WordNet is downloaded
nltk.download('wordnet')

class InferenceEngine:
    def __init__(self, knowledge_base_file):
        with open(knowledge_base_file, 'r') as f:
            self.knowledge_base = json.load(f)
        print(f"Loaded knowledge base: {self.knowledge_base}")  # Debug print

    def _get_synonyms(self, word):
        """Retrieve synonyms for a given word using WordNet."""
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().replace('_', ' '))  # Replace underscores with spaces
        return synonyms

    def analyze_symptoms(self, symptoms_input, duration_input, severity_input, associated_symptoms_input):
        recommendations = []
        partial_matches = []

        for rule in self.knowledge_base['symptoms']:
            match_percentage = self._calculate_match_percentage(rule, symptoms_input, duration_input, severity_input, associated_symptoms_input)
            if match_percentage >= 50:  # Threshold for a full match
                advice = self._generate_advice(rule)
                recommendations.append({
                    "reported_symptoms": symptoms_input,
                    "potential_condition": rule.get('condition', 'Unknown condition'),
                    "advice": advice
                })
            elif match_percentage > 0:  # Collect partial matches
                partial_matches.append({
                    "reported_symptoms": symptoms_input,
                    "potential_condition": rule.get('condition', 'Unknown condition'),
                    "match_percentage": match_percentage,
                    "advice": rule.get('advice', 'Please visit a doctor for further evaluation.')
                })

        if not recommendations:
            if partial_matches:
                # Sort partial matches by match percentage
                partial_matches.sort(key=lambda x: x["match_percentage"], reverse=True)
                # Provide the top partial match as a suggestion
                top_partial_match = partial_matches[0]
                recommendations.append({
                    "reported_symptoms": symptoms_input,
                    "potential_condition": top_partial_match["potential_condition"],
                    "advice": f"Partial match found ({top_partial_match['match_percentage']}% match). {top_partial_match['advice']}"
                })
            else:
                recommendations.append({
                    "reported_symptoms": symptoms_input,
                    "potential_condition": "No matches found",
                    "advice": "No clear match found. Please consult a healthcare professional for further evaluation."
                })

        print(f"Generated recommendations: {recommendations}")  # Debug print
        return recommendations

    def _calculate_match_percentage(self, rule, symptoms_input, duration_input, severity_input, associated_symptoms_input):
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
            if rule['duration'] in duration_input:
                matches += 1

        # Check severity if applicable
        if 'severity' in rule:
            total_checks += 1
            if rule['severity'] in severity_input:
                matches += 1

        # Check comorbidity (e.g., multiple symptoms together)
        if 'comorbid_symptoms' in rule:
            total_checks += len(rule['comorbid_symptoms'])
            matches += sum(1 for symptom in rule['comorbid_symptoms'] if symptom in symptoms_input or symptom in associated_symptoms_input)

        if total_checks == 0:
            return 0
        return (matches / total_checks) * 100  # Return match percentage

    def _generate_advice(self, rule):
        advice = rule.get('advice', '')
        condition = rule.get('condition', '')
        if condition:
            advice += f" Possible condition: {condition}"
        return advice