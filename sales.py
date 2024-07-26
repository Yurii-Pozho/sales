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
    # Переконаємося, що description - це рядок
    description = str(description)
    match = re.search(r'(\d{4})\.', description)
    return match.group(1) if match else None

# Відповідність номерів карт і їх назв
card_names = {
    '4958': 'Хомик М ПДП', '6026': 'Хомик М Унів', '1725': 'Хомик М МОНО',
    '7731': 'Хомик М USD', '1632': 'Токар О ПДП', '2202': 'Токар О Унів',
    '9359': 'Видиш ПДП', '6141': 'Видиш Унів', '5733': 'Видиш МОНО',
    '4408': 'Видиш USD', '8954': 'Хомик Д ПДП', '5014': 'Хомик Д Унів',
    '4974': 'Хомик Д USD', '6597': 'Хомик Р ПДП', '6091': 'Хомик Р Унів',
    '1020': 'Хомик Р МОНО', '8358': 'Хомик Р USD', '7902': 'Сакалош ПДП',
    '1120': 'Сакалош Унів', '8351': 'Сакалош USD', '3759': 'Шароді ПДП',
    '9935': 'Шароді Унів', '6186': 'Шароді USD', '0025': 'Опанасенко ПДП',
    '3232': 'Опанасенко Унів', '6411': 'Опанасенко USD', '3804': 'Свіца ПДП',
    '4792': 'Свіца Унів', '3853': 'Свіца USD', '0906': 'Варчук ПДП',
    '9740': 'Варчук Унів', '8506': 'Варчук USD'
}

pd.set_option('display.max_colwidth', None)

upload_file = st.file_uploader("Оберіть файл Excel", type=['xlsx'])

if upload_file:   
    data = pd.read_excel(upload_file)
    
    # Перевірка перших кількох рядків даних
    st.write("Початкові дані:")
    st.dataframe(data.head())

    data = data.rename(columns={'Unnamed: 2': 'Describe', 'Unnamed: 5': 'Credits'})
    data = data.drop([0, 1]).reset_index(drop=True)    
    data['Credits'] = data['Credits'].apply(clean)
    data['Bank_acount'] = data['Describe'].apply(extract_digit)

    # Додавання стовпця з назвами карт
    data['Card_Name'] = data['Bank_acount'].map(card_names)
    data['Card_Name'] = data['Card_Name'].fillna('<span style="color:red; font-weight:bold;">ФОП не вказаний</span>')

    # Перевірка даних після додавання назв карт
    st.write("Дані після додавання назв карт:")
    st.dataframe(data.head())

    # Фільтруємо дані, щоб залишити лише ті, які мають значення у 'Bank_acount'
    filtered_data = data[data['Bank_acount'].notna()]
    
    # Обираємо потрібні стовпці для виведення результатів
    result_data = filtered_data[['Bank_acount', 'Card_Name', 'Credits']]
    
    # Форматуємо стовпець 'Credits' жирним шрифтом
    result_data['Credits'] = result_data['Credits'].apply(lambda x: f'<b>{x}</b>')

    # Створюємо зведену таблицю
    table = result_data.pivot_table('Credits', ['Bank_acount', 'Card_Name'], aggfunc='sum')

    # Запит користувача для вибору стовпця для сортування
    sort_column = st.selectbox(
        'Виберіть стовпець для сортування',
        ['Bank_acount', 'Card_Name']
    )

    # Сортування даних
    sorted_table = table.reset_index().sort_values(by=sort_column)
    sorted_table = sorted_table.set_index(['Bank_acount', 'Card_Name'])
    
    # Виводимо таблицю з форматуванням HTML
    st.write('Результат обробки даних')

    # Зміна форматування HTML для DataFrame
    table_html = sorted_table.to_html(escape=False)
    
    # Замінюємо "ФОП не вказаний" на форматований текст
    table_html = table_html.replace(
        '<td>ФОП не вказаний</td>',
        '<td><span style="color:red; font-weight:bold;">ФОП не вказаний</span></td>'
    )
    
    # Вставляємо жирний шрифт для Credits
    table_html = table_html.replace(
        '<td>',
        '<td><b>'
    ).replace(
        '</td>',
        '</b></td>'
    )
    
    st.markdown(table_html, unsafe_allow_html=True)
