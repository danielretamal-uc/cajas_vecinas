import requests

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
            print(data['candidates'])
            first_candidate = data['candidates'][0]
            return first_candidate['location']['y'] / 100000, first_candidate['location']['x'] / 100000
        else:
            print("No address match found.")
            return None, None
    else:
        print(f"Error: Received status code {response.status_code}")
        return None, None

search_coordinates("poeta huidobro 3500, macul")