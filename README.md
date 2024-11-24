# Buscador Cajas Vecinas
Wrapper de ```https://cajavecina.gisgeoresearch.com/``` para la obtención de ```Cajas Vecinas```

## coordinates_finder.py
```search_coordinates(address : str)```: Retorna las coordenadas ```(lat, lng)``` a partir de la dirección entregada

## caja_vecina_finder.py
1. ```search_caja_vecinas(lat, lng)```: Retorna listado completo de ```Cajas Vecinas``` cercanas a partir de coordenadas
2. ```search_ATM(lat, lng)```: Retorna listado completo de ```Cajeros``` cercanas a partir de coordenadas
3. ```search_cajas_vecinas_and_ATM(lat, lng)```: Retorna listado completo de ```Cajas Vecinas``` y ```Cajeros``` cercanos a partir de coordenadas

## get_nearest_cajas_vecinas.py
```find_nearest_cajas_vecinas(address : str)```: A partir de una dirección, entrega listado de ```Cajas Vecinas```

# Clases
```
class BancoEstadoEntity:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.address = data["direccion"]
        self.number = data["numero"]
        self.distance = float(data["distancia"])
        self.neighborhood = data["comuna"]
        self.accessibility = data["accesibilidad"]

    def get_speech_text(self):
        pass

class CajaVecina(BancoEstadoEntity):
    def __init__(self, data) -> None:
        super().__init__(data)
    
    def get_speech_text(self):
        speech_text = f"Caja Vecina"
        if self.accessibility:
            speech_text += " accesible"
        speech_text += f" en {self.neighborhood}, {self.address} {self.number}. Distancia: {int(self.distance)} metros."
        return speech_text

class ATM(BancoEstadoEntity):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.audible = data["audible"]
    
    def get_speech_text(self):
        speech_text = f"Cajero"
        if self.accessibility and self.audible:
            speech_text += " audible y accesible"
        elif self.accessibility:
            speech_text += " accesible"
        elif self.audible:
            speech_text += " audible"
        speech_text += f" en {self.neighborhood}, {self.address} {self.number}. Distancia: {int(self.distance)} metros."
        return speech_text
```

## Requisitos
Librerias requeridas:
* ```requests```
* ```pyproj```


Se instalan mediante

```pip install requests pyproj```