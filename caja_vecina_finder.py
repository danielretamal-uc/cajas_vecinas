import requests

class BancoEstadoEntity:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.address = data["direccion"]
        self.number = data["numero"] if data["numero"] else ""
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

def search_banco_estado_entity(lat, lng, category):
    url = "https://cajavecina.gisgeoresearch.com/data_cajavecina"
    
    payload = {
        'categoria': category,
        'lat': lat,
        'lng': lng,
        'servicio': '',
        'estados[]': category
    }
    
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
    }

    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        entity_list = response.json()
        return entity_list
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

def search_cajas_vecinas(lat, lng):
    return search_banco_estado_entity(lat, lng, 'CV')

def search_ATM(lat, lng):
    return search_banco_estado_entity(lat, lng, 'ATM')

def search_cajas_vecinas_and_ATM(lat, lng):
    entities = []
    cajas_vecinas_data = search_cajas_vecinas(lat, lng)
    if cajas_vecinas_data:
        entities.extend([CajaVecina(data) for data in cajas_vecinas_data])

    atms_data = search_ATM(lat, lng)
    if atms_data:
        entities.extend([ATM(data) for data in atms_data])
    
    return sorted(entities, key=lambda x: x.distance)

if __name__ == "__main__":
    latitude = -33.43886093844669
    longitude = -70.55856928189903
    cajas_vecinas_data = search_cajas_vecinas(latitude, longitude)
    
    max_count = 3
    if cajas_vecinas_data:
        for i in range(len(cajas_vecinas_data)):
            if i >= max_count: break
            caja_vecina : CajaVecina = CajaVecina(cajas_vecinas_data[i])
            print(caja_vecina.get_speech_text())
