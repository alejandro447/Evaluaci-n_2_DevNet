import requests
import sys

# Tu API Key de GraphHopper
API_KEY ='555b70fa-1b5e-4989-9aae-20bcbe6b2a22'

# Consumo por kilómetro en litros (ejemplo: 12 km/L → 1L cada 12 km)
CONSUMO_KM_LITRO = 12

def obtener_datos_viaje(origen, destino):
    url = "https://graphhopper.com/api/1/routegeocode"
    params = {
        "point": [origen, destino],
        "vehicle": "car",
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": '555b70fa-1b5e-4989-9aae-20bcbe6b2a22'
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error al consultar la API: {response.status_code}")
        sys.exit()

    data = response.json()

    distancia_metros = data['paths'][0]['distance']
    tiempo_miliseg = data['paths'][0]['time']
    instrucciones = data['paths'][0]['instructions']

    return distancia_metros, tiempo_miliseg, instrucciones

def mostrar_narrativa(instrucciones):
    print("\n Narrativa del viaje:")
    for i, paso in enumerate(instrucciones):
        texto = paso['text']
        distancia = paso['distance'] / 1000
        print(f"Paso {i+1}: {texto} ({distancia:.2f} km)")

def formatear_tiempo(ms):
    segundos = ms // 1000
    minutos = segundos // 60
    horas = minutos // 60
    return horas, minutos % 60, segundos % 60

def main():
    print("===== Evaluación 2 - DevNet =====")
    print("Presiona 'q' para salir.\n")

    while True:
        origen = input("Ingrese Ciudad de Origen: ")
        if origen.lower() == 'q':
            print("Saliendo del programa.")
            break

        destino = input("Ingrese Ciudad de Destino: ")
        if destino.lower() == 'q':
            print("Saliendo del programa.")
            break

        try:
            distancia_m, tiempo_ms, instrucciones = obtener_datos_viaje(origen, destino)
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            continue

        distancia_km = distancia_m / 1000
        horas, minutos, segundos = formatear_tiempo(tiempo_ms)
        litros_consumidos = distancia_km / CONSUMO_KM_LITRO

        print(f"\n Distancia entre {origen} y {destino}: {distancia_km:.2f} km")
        print(f" Duración estimada del viaje: {horas:.0f}h {minutos:.0f}m {segundos:.0f}s")
        print(f" Combustible estimado requerido: {litros_consumidos:.2f} litros")

        mostrar_narrativa(instrucciones)
        print("\n===========================\n")

if __name__ == "__main__":
    main()
