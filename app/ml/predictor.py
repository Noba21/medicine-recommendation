# import os
# import numpy as np
# import pandas as pd
# from tensorflow.keras.models import load_model
# from pathlib import Path

# class DiseasePredictor:
#     def __init__(self):
#         self.model = None
#         self.dataset = None
#         self.symptoms_list = None
#         self.load_data()
        
#     def load_data(self):
#         """Load the model and dataset"""
#         base_dir = Path(__file__).parent.parent.parent
#         model_path = base_dir / 'model-project' / 'resources' / 'disease_svc_model.pkl'
#         dataset_path = base_dir / 'model-project' / 'resources' / 'preprocessed_symptoms.csv'
        
#         # Load dataset to get symptoms list
#         self.dataset = pd.read_csv(dataset_path)
        
#         # Get unique symptoms from all symptom columns
#         symptom_cols = [col for col in self.dataset.columns if col.startswith('Symptom_')]
#         all_symptoms = set()
#         for col in symptom_cols:
#             symptoms = self.dataset[col].dropna().unique()
#             all_symptoms.update(symptoms)
#         self.symptoms_list = sorted(list(all_symptoms))
        
#         # Load the model
#         self.model = load_model(str(model_path))
        
#     def prepare_input(self, selected_symptoms):
#         """Convert selected symptoms to model input format using one-hot encoding"""
#         # Create a one-hot encoded vector for all unique symptoms
#         input_vector = np.zeros((1, 676))  # Model expects 676 features
        
#         # Get all possible symptoms from the dataset
#         all_symptoms = set()
#         for col in self.dataset.columns:
#             if col.startswith('Symptom_'):
#                 symptoms = self.dataset[col].dropna().unique()
#                 all_symptoms.update(symptoms)
#         symptom_list = sorted(list(all_symptoms))
        
#         # Set 1 for each selected symptom in the one-hot encoded vector
#         for symptom in selected_symptoms:
#             if symptom in symptom_list:
#                 idx = symptom_list.index(symptom)
#                 input_vector[0, idx] = 1
                
#         return input_vector
    
#     def predict(self, symptoms):
#         """Predict disease based on symptoms"""
#         if self.model is None:
#             raise ValueError("Model not loaded")
        
#         if not symptoms:
#             raise ValueError("No symptoms provided")
            
#         # Prepare input
#         X = self.prepare_input(symptoms)
        
#         # Make prediction
#         prediction = self.model.predict(X)
        
#         # Get disease classes
#         diseases = sorted(self.dataset['Disease'].unique())
        
#         # Get top prediction
#         predicted_idx = np.argmax(prediction[0])
#         confidence = prediction[0][predicted_idx]
#         disease = diseases[predicted_idx]
        
#         return {
#             'disease': disease,
#             'confidence': float(confidence),
#             'symptoms': symptoms
#         }
        
#     def get_symptoms(self):
#         """Get list of all possible symptoms"""
#         return self.symptoms_list


import os
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.preprocessing import LabelEncoder

class DiseasePredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.selector = None
        self.selected_features = None
        self.symptoms_list = None
        self.medicine_mapping = None
        self.load_components()
        
    def load_components(self):
        """Load all required models and resources"""
        base_dir = Path(__file__).parent.parent.parent
        resources_path = base_dir / 'medrecommendmodel'
        
        # Load model components
        self.model = joblib.load(resources_path / 'disease_svc_model.pkl')
        self.label_encoder = joblib.load(resources_path / 'label_encoder.pkl')
        self.selector = joblib.load(resources_path / 'feature_selector.pkl')
        self.selected_features = joblib.load(resources_path / 'selected_features.pkl')
        
        # Load symptoms list from CSV
        symptoms_df = pd.read_csv(resources_path / 'preprocessed_symptoms.csv')
        self.symptoms_list = list(symptoms_df.columns[7:])  # All columns after 'Symptom_Count'
        
        # Load medicine mapping
        self.medicine_mapping = pd.read_csv(resources_path / 'medications.csv')
    
    def prepare_input(self, selected_symptoms):
        """Convert selected symptoms to model input format"""
        # Create base feature vector with all symptoms set to 0
        feature_vector = pd.DataFrame(np.zeros((1, len(self.symptoms_list))), 
                                   columns=self.symptoms_list)
        
        # Set selected symptoms to 1
        for symptom in selected_symptoms:
            if symptom in feature_vector.columns:
                feature_vector[symptom] = 1
                
        # Select features using the same selector from training
        selected_features_vector = self.selector.transform(feature_vector)
        return selected_features_vector
    
    def recommend_medicine(self, disease):
        """Get medicine recommendations for a disease"""
        medicines_data = self.medicine_mapping[self.medicine_mapping['Disease'] == disease]['Medication'].tolist()
        
        if not medicines_data:
            return ["Consult a doctor for proper medication"]
        
        # Parse the string representation of the list into an actual list
        if isinstance(medicines_data[0], str) and medicines_data[0].startswith('['):
            # Remove brackets and split by commas
            medicines_str = medicines_data[0].strip('[]')
            # Split by comma and clean up each medicine name
            medicines = [med.strip().strip('\'"') for med in medicines_str.split(',')]
            return medicines
        
        return medicines_data
    
    def predict(self, symptoms):
        """Predict disease based on symptoms and provide medicine recommendations"""
        if not symptoms:
            raise ValueError("No symptoms provided")
            
        # Prepare input
        X = self.prepare_input(symptoms)
        
        # Make prediction
        prediction = self.model.predict(X)
        probabilities = self.model.predict_proba(X)[0]
        
        # Get disease name and probabilities
        disease = self.label_encoder.inverse_transform(prediction)[0]
        disease_probs = {self.label_encoder.classes_[i]: float(prob) 
                        for i, prob in enumerate(probabilities)}
        
        # Sort diseases by probability
        sorted_probs = sorted(disease_probs.items(), key=lambda x: x[1], reverse=True)
        
        # Get top 5 predictions and normalize probabilities
        top_5 = dict(sorted_probs[:5])
        total = sum(top_5.values())
        top_5 = {k: (v/total)*100 for k, v in top_5.items()}
        
        # Get medicine recommendations
        medicines = self.recommend_medicine(disease)
        
        return {
            'top_disease': disease,
            'top_5': top_5,
            'medicines': medicines,
            'symptoms': symptoms
        }
        
    def get_symptoms(self):
        """Get list of all available symptoms"""
        return self.symptoms_list