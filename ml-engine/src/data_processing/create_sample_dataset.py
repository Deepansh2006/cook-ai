import pandas as pd
from pathlib import Path

# Get project root dynamically
BASE_DIR = Path(__file__).resolve().parents[2]

# Define paths
raw_data_path = BASE_DIR / "data" / "raw" / "recipes.csv"
output_path = BASE_DIR / "data" / "raw" / "recipes_small.csv"

print("Reading from:", raw_data_path)

# Load dataset
df = pd.read_csv(raw_data_path)

# Take random 10k rows
df_small = df.sample(10000, random_state=42)

# Save smaller dataset
df_small.to_csv(output_path, index=False)

print("✅ Small dataset created successfully!")