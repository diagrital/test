import streamlit as st
import pandas as pd
import os

folder_path = st.text_input("Enter the folder path:")

if folder_path:
    file_names = []
    dfs = []
    for file in os.listdir(f"r{folder_path}"):
        if file.endswith(".xlsx") or file.endswith(".xls"):
            file_names.append(file)
            df = pd.read_excel(os.path.join(f"r{folder_path, file}"))
            pulse_value = st.sidebar.selectbox("Select pulse", [0,1,2,3,4,5], index=0)
            pulse_value_2 = st.sidebar.selectbox("Select pulse 2",[0,1,2,3,4,5],index = 0)
            df = df[(df['Pulse'] == pulse_value) | (df['Pulse'] == pulse_value_2)]
            df = df[["Name", "Phone Number", "Speaker",'Pulse']]
            df['Speaker'] = df['Speaker'].replace(['Yes','No'], [1,0])
            df = df[["Name", "Phone Number", "Speaker"]].reset_index(drop = True)
            dfs.append(df)
    
    if dfs:
        @st.experimental_memo
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')
        
        csvs = [convert_df(df) for df in dfs]
        for file_name, csv in zip(file_names, csvs):
            st.download_button(f"Download {file_name}", csv, f"{file_name}_transformed.csv","text/csv")
