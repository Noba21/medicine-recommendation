# import streamlit as st
# import pandas as pd
# import numpy as np
# import tensorflow as tf
# import plotly.express as px
# from tensorflow.keras.models import load_model
# import random

# # Set the theme for the app
# st.set_page_config(page_title="🩺 Disease Prediction Based on Symptoms", layout="wide")

# # Load the trained MLP model
# model = load_model('resources/mlp_model.h5')

# # Load and prepare the dataset
# df = pd.read_csv('resources/dataset_kaggle.csv')

# # Full list of symptoms
# symptoms_list = [
#     "foul_smell_of_urine",
#     "neck_pain",
#     "blackheads",
#     "irritation_in_anus",
#     "movement_stiffness",
#     "cramps",
#     "pus_filled_pimples",
#     "indigestion",
#     "back_pain",
#     "breathlessness",
#     "stomach_pain",
#     "cold_hands_and_feets",
#     "silver_like_dusting",
#     "patches_in_throat",
#     "vomiting",
#     "anxiety",
#     "nausea",
#     "yellowish_skin",
#     "fatigue",
#     "weight_loss",
#     "obesity",
#     "knee_pain",
#     "swelling_of_stomach",
#     "joint_pain",
#     "loss_of_balance",
#     "dischromic__patches",
#     "chills",
#     "small_dents_in_nails",
#     "skin_peeling",
#     "altered_sensorium",
#     "spinning_movements",
#     "watering_from_eyes",
#     "weakness_of_one_body_side",
#     "excessive_hunger",
#     "extra_marital_contacts",
#     "dark_urine",
#     "pain_during_bowel_movements",
#     "high_fever",
#     "abdominal_pain",
#     "swollen_legs",
#     "sweating",
#     "yellowing_of_eyes",
#     "hip_joint_pain",
#     "bruising",
#     "dehydration",
#     "diarrhoea",
#     "lethargy",
#     "pain_in_anal_region",
#     "family_history",
#     "yellow_crust_ooze",
#     "swelling_joints",
#     "sunken_eyes",
#     "weakness_in_limbs",
#     "itching",
#     "loss_of_appetite",
#     "dizziness",
#     "nodal_skin_eruptions",
#     "headache",
#     "scurring",
#     "continuous_feel_of_urine",
#     "painful_walking",
#     "restlessness",
#     "acidity",
#     "distention_of_abdomen",
#     "continuous_sneezing",
#     "stiff_neck",
#     "muscle_weakness",
#     "spotting__urination",
#     "blister",
#     "skin_rash",
#     "muscle_wasting",
#     "red_sore_around_nose",
#     "bladder_discomfort",
#     "cough",
#     "bloody_stool",
#     "weight_gain",
#     "passage_of_gases",
#     "shivering",
#     "lack_of_concentration",
#     "ulcers_on_tongue",
#     "blurred_and_distorted_vision",
#     "mood_swings",
#     "chest_pain",
#     "burning_micturition",
#     "irregular_sugar_level",
#     "constipation"
# ]

# # Streamlit app layout
# st.title("🩺 Disease Prediction Based on Symptoms")
# st.markdown("""
# Welcome to the Disease Prediction app. This tool allows healthcare providers and patients to input symptoms and receive potential disease predictions based on machine learning. The predictions prioritize serious illnesses depending on the symptoms provided.
# """)

# # Initialize selected symptoms list
# if 'selected_symptoms' not in st.session_state:
#     st.session_state.selected_symptoms = ['Please Select'] * 5

# # Function to display dropdowns and manage selections
# def display_dropdowns():
#     for i in range(len(st.session_state.selected_symptoms)):
#         options = ['Please Select'] + sorted(set(symptoms_list) - set(st.session_state.selected_symptoms[:i] + st.session_state.selected_symptoms[i+1:]))

#         # Initialize session state for the typed value if not already set
#         if f"typed_{i}" not in st.session_state:
#             st.session_state[f"typed_{i}"] = ""

#         def on_select_change():
#             typed_value = st.session_state[f"typed_{i}"].strip()
#             if typed_value in symptoms_list:
#                 st.session_state.selected_symptoms[i] = typed_value
#             elif st.session_state.selected_symptoms[i] not in symptoms_list:
#                 st.session_state.selected_symptoms[i] = 'Please Select'

#         selected_symptom = st.selectbox(
#             f"Symptom {i+1}",
#             options=options,
#             index=options.index(st.session_state.selected_symptoms[i]) if st.session_state.selected_symptoms[i] in options else 0,
#             key=f"dropdown_{i}",
#             on_change=on_select_change
#         )

#         st.session_state.selected_symptoms[i] = selected_symptom

#     if len(st.session_state.selected_symptoms) < 17:
#         if st.button("Add Another Symptom"):
#             st.session_state.selected_symptoms.append('Please Select')

# # Create a two-column layout
# col1, col2 = st.columns([1, 1])

# with col1:
#     # Display dropdowns for symptom selection
#     display_dropdowns()

# # Filter out 'Please Select' from the final symptom list
# final_selected_symptoms = [symptom for symptom in st.session_state.selected_symptoms if symptom != 'Please Select' and symptom in symptoms_list]

# # Placeholder for the pie chart
# with col2:
#     if len(final_selected_symptoms) < 5:
#         fig = px.pie(names=["Please make symptom selections to generate probable disease cause"], values=[100], title="Awaiting Input")
#         st.markdown("**User must select at least 5 symptoms for Predict to be enabled**", unsafe_allow_html=True)
#         st.plotly_chart(fig)
#     else:
#         # Limit number of selected symptoms to 17
#         if len(final_selected_symptoms) > 17:
#             st.warning("You can only select up to 17 symptoms.")
#             final_selected_symptoms = final_selected_symptoms[:17]

#         # Disable predict button if conditions are not met
#         predict_disabled = len(final_selected_symptoms) < 5 or len(final_selected_symptoms) > 17

#         if st.button("Predict", disabled=predict_disabled):
#             # Convert selected symptoms to encoded format
#             encoded_symptoms = np.zeros(len(symptoms_list))
#             for symptom in final_selected_symptoms:
#                 if symptom in symptoms_list:
#                     encoded_symptoms[symptoms_list.index(symptom)] = 1

#             # Prepare input for the model
#             final_input = np.zeros((1, 676))  # Ensure the input has 676 features as expected by the model
#             final_input[0, :len(encoded_symptoms)] = encoded_symptoms

#             # Predict using the model
#             predictions = model.predict(final_input)

#             # Post-prediction adjustments
#             disease_match_scores = {}
#             for _, row in df.iterrows():
#                 disease_symptoms = row[1:].values  # Skip the first column (Disease)
#                 disease_encoded = np.array([1 if symptom in disease_symptoms else 0 for symptom in symptoms_list])
#                 match_score = np.sum(encoded_symptoms == disease_encoded)
#                 disease_match_scores[row['Disease']] = match_score

#             # Exact match boost
#             if any(np.array_equal(encoded_symptoms, df.iloc[i, 1:].values) for i in range(len(df))):
#                 exact_match_disease = next(df['Disease'][i] for i in range(len(df)) if np.array_equal(encoded_symptoms, df.iloc[i, 1:].values))
#                 exact_match_idx = df[df['Disease'] == exact_match_disease].index[0]
#                 if exact_match_idx < len(predictions[0]):
#                     predictions[0][exact_match_idx] *= 2.0

#             # Partial match boost
#             elif any(score >= 10 for score in disease_match_scores.values()):
#                 partial_match_disease = max(disease_match_scores, key=disease_match_scores.get)
#                 partial_match_idx = df[df['Disease'] == partial_match_disease].index[0]
#                 if partial_match_idx < len(predictions[0]):
#                     predictions[0][partial_match_idx] *= 1.5

#             # Less significant match boost
#             else:
#                 best_match_disease = max(disease_match_scores, key=disease_match_scores.get)
#                 best_match_idx = df[df['Disease'] == best_match_disease].index[0]
#                 if best_match_idx < len(predictions[0]):
#                     predictions[0][best_match_idx] *= 1.2

#             # Normalize predictions
#             predictions = predictions / predictions.sum() * 100

#             # Create DataFrame for predictions
#             diseases = df['Disease'].unique()
#             prediction_df = pd.DataFrame(predictions, columns=diseases).T
#             prediction_df.columns = ['Probability']
#             prediction_df = prediction_df.sort_values(by='Probability', ascending=False)

#             # Select the top 5 diseases
#             top_5 = prediction_df.head(5)

#             # Adjust the probabilities to sum to 100%
#             top_5['Probability'] = (top_5['Probability'] / top_5['Probability'].sum()) * 100

#             # Display the prediction result text
#             st.markdown(f"**Patient has a high chance of having {top_5.index[0]}**")

#             # Plot interactive pie chart for the top 5 diseases
#             fig = px.pie(top_5, values='Probability', names=top_5.index, title='Top 5 Disease Predictions')
#             fig.update_traces(textposition='inside', textinfo='percent+label')
#             fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=400, width=400)
#             st.plotly_chart(fig)

#             # Display additional disease suggestions
#             remaining_diseases = prediction_df.iloc[5:].index.tolist()
#             if remaining_diseases:
#                 additional_diseases = random.sample(remaining_diseases, min(4, len(remaining_diseases)))
#                 st.write("Here are additional diseases the medical provider may want to consider, accompanied by lab work, diagnoses, and care suggestions.")
#                 st.write(", ".join(additional_diseases))
#             else:
#                 st.write("No other diseases can be indicated at this time.")
#             st.write("""
#             This data was pulled from the CDC using their research studies on listed diseases and symptoms. Please note that these predictions are not definitive diagnoses and should be used as a guide to aid in clinical decision-making. For accurate diagnosis and treatment, medical professionals should rely on comprehensive clinical evaluation and testing.
#             """)

# # Custom styling for a medical-themed look with a smooth background image
# st.markdown("""
#     <style>
#     body {
#         background-image: url('https://www.example.com/medical_background.jpg');
#         background-size: cover;
#         background-attachment: fixed;
#     }
#     .stButton button {
#         background-color: #4CAF50;
#         color: white;
#         border-radius: 5px;
#         padding: 8px;
#         margin-top: 8px;
#         width: 100%;
#     }
#     .stButton button:hover {
#         background-color: #45a049;
#     }
#     .stMarkdown {
#         font-family: Arial, sans-serif;
#         color: #333333;
#         font-size: 15px;
#     }
#     .css-1aumxhk {
#         padding: 15px;
#         background: rgba(255, 255, 255, 0.8);
#         border-radius: 10px;
#     }
#     .css-18e3th9 {
#         padding: 15px;
#     }
#     </style>
#     """, unsafe_allow_html=True)



# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import plotly.express as px
# from sklearn.preprocessing import LabelEncoder
# import random

# # Set the theme for the app
# st.set_page_config(page_title="🩺 Disease Prediction and Medicine Recommendation", layout="wide")

# # Load the trained SVC model and components
# model = joblib.load('resources\disease_svc_model.pkl')
# label_encoder = joblib.load('resources\label_encoder.pkl')
# selector = joblib.load('resources\feature_selector.pkl')
# selected_features = joblib.load('resources\selected_features.pkl')

# # Load the medicine mapping
# medicine_mapping = pd.read_csv('resources\medications.csv')

# # Load the dataset to get all symptom columns
# df = pd.read_csv('resources\preprocessed_symptoms.csv')
# symptom_columns = df.columns[7:]  # All columns after 'Symptom_Count'

# # Streamlit app layout
# st.title("🩺 Disease Prediction and Medicine Recommendation")
# st.markdown("""
# Welcome to the Disease Prediction app. This tool allows healthcare providers and patients to input symptoms and receive potential disease predictions with medicine recommendations based on machine learning.
# """)

# # Function to recommend medicines
# def recommend_medicine(disease):
#     medicines = medicine_mapping[medicine_mapping['Disease'] == disease]['Medication'].tolist()
#     return medicines if medicines else ["Consult a doctor for proper medication"]

# # Initialize selected symptoms list
# if 'selected_symptoms' not in st.session_state:
#     st.session_state.selected_symptoms = []

# # Create a two-column layout
# col1, col2 = st.columns([1, 1])

# with col1:
#     st.subheader("Select Your Symptoms")
    
#     # Multiselect widget for symptoms
#     selected_symptoms = st.multiselect(
#         "Choose symptoms (select at least 3):",
#         options=sorted(symptom_columns),
#         default=st.session_state.selected_symptoms
#     )
    
#     st.session_state.selected_symptoms = selected_symptoms

#     # Predict button
#     predict_disabled = len(selected_symptoms) < 3
#     if st.button("Predict", disabled=predict_disabled):
#         # Create feature vector
#         feature_vector = pd.DataFrame(np.zeros((1, len(symptom_columns))), 
#                                     columns=symptom_columns)
        
#         # Set selected symptoms to 1
#         for symptom in selected_symptoms:
#             if symptom in feature_vector.columns:
#                 feature_vector[symptom] = 1
        
#         # Select features and predict
#         selected_features_vector = selector.transform(feature_vector)
#         prediction = model.predict(selected_features_vector)
#         probabilities = model.predict_proba(selected_features_vector)[0]
        
#         # Get disease name and probabilities
#         disease = label_encoder.inverse_transform(prediction)[0]
#         disease_probs = {label_encoder.classes_[i]: prob 
#                         for i, prob in enumerate(probabilities)}
        
#         # Sort diseases by probability
#         sorted_probs = sorted(disease_probs.items(), 
#                             key=lambda x: x[1], reverse=True)
        
#         # Get top 5 predictions
#         top_5 = dict(sorted_probs[:5])
        
#         # Adjust probabilities to sum to 100%
#         total = sum(top_5.values())
#         top_5 = {k: (v/total)*100 for k, v in top_5.items()}
        
#         # Get medicine recommendations
#         medicines = recommend_medicine(disease)
        
#         # Store results in session state
#         st.session_state.prediction_results = {
#             'top_disease': disease,
#             'top_5': top_5,
#             'medicines': medicines
#         }

# with col2:
#     if 'prediction_results' in st.session_state:
#         results = st.session_state.prediction_results
        
#         # Display the prediction result
#         st.markdown(f"**Most Likely Disease: {results['top_disease']}**")
        
#         # Display medicine recommendations
#         st.subheader("Recommended Medicines:")
#         for med in results['medicines']:
#             st.write(f"- {med}")
        
#         # Plot interactive pie chart for the top 5 diseases
#         prediction_df = pd.DataFrame.from_dict(results['top_5'], 
#                                              orient='index', 
#                                              columns=['Probability'])
#         fig = px.pie(prediction_df, 
#                     values='Probability', 
#                     names=prediction_df.index, 
#                     title='Top 5 Disease Predictions')
#         fig.update_traces(textposition='inside', textinfo='percent+label')
#         fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), 
#                          height=400, 
#                          width=400)
#         st.plotly_chart(fig)
        
#         # Display disclaimer
#         st.markdown("""
#         **Disclaimer:**  
#         These predictions are not definitive diagnoses and should be used as a guide to aid in clinical decision-making. 
#         For accurate diagnosis and treatment, medical professionals should rely on comprehensive clinical evaluation and testing.
#         """)
#     else:
#         st.subheader("Prediction Results Will Appear Here")
#         if len(selected_symptoms) < 3:
#             st.warning("Please select at least 3 symptoms to enable prediction.")

# # Custom styling
# st.markdown("""
#     <style>
#     .stButton button {
#         background-color: #4CAF50;
#         color: white;
#         border-radius: 5px;
#         padding: 8px;
#         margin-top: 8px;
#         width: 100%;
#     }
#     .stButton button:hover {
#         background-color: #45a049;
#     }
#     .stMarkdown {
#         font-family: Arial, sans-serif;
#         color: #333333;
#         font-size: 15px;
#     }
#     .css-1aumxhk {
#         padding: 15px;
#         background: rgba(255, 255, 255, 0.9);
#         border-radius: 10px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

# Set the theme for the app
st.set_page_config(page_title="🩺 Disease Prediction and Medicine Recommendation", layout="wide")

# Load the trained SVC model and components
model = joblib.load('resources\\disease_svc_model.pkl')
label_encoder = joblib.load('resources\\label_encoder.pkl')
selector = joblib.load('resources\\feature_selector.pkl')
selected_features = joblib.load('resources\\selected_features.pkl')

# Load the medicine mapping
medicine_mapping = pd.read_csv('resources\\medications.csv')

# Use provided symptoms list
symptoms_list = [
    "foul_smell_of_urine", "neck_pain", "blackheads", "irritation_in_anus",
    "movement_stiffness", "cramps", "pus_filled_pimples", "indigestion",
    "back_pain", "breathlessness", "stomach_pain", "cold_hands_and_feets",
    "silver_like_dusting", "patches_in_throat", "vomiting", "anxiety",
    "nausea", "yellowish_skin", "fatigue", "weight_loss", "obesity",
    "knee_pain", "swelling_of_stomach", "joint_pain", "loss_of_balance",
    "dischromic__patches", "chills", "small_dents_in_nails", "skin_peeling",
    "altered_sensorium", "spinning_movements", "watering_from_eyes",
    "weakness_of_one_body_side", "excessive_hunger", "extra_marital_contacts",
    "dark_urine", "pain_during_bowel_movements", "high_fever", "abdominal_pain",
    "swollen_legs", "sweating", "yellowing_of_eyes", "hip_joint_pain",
    "bruising", "dehydration", "diarrhoea", "lethargy", "pain_in_anal_region",
    "family_history", "yellow_crust_ooze", "swelling_joints", "sunken_eyes",
    "weakness_in_limbs", "itching", "loss_of_appetite", "dizziness",
    "nodal_skin_eruptions", "headache", "scurring", "continuous_feel_of_urine",
    "painful_walking", "restlessness", "acidity", "distention_of_abdomen",
    "continuous_sneezing", "stiff_neck", "muscle_weakness", "spotting__urination",
    "blister", "skin_rash", "muscle_wasting", "red_sore_around_nose",
    "bladder_discomfort", "cough", "bloody_stool", "weight_gain",
    "passage_of_gases", "shivering", "lack_of_concentration", "ulcers_on_tongue",
    "blurred_and_distorted_vision", "mood_swings", "chest_pain",
    "burning_micturition", "irregular_sugar_level", "constipation"
]

# Use symptoms_list as symptom_columns (maintaining order for model compatibility)
symptom_columns = symptoms_list

# Streamlit app layout
st.title("🩺 Disease Prediction and Medicine Recommendation")
st.markdown("""
Welcome to the Disease Prediction app. This tool allows healthcare providers and patients to input symptoms and receive potential disease predictions with medicine recommendations based on machine learning.
""")

# Function to recommend medicines
def recommend_medicine(disease):
    medicines = medicine_mapping[medicine_mapping['Disease'] == disease]['Medication'].tolist()
    return medicines if medicines else ["Consult a doctor for proper medication"]

# Initialize session state for dropdown selections
for i in range(1, 6):
    if f'symptom_{i}' not in st.session_state:
        st.session_state[f'symptom_{i}'] = 'None'

# Create a two-column layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Select Your Symptoms")
    
    # Dropdown symptom selection
    num_dropdowns = 5
    selected_symptoms = []

    for i in range(1, num_dropdowns + 1):
        current_key = f'symptom_{i}'
        current_value = st.session_state.get(current_key, 'None')
        
        # Collect previously selected symptoms
        prev_symptoms = []
        for j in range(1, i):
            val = st.session_state.get(f'symptom_{j}', 'None')
            if val != 'None':
                prev_symptoms.append(val)
        
        # Generate available options (sorted for UX)
        available_options = [s for s in sorted(symptom_columns) if s not in prev_symptoms]
        
        # Reset invalid selections
        if current_value != 'None' and current_value not in available_options:
            st.session_state[current_key] = 'None'
            current_value = 'None'
        
        # Handle empty options
        if not available_options:
            available_options = ['No more symptoms available']
        
        # Calculate index for selectbox
        try:
            index = available_options.index(current_value) + 1 if current_value != 'None' else 0
        except ValueError:
            index = 0
        
        # Render selectbox
        selected = st.selectbox(
            f"Symptom {i}",
            options=['None'] + available_options,
            index=index,
            key=current_key
        )
        
        # Add valid selections to list
        if selected != 'None' and selected != 'No more symptoms available':
            selected_symptoms.append(selected)
    
    # Update session state with selected symptoms
    st.session_state.selected_symptoms = selected_symptoms

    # Predict button
    predict_disabled = len(selected_symptoms) < 3
    if st.button("Predict", disabled=predict_disabled):
        # Create feature vector
        feature_vector = pd.DataFrame(np.zeros((1, len(symptom_columns))), 
                                    columns=symptom_columns)
        
        # Set selected symptoms to 1
        for symptom in selected_symptoms:
            if symptom in feature_vector.columns:
                feature_vector[symptom] = 1
        
        # Select features and predict
        selected_features_vector = selector.transform(feature_vector)
        prediction = model.predict(selected_features_vector)
        probabilities = model.predict_proba(selected_features_vector)[0]
        
        # Get disease name and probabilities
        disease = label_encoder.inverse_transform(prediction)[0]
        disease_probs = {label_encoder.classes_[i]: prob 
                        for i, prob in enumerate(probabilities)}
        
        # Sort diseases by probability
        sorted_probs = sorted(disease_probs.items(), 
                            key=lambda x: x[1], reverse=True)
        
        # Get top 5 predictions
        top_5 = dict(sorted_probs[:5])
        
        # Adjust probabilities to sum to 100%
        total = sum(top_5.values())
        top_5 = {k: (v/total)*100 for k, v in top_5.items()}
        
        # Get medicine recommendations
        medicines = recommend_medicine(disease)
        
        # Store results in session state
        st.session_state.prediction_results = {
            'top_disease': disease,
            'top_5': top_5,
            'medicines': medicines
        }

with col2:
    if 'prediction_results' in st.session_state:
        results = st.session_state.prediction_results
        
        # Display the prediction result
        st.markdown(f"**Most Likely Disease: {results['top_disease']}**")
        
        # Display medicine recommendations
        st.subheader("Recommended Medicines:")
        for med in results['medicines']:
            st.write(f"- {med}")
        
        # Plot interactive pie chart for the top 5 diseases
        prediction_df = pd.DataFrame.from_dict(results['top_5'], 
                                             orient='index', 
                                             columns=['Probability'])
        fig = px.pie(prediction_df, 
                    values='Probability', 
                    names=prediction_df.index, 
                    title='Top 5 Disease Predictions')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), 
                         height=400, 
                         width=400)
        st.plotly_chart(fig)
        
        # Display disclaimer
        st.markdown("""
        **Disclaimer:**  
        These predictions are not definitive diagnoses and should be used as a guide to aid in clinical decision-making. 
        For accurate diagnosis and treatment, medical professionals should rely on comprehensive clinical evaluation and testing.
        """)
    else:
        st.subheader("Prediction Results Will Appear Here")
        if len(st.session_state.selected_symptoms) < 3:
            st.warning("Please select at least 3 symptoms to enable prediction.")

# Custom styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 8px;
        margin-top: 8px;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stMarkdown {
        font-family: Arial, sans-serif;
        color: #333333;
        font-size: 15px;
    }
    .css-1aumxhk {
        padding: 15px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)