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
    # Pre-aloquem una llista que guarda tots els accidents.
    list_accidents = []
    # Iniciliatzem variables per while loop.
    i = 1
    equal_accident = False
    if year > 2018:
        website = "https://transit.gencat.cat/ca/el_servei/premsa_i_comunicacio/" \
                  "comunicats_d_accidents_mortals/accidents-mortals-" + str(
            year) + "/"
    if year <= 2018:
        website = "https://transit.gencat.cat/ca/el_servei/premsa_i_comunicacio/" \
                  "comunicats_d_accidents_mortals/accidents_mortals_" + str(
            year) + "/"
    #Primer bucle comprova si hem arribat a la última pàgina.
    while equal_accident == False:
    #Web especifica

        page = requests.get(website, headers=headers)
        soup_general = BeautifulSoup(page.content)
        copy_list_accidents = list_accidents.copy()
        print("Scraping pàgina {}".format(i))
        #TODO: Canviar norma de break. Comprar last i seguent. Quan siguin iguals es la última iteració.
        if len(copy_list_accidents) % 15 != 0:
            print('Breaking')
            break

        for a in soup_general.find_all('a', {"class": "avoidEscapeU0023"}):
            link_accident = a['href']
            accident_i = home_web + link_accident
            page = requests.get(accident_i, headers=headers)
            soup = BeautifulSoup(page.content)
            list_strongs = soup.find_all('div', {
                "class": "basic_text_peq pd-15 link-dotted"})
            string_strongs = ''.join(str(list_strongs))
            #TODO: Quan aquests codis no funcionen, guardar URL. Sera un cas a netejar a ma.
            text_prova = string_strongs
            data = re.findall(r"(?:DIA:)(.*?)(<)", text_prova)[0][0]
            hora_avis = re.findall(r"(?:HORA D'AVÍS:)(.*?)(h)", text_prova)[0][0]
            via = re.findall(r"(?:VIA:)(.*?)(<)", text_prova)[0][0]
            info_accident = {"Data": data, "Hora_Avis": hora_avis, "Via": via}
            list_accidents.append(info_accident)



        if i != 1:
            equal_accident = info_accident == last_accident
            if equal_accident == False:
                last_accident = info_accident
            else:
                print("Pàgina repetida.")
                list_accidents = copy_list_accidents
        else:
            last_accident = info_accident
        i = i + 1
        website = home_web + soup_general.find_all('a', {"class": "seguent"})[0]['href']

    df = pd.DataFrame.from_records(list_accidents)

    return df
df = scraping(2018)

print(df)
