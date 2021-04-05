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
    'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=Full+Stack+Developer&sc.keyword=Full+Stack+Developer&locT=N&locId=1&jobType=')

# LOGICA DE MAXIMA PAGINACION CON LAZO WHILE
# VECES VOY A PAGINAR HASTA UN MAXIMO DE 10
PAGINACION_MAX = 3
PAGINACION_ACTUAL = 1
lista_resultados = []
# Debemos darle click al boton de disclaimer para que no interrumpa nuestras acciones
#
# Mientras la pagina en la que me encuentre, sea menor que la maxima pagina que voy a sacar... sigo ejecutando...
while PAGINACION_MAX > PAGINACION_ACTUAL:
    # links_productos = driver.find_elements(By.XPATH, '//a[@class="ui-search-item_group_element ui-search-link"]')
    links_productos = driver.find_elements(By.XPATH, '//a[@data-test="job-link"]')
    print(len(links_productos))
    links_de_la_pagina = []

    for a_link in links_productos:
        links_de_la_pagina.append(a_link.get_attribute("href"))

    for link in links_de_la_pagina:

        try:
            # Voy a cada uno de los links de los detalles de los productos
            driver.get(link)
            print(link)
            sleep(3)
            mostrar_mas = driver.find_element(By.XPATH, '//div[@class="css-t3xrds ecgq1xb2"]')
            mostrar_mas.click()

            empresa = driver.find_element(By.XPATH, '//div[@class="css-16nw49e e11nt52q1"]').text
            print(empresa)
            cargo = driver.find_element(By.XPATH, '//div[@class="css-17x2pwl e11nt52q6"]').text
            print(cargo)
            ubicacion = driver.find_element(By.XPATH, '//div[@class="css-1v5elnn e11nt52q2"]').text
            print(ubicacion)
            #sueldo = driver.find_element(By.XPATH, '').text
            #print(sueldo)
            descripcion = driver.find_element(By.XPATH, '//div[@class="desc css-58vpdc ecgq1xb4"]').text
            print(descripcion)

            sleep(4)
            lista_resultados.append(
                {
                    "empresa": empresa,
                    "cargo": cargo,
                    "ubicación": ubicacion,
                    #"salario": sueldo,
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
        puedo_seguir_horizontal = driver.find_element(By.XPATH, '//a[@data-test="pagination-next"]')
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
df.to_csv("glassdoor_data.csv")
