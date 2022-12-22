#!/usr/bin/env python
# coding: utf-8


# para criar o arquivo de libs 

from selenium import webdriver
from time import sleep, time

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pdfkit


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('http://portal.pucminas.br/biblioteca/index_padrao.php')

# Realizar a pesquisa digitando o termo desejado
driver.find_element(By.ID, 'searchboxholdingsid').send_keys('Teste de Software')

wait = WebDriverWait(driver, 10)

original_window = driver.current_window_handle

assert len(driver.window_handles) == 1

#clicar no botao
driver.find_element(By.CSS_SELECTOR, '#searchformholdingsid button.botao-padrao').click()

# Identificar quantas abas estão abertas e saber qual é para está usando
wait.until(EC.number_of_windows_to_be(2))

# Declaração das variáveis necssárias para o fluxo do programa
i = 1
qtde_books = 0
info = ["<!DOCTYPE html><html><head><style>table, th, td {border: 1px solid black;}table {width: 100%;}</style></head><body><h2>Relatorio de livros no acervo da PUCMINAS</h2><table><tr><th>TITULO</th><th>LINK</th></tr>"]

# saber qual tela é para está usando
for window_handle in driver.window_handles:
    if window_handle != original_window:
        driver.switch_to.window(window_handle)
        break

# Condicional para realizar a paginação
while i <= 5:

    # Seleciono todos os elementos que possuem a class result-list-li
    books = wait.until(lambda driver: driver.find_elements(By.CSS_SELECTOR, 'li.result-list-li'))

    for book in books:
        # Está sendo feito a contagem de livros lidos
        qtde_books = qtde_books + 1

        # O elemento `a` com a class selector `book-title`
        # contém todas as informações que queremos mostrar
        book_title = book.find_element(By.CSS_SELECTOR, 'a.title-link')

        # `get_attribute` serve para extrair qualquer atributo do elemento
        book_link = book_title.get_attribute('href')

        # Concatenar informações
        s = "<tr><td>" + book_title.text + "</td><td><a href='" + book_link + "'>" + book_link + "</a></td></tr>"
        
        info.append(s)
    
    # Clica no botão de 'próximo' para seguir para a próxima página da paginação 
    driver.find_element(By.ID, 'ctl00_ctl00_MainContentArea_MainContentArea_bottomMultiPage_lnkNext').click()

    # Incrementando o valor do while para continuar seguindo na paginação
    i = i + 1

    WebDriverWait(driver, 10)


# Finalizado a concatenação dos dados
info.append("</table><br/>TOTAL DE LIVROS: " + str(qtde_books) + "</body></html>")

# Gerar o PDF com os dados coletados
pdfkit.from_string(str(info), "relatorio.pdf")

# Fechar navegador
driver.quit()



