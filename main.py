import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep, strftime
import re
import pandas as pd


def year_select(year1: int, year2: int) -> str:
    """
    TODO: Aquesta funcio ha de permetre agafar dades de multiples anys. year1 any minim year 2 any maxim.
    :param year:
    :return:
    """

    return website

def scraping(year: str) -> pd.DataFrame:
    """

    :param website:
    :return:
    """

    # Canviem user agent.
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
    */*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "no-cache",
        "dnt": "1",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
    37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }
    # Directori principal
    home_web = "https://transit.gencat.cat"
    if year > 2018:
        website = "https://transit.gencat.cat/ca/el_servei/premsa_i_comunicacio/" \
                  "comunicats_d_accidents_mortals/accidents-mortals-" + str(
            year) + "/"
    if year <= 2018:
        website = "https://transit.gencat.cat/ca/el_servei/premsa_i_comunicacio/" \
                  "comunicats_d_accidents_mortals/accidents_mortals_" + str(
            year) + "/"

    # Pre-aloquem una llista que guarda tots els accidents.
    list_accidents = []
    # Iniciliatzem variables per while loop.
    i = 1
    # Inicialitzem a false el comparador de l'ultima pagina de l'any
    is_last_page = False

    # Guardem l'adreça de la última pagina
    page = requests.get(website, headers=headers)
    soup_general = BeautifulSoup(page.content)
    last_page = home_web + soup_general.find_all('a', {"title": "Vés a l'última pàgina"})[0]['href']
    
    #Primer bucle comprova si hem arribat a la última pàgina.
    while is_last_page == False:
        is_last_page = last_page == website
        page = requests.get(website, headers=headers)
        soup_general = BeautifulSoup(page.content)
        print("Scraping pàgina {}".format(i))
        for a in soup_general.find_all('a', {"class": "avoidEscapeU0023"}):
            link_accident = a['href']
            accident_i = home_web + link_accident
            page = requests.get(accident_i, headers=headers)
            soup = BeautifulSoup(page.content)
            
            info_noticia = soup.find_all('div', {
                "class": "basic_text_peq pd-15 link-dotted"})
            text = ''.join(str(info_noticia))
            
            text_data = re.findall(r"(?:DIA:)(.*?)(<)", text)
            text_hora_avis = re.findall(r"(?:HORA D'AVÍS:)(.*?)(h)", text)
            text_via = re.findall(r"(?:VIA:)(.*?)(<)", text)

            # Comprovem que la info de la data, hora d'avís i via estan presents a la pagina, sino guardem la URL a la data
            if text_data and text_hora_avis and text_via:
                data = text_data[0][0]
                hora_avis = text_hora_avis[0][0]
                via = text_via[0][0] 
                info_accident = {"Data_accident": data, "Hora_Avis": hora_avis, "Via": via}
            else:
                info_accident = {"Data_accident": str(accident_i)}
            
            # Detalls de publicacio
            detalls_publicacio = soup.find_all('div', {"class": "noticia_detalls_cont"})
            string_detalls_publicacio = ''.join(str(detalls_publicacio))
            data_publicacio = re.findall(r"(>)(.*?)(<)", string_detalls_publicacio)[0][1]
            hora_publicacio = re.findall(r"(>)(.*?)(<)", string_detalls_publicacio)[2][1]
            info_accident["Data_publicacio"] = data_publicacio
            info_accident["Hora_publicacio"] = hora_publicacio
            
            # Afegim tota la informacio de l'accident 
            list_accidents.append(info_accident)

        i = i + 1
        website = home_web + soup_general.find_all('a', {"class": "seguent"})[0]['href']

    df = pd.DataFrame.from_records(list_accidents)

    return df


df = scraping(2019)


print(df)
