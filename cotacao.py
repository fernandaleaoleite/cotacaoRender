from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import psycopg2
from time import sleep

def salvar_dolar():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.google.com/search?q=valor+atual+do+dolar")
    sleep(0.1)  

    dolar_element = driver.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]')
    dolar = dolar_element.text.replace(",", ".")  
    driver.quit()  

    data_e_hora_atual = datetime.now()
    data = data_e_hora_atual.strftime('%Y-%m-%d')  
    hora = data_e_hora_atual.strftime('%H:%M:%S')  

    conexao = psycopg2.connect(
        dbname='dbCotacoes', 
        user='postgres', 
        password='1234', 
        host='localhost', 
        port='5432'
    )
    cursor = conexao.cursor()

    cursor.execute("CALL inserir_cotacao_dolar(%s, %s, %s)", (data, hora, float(dolar)))
    conexao.commit() 

    cursor.close()
    conexao.close()

salvar_dolar()
