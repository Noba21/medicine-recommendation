import pandas as pd
from pathlib import Path

# Load the dataset
base_dir = Path(__file__).parent.parent.parent
dataset_path = base_dir / 'model-project' / 'resources' / 'preprocessed_symptoms.csv'
df = pd.read_csv(dataset_path)

# Print information about the dataset
print("Dataset shape:", df.shape)
print("\nColumns:")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

print("\nSample data:")
print(df.head())
