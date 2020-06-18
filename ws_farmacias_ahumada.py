# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 08:37:14 2019

@author: jmunozu
"""

#acá enviamos nuestro contenido por POST

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from pandas import DataFrame



def fecha_actual_txt():
    now = datetime.now()
    # dd/mm/YY H:M:S
    #dt_string = now.strftime("%d/%m/%Y_%H:%M:%S")
    dt_string = now.strftime("%d_%m_%Y")
    return(dt_string)

###
### Vamos a iniciar una sesión
###

cat = ["BEBE","BELLEZA","CONSUMO Y MERCADERIAS GENERALES","CUIDADO PERSONAL","FARMACIA OTC","FARMACIA RX"]
fecha = datetime.today()

tit_eleme = []
precio_eleme = []
sku_eleme = []
cat_eleme = []
fecha_eleme = []
pag_ = []

for cat_i in cat:
    session = requests.session()
    url = 'https://www.farmaciasahumada.cl/catalogo-productos/'
    myobj = {'buscarproducto': '', 'filter_categories[]': cat_i}
   
    s = session.post(url,myobj)
   
    print(s.cookies.get_dict())
   
    s = session.get('https://www.farmaciasahumada.cl/catalogo-productos/?cpage=1')
   
   
    bs = BeautifulSoup(s.text, 'html.parser')
   
    #reconocemos cuántas pags tiene esta coseque
   
    paginas = []
    for pags in bs.findAll("div", {"class": "pagination"})[0].findAll("a", {"class": "page-numbers"}):
        if pags.text.find("«") == -1 and pags.text.find("»") == -1:
            paginas.append(int(pags.text))
     
    max_pag = max(paginas)
    flag = 1
    pag = 1

    while (flag == 1):
        if pag == max_pag:
            s = session.get('https://www.farmaciasahumada.cl/catalogo-productos/?cpage=' + str(pag))
        #Itero sobre los elementos
            bs = BeautifulSoup(s.text, 'html.parser')
            for producto in bs.findAll("p", {"class": "n-gnc-bajada-pro-new"}):
                tit_eleme.append(producto.findAll("span", {"class": "t-com"})[0].text)
                precio_eleme.append(producto.findAll("span", {"class": "n-gnc-bajada-precio-new"})[0].text)
                sku_eleme.append(producto.text[producto.text.find("Sku: "):producto.text.find("$")])
                cat_eleme.append(cat_i)
                fecha_eleme.append(fecha)
                pag_.append('https://www.farmaciasahumada.cl/catalogo-productos/?cpage=' + str(pag))
               
            time.sleep(1.2)
            s.cookies.clear()
            flag = 0
            print("Categoría: " + str(cat_i) + "\n")
            print("Página: " + str(pag))
        else:
            
            s = session.get('https://www.farmaciasahumada.cl/catalogo-productos/?cpage=' + str(pag))
            bs = BeautifulSoup(s.text, 'html.parser')
            for producto in bs.findAll("p", {"class": "n-gnc-bajada-pro-new"}):
                tit_eleme.append(producto.findAll("span", {"class": "t-com"})[0].text)
                precio_eleme.append(producto.findAll("span", {"class": "n-gnc-bajada-precio-new"})[0].text)
                sku_eleme.append(producto.text[producto.text.find("Sku: "):producto.text.find("$")])
                cat_eleme.append(cat_i)
                fecha_eleme.append(fecha)
                pag_.append('https://www.farmaciasahumada.cl/catalogo-productos/?cpage=' + str(pag))
            time.sleep(1.2)
            print("Categoría: " + str(cat_i) + "\n")
            print("Página: " + str(pag))
            pag = pag + 1
        
        
       
#escrapee todo, guardo la pag
base = {'tit_pro' : tit_eleme, 'precio' : precio_eleme, 'sku' : sku_eleme , 'categoria' : cat_eleme , 'Fecha' : fecha_eleme, 'URL': pag_}
df = DataFrame(base, columns=['tit_pro','precio','sku','categoria','Fecha', 'URL'])
df.to_csv("C:\\webscrapping\\base_ahumada_" + str(fecha_actual_txt()) + "_.csv", index = None, header=True, encoding="utf-8") 







