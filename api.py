import requests
import pandas as pd
import io
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from api_key import key


def build_query(start_value):
    query = '("chat bot" OR "conversational agent" OR chatbot OR "dialogue agent" ) AND ( "design theory" OR "design science" OR "design principles" OR "designing")'
    url = f'http://api.springernature.com/meta/v2/pam?q=({query})&p=100&s={start_value}&api_key={key}'
    return url

def get_result_xml(start_value):
        r = requests.get(build_query(start_value))
        print(r.text)
        return r.text

def xml_to_df(xml_data):
    root = ET.fromstring(xml_data)

    # Namespaces definieren
    namespaces = {
        'pam': 'http://prismstandard.org/namespaces/pam/2.2/',
        'prism': 'http://prismstandard.org/namespaces/basic/2.2/',
        'xhtml': 'http://www.w3.org/1999/xhtml',
        'dc': 'http://purl.org/dc/elements/1.1/',
    }

    # Listen für die Daten erstellen
    years = []
    authors = []
    titles = []
    abstracts = []
    dois = []
    keywords = []

    # Alle 'record'-Elemente durchgehen
    for record in root.findall('.//record'):
        year_element = record.find('.//prism:publicationDate', namespaces=namespaces)
        year = year_element.text if year_element is not None else None

        author_elements = record.findall('.//dc:creator', namespaces=namespaces)
        author_list = [author.text for author in author_elements] if author_elements is not None else []

        title_element = record.find('.//dc:title', namespaces=namespaces)
        title = title_element.text if title_element is not None else None

        abstract_element = record.find('.//xhtml:p', namespaces=namespaces)
        abstract = abstract_element.text if abstract_element is not None else None

        doi_element = record.find('.//prism:doi', namespaces=namespaces)
        doi = doi_element.text if doi_element is not None else None

        keyword_elements = record.findall('.//prism:keyword', namespaces=namespaces)
        keyword_list = [keyword.text for keyword in keyword_elements] if keyword_elements is not None else []

        years.append(year)
        authors.append(author_list)
        titles.append(title)
        abstracts.append(abstract)
        dois.append(doi)
        keywords.append(keyword_list)


    # DataFrame erstellen
    df = pd.DataFrame({
        'Year': years,
        'Authors': authors,
        'Title': titles,
        'Abstract': abstracts,
        'DOI': dois,
        'Keywords': keywords
    })

    # DataFrame anzeigen
    print(df)
    return df

def append_dataframes(df1, df2):
    if df1.empty:
        return df2
    elif df2.empty:
        return df1
    else:
        return pd.concat([df1, df2], ignore_index=True)

import pandas as pd

def filter_dataframe(df, column_names, phrases1, phrases2):
    combined_mask = None

    for column_name in column_names:
        mask1 = df[column_name].str.contains('|'.join(phrases1), case=False)
        mask2 = df[column_name].str.contains('|'.join(phrases2), case=False)
        
        # Combine the masks using logical OR (|) for each list of phrases
        column_mask = mask1 & mask2
        
        if combined_mask is None:
            combined_mask = column_mask
        else:
            combined_mask |= column_mask

    # Filter the DataFrame based on the combined mask
    filtered_df = df[combined_mask]

    return filtered_df

num_result = 13764
i=0
combined_df = pd.DataFrame()

for i in range(0, num_result, 100):
    xml_result = get_result_xml(i)
    print("i= " + str(i))
    df = xml_to_df(xml_result)
    combined_df = append_dataframes(combined_df, df)


phrases1 = ["chat bot", "conversational agent", "chatbot", "dialogue agent"]
phrases2 = ["design theory", "design science", "design principles", "designing"]

filtered_result = filter_dataframe(combined_df, ['Abstract', 'Title', 'Keywords'], phrases1, phrases2)

filtered_result.to_csv('your_file_name.csv', index=False)