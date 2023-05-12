import requests
from datetime import datetime

# URL base de la PI Web API
base_url = "http://nombre_del_servidor/piwebapi"

# Ruta del archivo de texto con los datos
archivo_datos = "ruta_del_archivo.txt"

# Obtener el Web ID del tag
def obtener_webid_tag(nombre_tag):
    url = f"{base_url}/points?path=\\\\nombre_del_servidor\\{nombre_tag}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "WebId" in data:
            return data["WebId"]
    return None

# Leer el archivo de texto y procesar los datos
with open(archivo_datos, 'r') as file:
    for line in file:
        # Dividir la línea en tag, timestamp y valor
        tag, timestamp_str, valor = line.strip().split(";")
        
        # Obtener el Web ID del tag
        web_id = obtener_webid_tag(tag)
        
        if web_id:
            # Convertir el timestamp a un objeto de tipo datetime
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            
            # Formatear el timestamp en el formato esperado por la PI Web API
            timestamp_str = timestamp.strftime("%Y-%m-%dT%H:%M:%S")
            
            # Construir la URL para insertar los datos
            url = f"{base_url}/streams/{web_id}/value"
            
            # Configurar los encabezados y los datos a enviar
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "Timestamp": timestamp_str,
                "Value": valor
            }
            
            # Realizar la solicitud POST para insertar los datos
            response = requests.post(url, json=data, headers=headers)
            
            # Verificar el código de respuesta de la solicitud
            if response.status_code == 201:
                print(f"Dato insertado correctamente en el tag {tag}")
            else:
                print(f"Error al insertar el dato en el tag {tag}:", response.text)
        else:
            print(f"No se encontró el Web ID del tag {tag}")
