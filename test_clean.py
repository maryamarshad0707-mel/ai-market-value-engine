import pandas as pd
import pytest

def test_pipeline_output():
    # 1. Read the cleaned dataset
    df = pd.read_csv("cleaned_data.csv")
    
    # 2. Assert no missing values (NaNs) remain in numeric columns
    assert df['age'].isnull().sum() == 0, "Age column still has missing values!"
    assert df['salary'].isnull().sum() == 0, "Salary column still has missing values!"
    
    # 3. Assert no duplicate rows exist
    assert df.duplicated().sum() == 0, "Duplicate rows still exist!"

def test_median_imputation_values():
    df = pd.read_csv("cleaned_data.csv")
    
    # Check that Bob's missing age was correctly filled with the median (25.0)
    bob_age = df.loc[df['name'] == 'Bob', 'age'].values[0]
    assert bob_age == 25.0, f"Expected Bob's age to be 25.0, got {bob_age}"