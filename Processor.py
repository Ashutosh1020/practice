import pandas as pd
import numpy as np

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

def clean_data(df):
    # Handle missing values
    df['clearance_type'].fillna(df['clearance_type'].median(), inplace=True)
    df['zip'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['address_2'].fillna('', inplace=True)
    
    # Convert date columns to datetime
    for col in ['incident_datetime', 'created_at', 'updated_at']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Combine address columns
    df['full_address'] = df['address_1'] + ', ' + df['address_2'].fillna('')
    
    return df

def generate_summary(df):
    summary = {
        'total_incidents': len(df),
        'most_common_incident': df['incident_type_primary'].mode()[0],
        'peak_hour': df['hour_of_day'].value_counts().idxmax(),
        'peak_day': df['day_of_week'].value_counts().idxmax()
    }
    return summary

def incidents_by_category(df):
    return df['incident_type_primary'].value_counts()

def incidents_by_time(df):
    hourly = df.groupby('hour_of_day').size()
    daily = df.groupby('day_of_week').size()
    return hourly, daily