"""
tests_selenium.py
=================
Pruebas automatizadas con Selenium - ContactoApp
"""
import time
import pytest
from selenium.webdriver.common.by import By
from conftest import login_como_admin, BASE_URL


# =========================
# HU01 LOGIN
# =========================
class TestHU01Login:

    def test_login_camino_feliz(self, driver):
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("admin123")

        driver.find_element(By.ID, "btn-login").click()
        time.sleep(1)

        assert "/contactos" in driver.current_url

    def test_login_negativo(self, driver):
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("mala")

        driver.find_element(By.ID, "btn-login").click()
        time.sleep(1)

        assert "/login" in driver.current_url

    def test_login_limite(self, driver):
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.ID, "btn-login").click()
        time.sleep(1)

        assert "/login" in driver.current_url


# =========================
# HU02 CREAR
# =========================
class TestHU02Crear:

    def test_crear_camino_feliz(self, driver):
        login_como_admin(driver)

        driver.find_element(By.ID, "btn-nuevo").click()
        time.sleep(0.5)

        driver.find_element(By.ID, "nombre").send_keys("Laura Martinez")
        driver.find_element(By.ID, "email").send_keys("laura@test.com")

        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(1)

        assert "Laura Martinez" in driver.page_source

    def test_crear_negativo(self, driver):
        login_como_admin(driver)

        driver.find_element(By.ID, "btn-nuevo").click()
        time.sleep(0.5)

        driver.find_element(By.ID, "nombre").send_keys("Sin Email")

        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(1)

        assert "error" in driver.page_source.lower()

    def test_crear_limite(self, driver):
        login_como_admin(driver)

        driver.find_element(By.ID, "btn-nuevo").click()
        time.sleep(0.5)

        driver.find_element(By.ID, "nombre").send_keys("A" * 100)
        driver.find_element(By.ID, "email").send_keys("limite@test.com")

        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(1)

        assert "/contactos" in driver.current_url


# =========================
# HU03 LISTAR
# =========================
class TestHU03Listar:

    def test_listar_camino_feliz(self, driver):
        login_como_admin(driver)
        time.sleep(1)

        assert "contacto" in driver.page_source.lower()

    def test_listar_negativo(self, driver):
        driver.get(f"{BASE_URL}/contactos")
        time.sleep(1)

        assert "/login" in driver.current_url

    def test_listar_limite(self, driver):
        login_como_admin(driver)
        time.sleep(1)

        assert "contacto" in driver.page_source.lower()


# =========================
# HU04 EDITAR
# =========================
class TestHU04Editar:

    def test_editar_camino_feliz(self, driver):
        login_como_admin(driver)
        time.sleep(1)

        botones = driver.find_elements(By.XPATH, "//a[contains(@id,'btn-editar')]")
        assert botones

        driver.execute_script("arguments[0].scrollIntoView();", botones[0])
        driver.execute_script("arguments[0].click();", botones[0])
        time.sleep(0.5)

        campo = driver.find_element(By.ID, "nombre")
        campo.clear()
        campo.send_keys("Editado OK")

        btn = driver.find_element(By.ID, "btn-guardar")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)

        assert "Editado OK" in driver.page_source

    def test_editar_negativo(self, driver):
        login_como_admin(driver)
        time.sleep(1)

        botones = driver.find_elements(By.XPATH, "//a[contains(@id,'btn-editar')]")
        assert botones

        driver.execute_script("arguments[0].click();", botones[0])
        time.sleep(0.5)

        campo = driver.find_element(By.ID, "nombre")
        campo.clear()

        btn = driver.find_element(By.ID, "btn-guardar")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)

        assert "error" in driver.page_source.lower()

    def test_editar_limite(self, driver):
        login_como_admin(driver)
        time.sleep(1)

        botones = driver.find_elements(By.XPATH, "//a[contains(@id,'btn-editar')]")
        assert botones

        driver.execute_script("arguments[0].click();", botones[0])
        time.sleep(0.5)

        campo = driver.find_element(By.ID, "nombre")
        campo.clear()
        campo.send_keys("B" * 101)

        btn = driver.find_element(By.ID, "btn-guardar")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)

        assert "B" * 101 not in driver.page_source


# =========================
# HU05 ELIMINAR
# =========================
class TestHU05Eliminar:

    def test_eliminar_camino_feliz(self, driver):
        login_como_admin(driver)
        time.sleep(1)

        # Crear contacto
        driver.find_element(By.ID, "btn-nuevo").click()
        time.sleep(0.5)

        driver.find_element(By.ID, "nombre").send_keys("Eliminar Now")
        driver.find_element(By.ID, "email").send_keys("eliminar@test.com")

        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(1)

        # Obtener ID
        botones = driver.find_elements(By.XPATH, "//button[contains(@id,'btn-eliminar')]")
        assert botones

        ultimo = botones[-1]
        contacto_id = ultimo.get_attribute("id").replace("btn-eliminar-", "")

        # Eliminar
        driver.get(f"{BASE_URL}/contactos/eliminar/{contacto_id}")
        time.sleep(1)

        driver.get(f"{BASE_URL}/contactos")
        time.sleep(1)

        # Validar por ID
        botones_restantes = driver.find_elements(By.XPATH, "//button[contains(@id,'btn-eliminar')]")

        ids = [b.get_attribute("id").replace("btn-eliminar-", "") for b in botones_restantes]

        assert contacto_id not in ids

    def test_eliminar_negativo(self, driver):
        driver.get(f"{BASE_URL}/contactos/eliminar/1")
        time.sleep(1)

        assert "/login" in driver.current_url

    def test_eliminar_limite(self, driver):
        login_como_admin(driver)

        driver.get(f"{BASE_URL}/contactos/eliminar/99999")
        time.sleep(1)

        assert "/contactos" in driver.current_url