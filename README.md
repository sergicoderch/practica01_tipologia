# Accidents de Trànsit Mortals a Catalunya

## Descripció
El codi ha sigut desenvolupat en el marge de l'assignatura _Tipologia i cicle
de vida de les dades_ dins del màster de Ciència de Dades impartit per la UOC
en el semestre d'hivern del curs 2022-2023. 

L'objectiu de la pràctica és el de generar una eina que sigui capaç
d'aconseguir les dades d'accidents mortals a Catalunya ja sigui per motius
periodístics o d'acció sobre la xarxa viària. 

En aquesta primera pràctica es presenta la funcionalitat de _web scraping_.
## Membres del grup
Sergi Coderch Navarro i Cristian Galán Augé. Contribució equivalent per tots
dos estudiants. 

## Funcions
Dins de la carpeta Source, el lliurament incorpora un sol arxiu `main.py`, el qual incorpora les següents dues funcions:

* `scraping(year)`: Aquesta funció fa web scraping a l'any especificat
l'input `year`. Obté la pàgina de Gencat on es fan les notes de premsa i extreu
la data de l'accident, l'hora d'avís, la vía de l'accident, el dia de
publicació de la notícia així com l'hora, la URL de la notícia i el text
complert. La intenció dels últims dos camps és facilitar la neteja de dades.
Finalment, el codi retorna un _dataframe_ amb tota aquesta informació per tots
els accidents notificats per l'any especificat.

* `select_year(year1, year2)`: Permet aplicar la funció `scraping()` a un 
interval d'anys on tots dos _inputs_ són inclosos. El codi retorna un
_dataframe_ que inclou els accidents dels anys especificats.

Aquest arxiu main.py conté la opció d'executar-se a partir del `__main__`. En aquest cas, farà web scrapping des del 2014 fins al 2022, generant el dataset complet (veure l'apartat Dataset). 

**Limitacions:** Només es pot fer web scraping fins al 2014 (any inclòs) degut
a que després els accidents eren carregats en PDF.

## Dataset
El dataset obtingut d’aquesta pràctica es pot trobar en el següent enllaç de Zenodo:

https://doi.org/10.5281/zenodo.7316989 
