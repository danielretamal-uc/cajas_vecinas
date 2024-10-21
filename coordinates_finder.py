import requests
from pyproj import Transformer

def search_coordinates(address : str, distance : int = 50000):
    url = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"
    params = {
        'SingleLine': address,
        'f': 'json',
        'outSR': '{"wkid":102100}',
        'outFields': 'Addr_type,Match_addr,StAddr,City',
        'countryCode': 'CL',
        'distance': distance,
        'location': "{'x':-8119607.167932156,'y':-5082176.560660033,'spatialReference':{'wkid':102100}}",
        'maxLocations': 6
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get('candidates'):
            first_candidate = data['candidates'][0]
            web_mercator_x = first_candidate['location']['x']
            web_mercator_y = first_candidate['location']['y']
            
            lat, lng = convert_to_lat_lng(web_mercator_x, web_mercator_y)
            return lat, lng
        else:
            print("No address match found.")
            return None, None
    else:
        print(f"Error: Received status code {response.status_code}")
        return None, None

def convert_to_lat_lng(x, y):
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
    lng, lat = transformer.transform(x, y)
    return lat, lng

if __name__ == "__main__":
   lat, lng = search_coordinates("Av. Príncipe de Gales 7170, La Reina")
   print(f"{lat}, {lng}")