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

if __name__ == "__main__":
    latitude = -33.43886093844669
    longitude = -70.55856928189903
    cajas_vecinas_data = search_caja_vecinas(latitude, longitude)
    
    max_count = 3
    if cajas_vecinas_data:
        for i in range(len(cajas_vecinas_data)):
            if i >= max_count: break
            caja_vecina : CajaVecina = CajaVecina(cajas_vecinas_data[i])
            print(caja_vecina)
