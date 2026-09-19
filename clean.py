import pandas as pd

# 1. Load raw CSV data into a Pandas DataFrame
print("--- Loading Raw Data ---")
df = pd.read_csv("raw_data.csv")
print(df)

# 2. Remove exact duplicate rows
df = df.drop_duplicates()

# 3. Fill missing numeric values (NaNs) using median values
df['age'] = df['age'].fillna(df['age'].median())
df['salary'] = df['salary'].fillna(df['salary'].median())

# 4. Save the cleaned DataFrame to a new file
df.to_csv("cleaned_data.csv", index=False)

print("\n--- Pipeline Complete! Cleaned Data Saved to cleaned_data.csv ---")
print(df)

