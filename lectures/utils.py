import pandas as pd

def get_df_focused_crimes():
    df = pd.read_csv('../res/focus_crimes_SF_2003_present.csv')
    df['FullDate'] = pd.to_datetime(df['FullDate'])
    return df

def get_df_all_crimes():
    df = pd.read_csv('../res/all_crimes_sf_203_present.csv.csv')
    df['FullDate'] = pd.to_datetime(df['FullDate'])
    return df