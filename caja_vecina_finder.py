import requests

class CajaVecina:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.address = data["direccion"]
        self.number = data["numero"]
        self.distance = data["distancia"]
        self.neighborhood = data["comuna"]
    
    def __str__(self) -> str:
        return f"ID: {self.id}, Address: {self.neighborhood}, {self.address} {self.number}, Distance: {self.distance} meters"

def search_caja_vecinas(lat, lng):
    url = "https://cajavecina.gisgeoresearch.com/data_cajavecina"
    
    payload = {
        'categoria': 'CV',
        'lat': lat,
        'lng': lng,
        'servicio': '',
        'estados[]': 'CV'
    }
    
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
    }

    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        cv_list = response.json()
        return cv_list
    else:
        print(f"Error: Received status code {response.status_code}")
        return None

latitude = -33.49217279999944
longitude = -70.6052095999988
cajas_vecinas_data = search_caja_vecinas(latitude, longitude)

if cajas_vecinas_data:
    for caja_vecina_data in cajas_vecinas_data:
        caja_vecina : CajaVecina = CajaVecina(caja_vecina_data)
        print(caja_vecina)
