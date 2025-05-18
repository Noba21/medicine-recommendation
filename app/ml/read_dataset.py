import pandas as pd

# Read the dataset
df = pd.read_csv('../model-project/resources/preprocessed_symptoms.csv')

# Print the first few rows and shape
print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())
