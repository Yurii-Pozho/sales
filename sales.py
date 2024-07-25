import pandas as pd
import re
import streamlit as st

def clean(value):
    value = re.sub(r'[^\d\.,-]', '', str(value))
    value = value.replace(',', '.')
    try:
        result = float(value)
        return abs(int(result))
    except ValueError:
        return 0 

def extract_digit(description):
    match = re.search(r'(\d{4})\.', description)
    return match.group(1) if match else None
pd.set_option('display.max_colwidth', None)

st.title =('Аналіз даних платіжної системи')

upload_file = st.file_uploader("Оберіть файл Excel",type=['xlsx'])

if upload_file:   
    data = pd.read_excel(upload_file)
    data = data.rename(columns={'Unnamed: 2':'Describe','Unnamed: 5': 'Credits'})
    data = data.drop([0,1]).reset_index(drop=True)    
    data['Credits'] = data['Credits'].apply(clean)
    data['Bank_acount'] = data['Describe'].apply(extract_digit)
    filtered_data = data[data['Bank_acount'].notna()]
    result_data = filtered_data[['Bank_acount','Credits']]
    table = result_data.pivot_table('Credits','Bank_acount',aggfunc='sum')
#
    st.write('Результат обробки даних')
    st.dataframe(table)