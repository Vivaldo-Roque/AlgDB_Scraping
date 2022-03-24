"""
Author: Vivaldo Roque
Date: 23-03-2022

Description: Scraping script for algdb.net
"""

# 1. Pegar conteúdo HTML a partir da URL
# 2. Parsear o conteúdo HTML - BeautifulSoup
# 3. Estruturar conteúdo em um Data Frame - Pandas
# 4. Transformar os Dados em um Dicionário de dados próprio
# 5. Converter e salvar em um arquivo JSON

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json

# Lista dos endereços onde se localizam as tabelas que eu preciso

urls = [
    {"F2L" : "http://algdb.net/puzzle/333/f2l"},
    {"OLL" : "http://algdb.net/puzzle/333/oll"},
    {"PLL" : "http://algdb.net/puzzle/333/pll"},
    {"COLL" : "http://algdb.net/puzzle/333/coll"},
    {"WV" : "http://algdb.net/puzzle/333/wv-wvls"}
]


# caminho da tabela na pagina web em questão
xpath = "//div[@class='row-border hover table-container']//table"

# Configurações, estou usando o Chrome você pode usar o firefox se quiser

'''
option = webdriver.FirefoxOptions()
option.headless = True
driver = webdriver.Firefox(options=option)
'''

option = webdriver.ChromeOptions()
option.headless = True # Trabalhar no background
driver = webdriver.Chrome(options=option)

# Dicionário principal

algsList = {}

# Percorrer os dicionário da lista urls

for dic in urls:

    # Percorrer cada key e value presente nos dicionários
    for caseKey, url in dic.items():

        # Adicionar lista vazia com a chave do submétodo
        algsList[caseKey] = []

        # Carrega a pagina web na sessão ativa
        driver.get(url)

        delay = 10 # segundos
        try:
            # Aguardar saber se o elemento existe com um atraso de 5 segundos antes do tempo expirar
            element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            # Pegar o código HTML do elemento caso exista
            html_content = element.get_attribute('outerHTML')

            # Responsável por fazer a conversão do conteúdo HTML para extração
            soup = BeautifulSoup(html_content, 'html.parser')

            # Procurar por tabela nessa extração
            table = soup.find(name='table')

            # Pegar o primeira ocorrência
            df_full = pd.read_html(str(table))[0]

            # Quais columas pegar
            df = df_full[['Case', 'Algs']]

            # Mudar nome das colunas
            df.columns = ['Case', 'Algs']

            # Dicionário onde salvar os submétodos
            submethod = {}

            submethod = df.to_dict('records')

            # Dicionário auxiliar
            temp = {}

            # Converter a columa Algs que esta em string para list
            for case in submethod:
                for key in case:
                    if key == "Algs":
                        temp[key] = case[key].split("  ")
                    else:
                        temp[key] = case[key]
                
                # Adicionar cada dicionário do submethod em algsList tendo em conta o submétodo em questão
                algsList[caseKey].append(temp)
                temp = {}

        except TimeoutException:
            print ("Loading took too much time!")

# Sair do navegador
driver.quit()
# Converter dicionário em JSON
js = json.dumps(algsList)
# Abrir / criar um ficheiro
fp = open('algdb.json', 'w')
# Escrever nele
fp.write(js)
# Fechar
fp.close()
