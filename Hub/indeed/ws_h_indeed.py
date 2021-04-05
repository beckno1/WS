# ======================================================================================
# Name Script     : ws_h_indeed.py
# Verion Software : 0.0
# Author          : ANS
# Date            : 2021-03-29
# e-mail          : angelosan.25@gmail.com
# Verion Python   : 3.9
#
# Purpose         : Extraer data de empleos de la web indeed
#                 :
# --------------------------------------------------------------------------------------
# Version|   Fecha    | Autor            | Description Modification
# --------------------------------------------------------------------------------------
#   0    |            |                  |
#   1    |            |                  |
# ======================================================================================
# 

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

# URL SEMILLA
driver.get(
    'https://mx.indeed.com/trabajo?q=IT+sistemas&from=mobRdr&utm_source=%2Fm%2F&utm_medium=redir&utm_campaign=dt')

# LOGICA DE MAXIMA PAGINACION CON LAZO WHILE
# VECES VOY A PAGINAR HASTA UN MAXIMO DE 10
PAGINACION_MAX = 20
PAGINACION_ACTUAL = 1
lista_resultados = []


# Debemos darle click al boton de disclaimer para que no interrumpa nuestras acciones
try:  # Encerramos todo en un try catch para que si no aparece el discilamer, no se caiga el codigo
    disclaimer = driver.find_element(By.XPATH, '//button[@id="cookieDisclaimerButton"]')
    disclaimer.click()  # lo obtenemos y le damos click
except Exception as e:
    print(e)
    None
# Mientras la pagina en la que me encuentre, sea menor que la maxima pagina que voy a sacar... sigo ejecutando...
while PAGINACION_MAX > PAGINACION_ACTUAL:
    # links_productos = driver.find_elements(By.XPATH, '//a[@class="ui-search-item_group_element ui-search-link"]')
    links_productos = driver.find_elements(By.XPATH, '//a[@class="jobtitle turnstileLink "]')
    print(len(links_productos))
    links_de_la_pagina = []

    for a_link in links_productos:
        links_de_la_pagina.append(a_link.get_attribute("href"))

    for link in links_de_la_pagina:

        try:
            # Voy a cada uno de los links de los detalles de los productos
            driver.get(link)
            print(link)

            empresa = driver.find_element(By.XPATH,'//div[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]').text

            cargo = driver.find_element(By.XPATH,'//h1[@class="icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"]').text

            ubicacion=driver.find_element(By.XPATH,'//*[@id="viewJobSSRRoot"]/div[1]/div[3]/div[1]/div[2]/div/div/div[2]').text

            descripcion=driver.find_element(By.XPATH,'//div[@class="jobsearch-jobDescriptionText"]').text

            sleep(4)
            lista_resultados.append(
                {
                    "empresa": empresa,
                    "cargo": cargo,
                    "ubicación": ubicacion,
                    "detalles": descripcion
                }

            )

            driver.back()
        except Exception as e:
            print(e)
            # Si sucede algun error dentro del detalle, no me complico. Regreso a la lista y sigo con otro producto.
            driver.back()
    try:
        # Intento obtener el boton de SIGUIENTE y le intento dar click
        puedo_seguir_horizontal = driver.find_element(By.XPATH, '//span[@class="np"]')
        puedo_seguir_horizontal.click()
    except:
        # Si obtengo un error al intentar darle click al boton, quiere decir que no existe
        # Lo cual me indica que ya no puedo seguir paginando, por ende rompo el While
        # print("No encuetro el clic a la siguiente pestaña")
        # print (puedo_seguir_horizontal)
        break
PAGINACION_ACTUAL += 1

df = pd.DataFrame(lista_resultados)
print(df)
df.to_csv("ws_h_indeed.csv")

