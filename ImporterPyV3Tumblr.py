import os
import time
import random
import urllib.parse
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# === Configuración ===
output_dir = r"<Coloque aqui su ruta>"
os.makedirs(output_dir, exist_ok=True)

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Mozilla/5.0 (X11; Linux x86_64)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
]

# === Configuración del navegador ===
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"--user-agent={random.choice(user_agents)}")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")

# === Scroll humano simulado ===
def human_scroll():
    scroll_amount = random.randint(300, 700)
    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    time.sleep(random.uniform(1.0, 2.5))

# === Etiquetas de búsqueda ===
search_tags = ["random", "aesthetic", "art", "nature", "dark"]
current_tag = random.choice(search_tags)
driver.get(f"https://www.tumblr.com/search/{urllib.parse.quote(current_tag)}")
time.sleep(5)

# === Extraer imágenes (srcset o src) ===
def extract_images():
    elements = driver.find_elements(By.TAG_NAME, "img")
    urls = []
    for el in elements:
        srcset = el.get_attribute("srcset")
        if srcset:
            parts = srcset.split(",")
            max_res_url = parts[-1].split()[0]
            if "media.tumblr.com" in max_res_url and ".gif" not in max_res_url:
                urls.append(max_res_url)
        else:
            src = el.get_attribute("src")
            if src and "media.tumblr.com" in src and ".gif" not in src:
                urls.append(src)
    return list(set(urls))

# === Descargar imagen ===
def download_image(url, filename):
    try:
        headers = {"User-Agent": random.choice(user_agents)}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            img.save(filename)
            return True
    except Exception as e:
        print(f"[ERROR] No se pudo descargar: {e}")
    return False

# === Lógica principal ===
seen_urls = set()
total = 0
max_scrolls = 30

for i in range(max_scrolls):
    print(f"[Scroll {i+1}/{max_scrolls}]")

    if i > 0 and i % 5 == 0:
        old_tag = current_tag
        while current_tag == old_tag:
            current_tag = random.choice(search_tags)
        driver.get(f"https://www.tumblr.com/tagged/{urllib.parse.quote(current_tag)}")
        time.sleep(3)

    img_urls = extract_images()
    print(f"    Encontradas: {len(img_urls)}")

    new_count = 0
    for idx, url in enumerate(img_urls):
        if url in seen_urls:
            continue
        seen_urls.add(url)

        ext = url.split('.')[-1].split('?')[0][:4]  # Extensión real: jpg, png, pnj, etc.
        filename = os.path.join(output_dir, f"tumblr_{current_tag}_{i+1}_{idx+1}.{ext}")

        if download_image(url, filename):
            print(f"    Guardada: {url}")
            total += 1
            new_count += 1

        time.sleep(random.uniform(0.2, 0.5))

    print(f"    Nuevas descargadas: {new_count}")
    human_scroll()
    time.sleep(random.uniform(1.5, 3.0))

print(f"\n[FIN] Total de imágenes descargadas: {total}")
driver.quit()
