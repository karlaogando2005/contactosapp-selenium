"""
conftest.py — Fixtures compartidos para todas las pruebas Selenium
"""
import pytest
import os
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Importar la app Flask
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, init_db

BASE_URL = "http://127.0.0.1:5000"
SCREENSHOT_DIR = "screenshots"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def flask_server():
    """Levanta el servidor Flask en un hilo secundario."""
    def run():
        app.run(port=5000, debug=False, use_reloader=False)

    t = threading.Thread(target=run, daemon=True)
    t.start()
    time.sleep(2)  # Esperar que levante
    yield
    # El daemon thread se cierra solo al terminar la sesión


@pytest.fixture()
def driver():
    """Crea y retorna un WebDriver de Chrome en modo headless."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=service, options=options)
    d.implicitly_wait(5)
    yield d
    d.quit()


def tomar_screenshot(driver, nombre_test):
    """Guarda captura de pantalla con el nombre del test."""
    path = os.path.join(SCREENSHOT_DIR, f"{nombre_test}.png")
    driver.save_screenshot(path)
    print(f"\n📸 Screenshot guardado: {path}")
    return path


def login_como_admin(driver):
    """Helper: hace login con credenciales correctas."""
    driver.get(f"{BASE_URL}/login")
    driver.find_element("id", "username").send_keys("admin")
    driver.find_element("id", "password").send_keys("admin123")
    driver.find_element("id", "btn-login").click()
    time.sleep(0.5)
