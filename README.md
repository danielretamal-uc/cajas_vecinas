# Buscador Cajas Vecinas
Wrapper de ```https://cajavecina.gisgeoresearch.com/``` para la obtención de ```Cajas Vecinas```

## coordinates_finder.py
```search_coordinates(address : str)```: Retorna las coordenadas ```(lat, lng)``` a partir de la dirección entregada

## caja_vecina_finder.py
```search_caja_vecinas(lat, lng)```: Retorna listado completo de ```Cajas Vecinas``` cercanas a partir de coordenadas

## get_nearest_cajas_vecinas.py
```find_nearest_cajas_vecinas(address : str)```: A partir de una dirección, entrega listado de ```Cajas Vecinas```