from caja_vecina_finder import search_caja_vecinas
from coordinates_finder import search_coordinates

def find_nearest_cajas_vecinas(address : str):
    lat, lng = search_coordinates(address)
    print(lat, lng)
    if lat is None or lng is None:
        return None
    return search_caja_vecinas(lat, lng)

while True:
    current_count = 0
    
    max_count = 2 #int(input("How many cajas vecinas do you want to find?\n"))
    address = "Poeta Vicente Huidobro 3500" #input("Enter home address: \n")
    
    cajas_vecinas = find_nearest_cajas_vecinas(address)
    if cajas_vecinas:
        for caja_vecina in cajas_vecinas:
            print(caja_vecina)
            current_count += 1
    break