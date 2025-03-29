import os
import time
import random
import requests
import urllib.parse
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración
output_dir = r"<Coloque aqui su ruta>"
os.makedirs(output_dir, exist_ok=True)

# Lista de user agents para rotación
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
]

# Iniciar navegador con opciones anti-detección
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"--user-agent={random.choice(user_agents)}")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Para evadir la detección de automation
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")

# Función para simular comportamiento humano
def human_like_scroll():
    # Scroll con variación aleatoria
    scroll_amount = random.randint(300, 700)
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    time.sleep(random.uniform(0.8, 2.0))

# Abrir Pinterest
search_queries = ["random", "nature", "art", "design", "food"]  # Múltiples búsquedas para más variedad
current_query = random.choice(search_queries)
driver.get(f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(current_query)}")
time.sleep(5)  # Dar tiempo para que la página cargue completamente

# Función para extraer imágenes de Pinterest
def extract_pin_images():
    images = []
    try:
        # Intentar diferentes selectores para mayor robustez
        selectors = [
            "div[data-test-id='pin'] img",
            "div.GrowthUnauthPinImage img",
            "div[data-grid-item] img",
            ".pinWrapper img"
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for element in elements:
                        src = element.get_attribute("src")
                        if src and ("i.pinimg.com" in src) and ".jpg" in src:
                            # Intentar obtener la versión de mayor resolución
                            src = src.replace("236x", "originals")
                            images.append(src)
            except:
                continue
    except Exception as e:
        print(f"Error al extraer imágenes: {str(e)}")
    
    return list(set(images))  # Eliminar duplicados

# Función para descargar y guardar imagen
def download_image(url, filename):
    try:
        headers = {
            "User-Agent": random.choice(user_agents),
            "Referer": "https://www.pinterest.com/"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.save(filename)
            return True
    except Exception as e:
        print(f"    Error descargando imagen: {str(e)}")
    return False

# Registro de URLs ya procesadas
image_urls_seen = set()
total_pins = 0
max_scrolls = 30  # Aumentar el número de scrolls
images_per_scroll = 10  # Cuántas imágenes intentamos guardar por scroll

# Función para cambiar periódicamente la búsqueda
def change_search_query():
    global current_query
    old_query = current_query
    while current_query == old_query:
        current_query = random.choice(search_queries)
    
    print(f"Cambiando búsqueda a: {current_query}")
    driver.get(f"https://www.pinterest.com/search/pins/?q={urllib.parse.quote(current_query)}")
    time.sleep(3)

# Iniciar proceso de extracción
for scroll_index in range(max_scrolls):
    print(f"[{scroll_index+1}/{max_scrolls}] Procesando scroll...")
    
    # Cambiar búsqueda cada 5 scrolls para obtener más variedad
    if scroll_index > 0 and scroll_index % 5 == 0:
        change_search_query()
    
    # Simular comportamiento aleatorio
    if random.random() > 0.7:
        # A veces hacemos scrolls extra o esperamos más tiempo
        human_like_scroll()
    
    # Extraer imágenes del scroll actual
    pin_images = extract_pin_images()
    print(f"    Se encontraron {len(pin_images)} imágenes potenciales")
    
    # Procesar imágenes
    new_pins = 0
    for i, img_url in enumerate(pin_images):
        if img_url in image_urls_seen or new_pins >= images_per_scroll:
            continue
        
        # Guardar URL para evitar duplicados
        image_urls_seen.add(img_url)
        
        # Descargar y guardar la imagen
        filename = os.path.join(output_dir, f"img_{current_query}_{scroll_index+1}_{i+1}.jpg")
        if download_image(img_url, filename):
            new_pins += 1
            total_pins += 1
            print(f"    Guardada imagen {i+1} del scroll {scroll_index+1}")
        
        # Pequeña pausa aleatoria entre descargas
        time.sleep(random.uniform(0.1, 0.5))
    
    print(f"    Guardadas {new_pins} imágenes nuevas de este scroll")
    
    # Scroll hacia abajo con comportamiento humano simulado
    human_like_scroll()
    
    # Pausa aleatoria entre scrolls
    time.sleep(random.uniform(1.5, 3.0))

driver.quit()
print(f"[FIN] Proceso completado. Se guardaron {total_pins} imágenes en total.")