from caja_vecina_finder import search_caja_vecinas, CajaVecina
from coordinates_finder import search_coordinates

def find_nearest_cajas_vecinas(address : str):
    lat, lng = search_coordinates(address)
    if lat is None or lng is None:
        return None
    return search_caja_vecinas(lat, lng)

def ask_for_nearby_cajas_vecinas():
    max_count = get_caja_vecina_count()
    address = input("Enter home address: \n")
    
    cajas_vecinas = find_nearest_cajas_vecinas(address)
    if cajas_vecinas:
        print("Here are the nearest cajas vecinas: ")
        for i in range(len(cajas_vecinas)):
            if i >= max_count: break
            caja_vecina : CajaVecina = CajaVecina(cajas_vecinas[i])
            print(caja_vecina)
    else:
        print("No nearby caja vecinas were found")

def get_caja_vecina_count():
    while True:
        count = input("How many cajas vecinas do you want to find? \n")
        if not count.isnumeric():
            print("ERROR: Input is not numeric")
            continue
        count = int(count)
        if count <= 0:
            print("ERROR: Input is lower or equal to zero")
            continue
        return count

if __name__ == "__main__":
    while True:    
        ask_for_nearby_cajas_vecinas()
        continue_input = input("Want to continue? (Y/N) \n")
        if continue_input.lower() not in ["y", "yes"]:
            break