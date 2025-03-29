import requests
import os

# Ruta personalizada para guardar las imágenes (modifícala a tu gusto)
ruta_destino = r'<Coloque aqui su ruta>'

# Crear la carpeta si no existe
os.makedirs(ruta_destino, exist_ok=True)

cantidad = 1000  # Número de imágenes a descargar

for i in range(cantidad):
    url = 'https://picsum.photos/200/300'
    response = requests.get(url)

    if response.status_code == 200:
        nombre_archivo = f'imagen_{i+1}.jpg'
        ruta_completa = os.path.join(ruta_destino, nombre_archivo)

        with open(ruta_completa, 'wb') as f:
            f.write(response.content)

        print(f'Imagen {i+1} guardada en {ruta_completa}')
    else:
        print(f'Error al descargar imagen {i+1}')
