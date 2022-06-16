"""
Author: Vivaldo Roque
Date: 23-03-2022

Description: This script collects only 3x3x3 data referring to F2L, OLL, PLL, COLL and WV from the site ==> [http://algdb.net/] and saves it in a file in json format.
"""
# Português 
# 1. Pegar conteúdo HTML a partir da URL
# 2. Parsear o conteúdo HTML - BeautifulSoup
# 3. Estruturar conteúdo em um Data Frame - Pandas
# 4. Transformar os Dados em um Dicionário de dados próprio
# 5. Converter e salvar em um arquivo JSON

# English
# 1. Get HTML content from URL
# 2. Parse HTML Content - BeautifulSoup
# 3. Structuring Content in a Data Frame - Pandas
# 4. Transform the Data into a Data Dictionary of its own
# 5. Convert and save to a JSON file

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json

# Português 
# Lista dos endereços onde se localizam as tabelas que eu preciso
# English
# List of addresses where the tables I need are located

urls = [
    {"F2L" : "http://algdb.net/puzzle/333/f2l"},
    {"OLL" : "http://algdb.net/puzzle/333/oll"},
    {"PLL" : "http://algdb.net/puzzle/333/pll"},
    {"COLL" : "http://algdb.net/puzzle/333/coll"},
    {"WV" : "http://algdb.net/puzzle/333/wv-wvls"}
]

# Português 
# Caminho da tabela na pagina web em questão
# English
# Table path on the web page in question
xpath = "//div[@class='row-border hover table-container']//table"

# Português 
# Configurações, estou usando o Chrome você pode usar o firefox se quiser
# English
# Settings, I'm using Chrome you can use firefox if you want

'''
option = webdriver.FirefoxOptions()
option.headless = True
driver = webdriver.Firefox(options=option)
'''

option = webdriver.ChromeOptions()
# Português 
# Trabalhar no background
# English
# Work in the background
option.headless = True 
driver = webdriver.Chrome(options=option)

# Português 
# Dicionário principal
# English
# Main dictionary

algsList = {}

# Português 
# Percorrer os dicionário da lista urls
# English
# Cycle through the urls list dictionaries

for dic in urls:

    # Português 
    # Percorrer cada key e value presente nos dicionários
    # English
    # Cycle through each key and value present in the dictionaries
    for caseKey, url in dic.items():

        # Português 
        # Adicionar lista vazia com a chave do submétodo
        # English
        # Add empty list with submethod key
        algsList[caseKey] = []

        # Português 
        # Carrega a pagina web na sessão ativa
        # English
        # Load the web page in the active session
        driver.get(url)
        
        # Português 
        # segundos
        # English
        # Seconds
        delay = 10 
        try:
            # Português 
            # Aguardar saber se o elemento existe com um atraso de 5 segundos antes do tempo expirar
            # English
            # Wait to know if element exists with a delay of 5 seconds before time expires
            element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            # Português 
            # Pegar o código HTML do elemento caso exista
            # English
            # Get the element's HTML code if it exists
            html_content = element.get_attribute('outerHTML')

            # Português 
            # Responsável por fazer a conversão do conteúdo HTML para extração
            # English
            # Responsible for converting HTML content for extraction
            soup = BeautifulSoup(html_content, 'html.parser')

            # Português 
            # Procurar por tabela nessa extração
            # English
            # Search for table in this extract
            table = soup.find(name='table')

            # Português 
            # Pegar o primeira ocorrência
            # English
            # Get the first occurrence
            df_full = pd.read_html(str(table))[0]

            # Português 
            # Quais colunas pegar
            # English
            # Which columns to get
            df = df_full[['Case', 'Algs']]

            # Português 
            # Mudar nome das colunas
            # English
            # Rename columns
            df.columns = ['Case', 'Algs']

            # Português 
            # Dicionário onde salvar os submétodos
            # English
            # Dictionary where to save submethods
            submethod = {}

            submethod = df.to_dict('records')

            # Português 
            # Dicionário auxiliar
            # English
            # Auxiliary dictionary
            temp = {}

            # Português 
            # Converter a columa Algs que esta em string para list
            # English
            # Convert the column Something that is in string to list
            for case in submethod:
                for key in case:
                    if key == "Algs":
                        temp[key] = case[key].split("  ")
                    else:
                        temp[key] = case[key]
                
                # Português 
                # Adicionar cada dicionário do submethod em algsList tendo em conta o submétodo em questão
                # English
                # Add each submethod dictionary into algsList taking into account the submethod in question
                algsList[caseKey].append(temp)
                temp = {}

        except TimeoutException:
            print ("Loading took too much time!")

# Português 
# Sair do navegador
# English
# Exit browser
driver.quit()
# Português 
# Converter dicionário em JSON
# English
# Convert dictionary to JSON
js = json.dumps(algsList)
# Português 
# Abrir / criar um ficheiro
# English
# Open / create a file
fp = open('algdb.json', 'w')
# Português 
# Escrever nele
# English
# write on it
fp.write(js)
# Português 
# Fechar
# English
# Close
fp.close()
