# ======================================================================================
# Name Script     : ws_h_dice.py
# Verion Software : 0.0
# Author          : ANS
# Date            : 2021-03-28
# e-mail          : angelosan.25@gmail.com
# Verion Python   : 3.9
#
# Purpose         : Extraer data de empleos de la web Dice
#                 :
# --------------------------------------------------------------------------------------
# Version|   Fecha    | Autor            | Description Modification
# --------------------------------------------------------------------------------------
#   0    |            |                  |
#   1    |            |                  |
# ======================================================================================

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
    'https://www.dice.com/jobs?location=United%20States&latitude=37.09024&longitude=-95.712891&countryCode=US&locationPrecision=Country&radius=30&radiusUnit=mi&page=1&pageSize=100&language=en')

# LOGICA DE MAXIMA PAGINACION CON LAZO WHILE
# VECES VOY A PAGINAR HASTA UN MAXIMO DE 10
PAGINACION_MAX = 5
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
    links_productos = driver.find_elements(By.XPATH, '//a[@data-cy="card-title-link"]')
    links_de_la_pagina = []

    for a_link in links_productos:
        links_de_la_pagina.append(a_link.get_attribute("href"))

    for link in links_de_la_pagina:

        try:
            # Voy a cada uno de los links de los detalles de los productos
            driver.get(link)
            NombreEmpresa = driver.find_element(By.XPATH, '//span[contains(@id,"hiringOrganizationName")]').text
            Puesto = driver.find_element(By.XPATH, '//h1[contains(@id,"jt")]').text
            Ubicacion = driver.find_element(By.XPATH, '//li[contains(@class,"location")]').text
            sueldo = driver.find_element(By.XPATH, '//span[@class="mL20"]').text
            if sueldo == "":
                nuevosueldo = "sueldo no disponible"
            else:
                nuevosueldo = sueldo
            descripcion = driver.find_element(By.XPATH, '//div[contains(@id,"jobdescSec")]').text
            Ult_actualizacion = driver.find_element(By.XPATH, '//li[contains(@class,"posted")]').text
            # print, imprime los datos en el terminal
            lista_resultados.append(
                {
                    "empresa": NombreEmpresa,
                    "cargo": Puesto,
                    "sueldo": nuevosueldo,
                    "ubicación": Ubicacion,
                    "ultima_actualizacion": Ult_actualizacion,
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
        puedo_seguir_horizontal = driver.find_element(By.XPATH, '//a[text()="»"]')
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
df.to_csv("ws_h_dice.csv")
