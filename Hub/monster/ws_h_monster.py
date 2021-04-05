from random import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
from numpy.distutils.fcompiler import none
import requests
# Definimos el User Agent en Selenium utilizando la clase Options
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome('chromedriver.exe', chrome_options=opts)  # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

def getScrollingScript(iteration):
    # Script de scrolling es un script de javascript. Le hago scroll a un contenedor que contenta ciertas clases
    # Estas clases dependen de mi extraccion. Existen otras maneras de hacer scrolling que veremos en el NIVEL EXTRA.
    scrollingScript = """ 
      document.getElementsByClassName('results-list split-screen-mode')[0].scroll(0, 200000)
    """
    return scrollingScript.replace('200000', str(200000 * (iteration + 1)))

# URL SEMILLA
driver.get(
    'https://www.monster.com/jobs/search/?q=Full-Stack-Developer&where=USA')
sleep(5)
# Logica de Scrolling
SCROLLS = 0
while (SCROLLS != 3): # Decido que voy a hacer 3 scrollings
  driver.execute_script(getScrollingScript(SCROLLS)) # Ejecuto el script para hacer scrolling del contenedor
  sleep(random.uniform(4, 5)) # Entre cada scrolling espero un tiempo
  SCROLLS += 1
lista_resultados = []
# Debemos darle click al boton de disclaimer para que no interrumpa nuestras acciones

    # links_productos = driver.find_elements(By.XPATH, '//a[@class="ui-search-item_group_element ui-search-link"]')
    links_productos = driver.find_elements(By.XPATH, '//div[@class="results-card "]')
    print(len(links_productos))
    links_de_la_pagina = []

    for a_link in links_productos:
        links_de_la_pagina.append(a_link.get_attribute("href"))

    for link in links_de_la_pagina:
        r=link.replace('#', '')
        rr="https://www.monster.com/job-openings/"

        driver.get(rr+r)
        sleep(3)
        print(rr+r)
PAGINACION_ACTUAL+=1
