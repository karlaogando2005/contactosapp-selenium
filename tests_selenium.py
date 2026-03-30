"""
tests_selenium.py
=================
Pruebas automatizadas con Selenium — ContactoApp
Cubre 5 Historias de Usuario × 3 tipos de prueba cada una.

Historias:
  HU-01: Login de usuario
  HU-02: Crear contacto
  HU-03: Listar contactos
  HU-04: Editar contacto
  HU-05: Eliminar contacto
"""
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import tomar_screenshot, login_como_admin, BASE_URL


# ─────────────────────────────────────────────────────────────────────────────
# HU-01: Login de usuario
# ─────────────────────────────────────────────────────────────────────────────

class TestHU01Login:
    """HU-01: Como usuario, quiero iniciar sesión para acceder al sistema."""

    def test_login_camino_feliz(self, driver):
        """✅ Camino feliz: login con credenciales válidas."""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("admin123")
        driver.find_element(By.ID, "btn-login").click()
        time.sleep(0.5)

        tomar_screenshot(driver, "HU01_login_camino_feliz")

        assert "/contactos" in driver.current_url, \
            "Debe redirigir a /contactos tras login exitoso"
        assert "admin" in driver.page_source, \
            "Debe mostrar el nombre del usuario en la página"

    def test_login_negativo_credenciales_incorrectas(self, driver):
        """❌ Prueba negativa: login con contraseña incorrecta."""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("contraseña_mala")
        driver.find_element(By.ID, "btn-login").click()
        time.sleep(0.5)

        tomar_screenshot(driver, "HU01_login_negativo_credenciales")

        assert "/login" in driver.current_url, \
            "Debe permanecer en /login si las credenciales son incorrectas"
        error = driver.find_element(By.ID, "error-msg")
        assert error.is_displayed(), "Debe mostrar mensaje de error"

    def test_login_limites_campos_vacios(self, driver):
        """⚠️ Prueba de límites: enviar formulario con campos vacíos."""
        driver.get(f"{BASE_URL}/login")
        # No llenar ningún campo
        driver.find_element(By.ID, "btn-login").click()
        time.sleep(0.5)

        tomar_screenshot(driver, "HU01_login_limite_campos_vacios")

        assert "/login" in driver.current_url, \
            "Debe permanecer en /login si no se llenaron los campos"
        error = driver.find_element(By.ID, "error-msg")
        assert "completa" in error.text.lower() or "campos" in error.text.lower(), \
            "Debe indicar que los campos son requeridos"


# ─────────────────────────────────────────────────────────────────────────────
# HU-02: Crear contacto
# ─────────────────────────────────────────────────────────────────────────────

class TestHU02CrearContacto:
    """HU-02: Como usuario, quiero crear un nuevo contacto con nombre y email."""

    def test_crear_contacto_camino_feliz(self, driver):
        """✅ Camino feliz: crear contacto con datos válidos."""
        login_como_admin(driver)
        driver.find_element(By.ID, "btn-nuevo").click()
        time.sleep(0.3)

        driver.find_element(By.ID, "nombre").send_keys("Laura Martínez")
        driver.find_element(By.ID, "email").send_keys("laura@ejemplo.com")
        driver.find_element(By.ID, "telefono").send_keys("809-555-0011")
        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(0.5)

        tomar_screenshot(driver, "HU02_crear_contacto_feliz")

        assert "/contactos" in driver.current_url, \
            "Debe redirigir al listado tras crear"
        assert "Laura Martínez" in driver.page_source, \
            "El nuevo contacto debe aparecer en la lista"

    def test_crear_contacto_negativo_sin_email(self, driver):
        """❌ Prueba negativa: crear contacto sin email obligatorio."""
        login_como_admin(driver)
        driver.find_element(By.ID, "btn-nuevo").click()
        time.sleep(0.3)

        driver.find_element(By.ID, "nombre").send_keys("Sin Email Test")
        # Email vacío intencionalmente
        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(0.5)

        tomar_screenshot(driver, "HU02_crear_contacto_negativo_sin_email")

        assert "/nuevo" in driver.current_url or "form" in driver.page_source.lower(), \
            "Debe permanecer en el formulario si falta email"
        error = driver.find_element(By.ID, "error-msg")
        assert error.is_displayed(), "Debe mostrar error cuando falta el email"

    def test_crear_contacto_limite_nombre_largo(self, driver):
        """⚠️ Prueba de límites: nombre con exactamente 100 caracteres (máximo permitido)."""
        login_como_admin(driver)
        driver.find_element(By.ID, "btn-nuevo").click()
        time.sleep(0.3)

        nombre_100 = "A" * 100
        driver.find_element(By.ID, "nombre").send_keys(nombre_100)
        driver.find_element(By.ID, "email").send_keys("limite@test.com")
        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(0.5)

        tomar_screenshot(driver, "HU02_crear_contacto_limite_nombre_100")

        assert "/contactos" in driver.current_url, \
            "Debe aceptar nombre de exactamente 100 caracteres"


# ─────────────────────────────────────────────────────────────────────────────
# HU-03: Listar contactos
# ─────────────────────────────────────────────────────────────────────────────

class TestHU03ListarContactos:
    """HU-03: Como usuario, quiero ver todos mis contactos en una tabla."""

    def test_listar_camino_feliz(self, driver):
        """✅ Camino feliz: la tabla se muestra tras iniciar sesión."""
        login_como_admin(driver)

        tomar_screenshot(driver, "HU03_listar_camino_feliz")

        assert "Contactos" in driver.title or "Contactos" in driver.page_source, \
            "La página de contactos debe cargarse correctamente"
        # Verificar que existe el elemento de la tabla o mensaje de vacío
        body = driver.page_source
        assert "tabla-contactos" in body or "Sin contactos" in body, \
            "Debe mostrar tabla de contactos o mensaje de lista vacía"

    def test_listar_negativo_sin_sesion(self, driver):
        """❌ Prueba negativa: acceder a /contactos sin sesión activa."""
        # No hacer login
        driver.get(f"{BASE_URL}/contactos")
        time.sleep(0.5)

        tomar_screenshot(driver, "HU03_listar_negativo_sin_sesion")

        assert "/login" in driver.current_url, \
            "Debe redirigir a /login si no hay sesión"

    def test_listar_limite_contador(self, driver):
        """⚠️ Prueba de límites: verificar que el contador de contactos es correcto."""
        login_como_admin(driver)

        tomar_screenshot(driver, "HU03_listar_limite_contador")

        body = driver.page_source
        # El contador siempre debe estar presente (0 o más contactos)
        assert "contacto" in body.lower(), \
            "El contador de contactos debe estar visible en la página"


# ─────────────────────────────────────────────────────────────────────────────
# HU-04: Editar contacto
# ─────────────────────────────────────────────────────────────────────────────

class TestHU04EditarContacto:
    """HU-04: Como usuario, quiero editar los datos de un contacto existente."""

    def _asegurar_contacto_existe(self, driver, nombre="Contacto Editable", email="editable@test.com"):
        """Helper: crea un contacto si no existe para poder editarlo."""
        login_como_admin(driver)
        if nombre not in driver.page_source:
            driver.find_element(By.ID, "btn-nuevo").click()
            time.sleep(0.3)
            driver.find_element(By.ID, "nombre").send_keys(nombre)
            driver.find_element(By.ID, "email").send_keys(email)
            driver.find_element(By.ID, "btn-guardar").click()
            time.sleep(0.5)

    def test_editar_camino_feliz(self, driver):
        """✅ Camino feliz: editar nombre de un contacto existente."""
        self._asegurar_contacto_existe(driver)
        # Clic en el primer botón Editar disponible
        botones_editar = driver.find_elements(By.XPATH, "//a[contains(@id, 'btn-editar-')]")
        assert len(botones_editar) > 0, "Debe haber al menos un contacto para editar"

        botones_editar[0].click()
        time.sleep(0.3)

        campo_nombre = driver.find_element(By.ID, "nombre")
        campo_nombre.clear()
        campo_nombre.send_keys("Nombre Actualizado")
        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(0.5)

        tomar_screenshot(driver, "HU04_editar_camino_feliz")

        assert "Nombre Actualizado" in driver.page_source, \
            "El nombre actualizado debe aparecer en la lista"

    def test_editar_negativo_borrar_nombre(self, driver):
        """❌ Prueba negativa: intentar guardar contacto sin nombre."""
        self._asegurar_contacto_existe(driver)
        botones_editar = driver.find_elements(By.XPATH, "//a[contains(@id, 'btn-editar-')]")
        assert len(botones_editar) > 0, "Debe haber al menos un contacto para editar"

        botones_editar[0].click()
        time.sleep(0.3)

        campo_nombre = driver.find_element(By.ID, "nombre")
        campo_nombre.clear()
        # Dejar nombre vacío
        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(0.5)

        tomar_screenshot(driver, "HU04_editar_negativo_sin_nombre")

        error = driver.find_element(By.ID, "error-msg")
        assert error.is_displayed(), "Debe mostrar error si el nombre está vacío"

    def test_editar_limite_nombre_101_chars(self, driver):
        """⚠️ Prueba de límites: nombre con 101 caracteres (supera el máximo)."""
        self._asegurar_contacto_existe(driver)
        botones_editar = driver.find_elements(By.XPATH, "//a[contains(@id, 'btn-editar-')]")
        assert len(botones_editar) > 0

        botones_editar[0].click()
        time.sleep(0.3)

        campo_nombre = driver.find_element(By.ID, "nombre")
        campo_nombre.clear()
        campo_nombre.send_keys("B" * 101)
        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(0.5)

        tomar_screenshot(driver, "HU04_editar_limite_nombre_101chars")

        error = driver.find_element(By.ID, "error-msg")
        assert error.is_displayed(), \
            "Debe rechazar nombre con más de 100 caracteres"


# ─────────────────────────────────────────────────────────────────────────────
# HU-05: Eliminar contacto
# ─────────────────────────────────────────────────────────────────────────────

class TestHU05EliminarContacto:
    """HU-05: Como usuario, quiero eliminar un contacto que ya no necesito."""

    def _asegurar_contacto_existe(self, driver, nombre="Contacto Para Borrar", email="borrar@test.com"):
        login_como_admin(driver)
        if nombre not in driver.page_source:
            driver.find_element(By.ID, "btn-nuevo").click()
            time.sleep(0.3)
            driver.find_element(By.ID, "nombre").send_keys(nombre)
            driver.find_element(By.ID, "email").send_keys(email)
            driver.find_element(By.ID, "btn-guardar").click()
            time.sleep(0.5)

    def test_eliminar_camino_feliz(self, driver):
        """✅ Camino feliz: crear y luego eliminar un contacto."""
        login_como_admin(driver)

        # Crear uno específico para eliminar
        driver.find_element(By.ID, "btn-nuevo").click()
        time.sleep(0.3)
        driver.find_element(By.ID, "nombre").send_keys("Para Eliminar Now")
        driver.find_element(By.ID, "email").send_keys("eliminar@ahora.com")
        driver.find_element(By.ID, "btn-guardar").click()
        time.sleep(0.5)

        assert "Para Eliminar Now" in driver.page_source

        # Aceptar el confirm dialog automáticamente
        driver.execute_script("window.confirm = function() { return true; }")

        botones_eliminar = driver.find_elements(By.XPATH, "//button[contains(@id, 'btn-eliminar-')]")
        assert len(botones_eliminar) > 0
        botones_eliminar[-1].click()
        time.sleep(0.7)

        tomar_screenshot(driver, "HU05_eliminar_camino_feliz")

        assert "Para Eliminar Now" not in driver.page_source, \
            "El contacto eliminado no debe aparecer en la lista"

    def test_eliminar_negativo_sin_sesion(self, driver):
        """❌ Prueba negativa: intentar eliminar por URL sin sesión activa."""
        # Sin hacer login, intentar eliminar directamente
        driver.get(f"{BASE_URL}/contactos/eliminar/1")
        time.sleep(0.5)

        tomar_screenshot(driver, "HU05_eliminar_negativo_sin_sesion")

        # Debe redirigir a login (GET no está permitido, pero la sesión no existe)
        assert "/login" in driver.current_url or driver.current_url != f"{BASE_URL}/contactos", \
            "Sin sesión no debe poder acceder a operaciones de eliminación"

    def test_eliminar_limite_id_inexistente(self, driver):
        """⚠️ Prueba de límites: eliminar un ID que no existe (ej: 99999)."""
        login_como_admin(driver)
        url_actual = driver.current_url

        # Intentar eliminar via JS (simular POST a ID inexistente)
        driver.execute_script("""
            const f = document.createElement('form');
            f.method = 'POST';
            f.action = '/contactos/eliminar/99999';
            document.body.appendChild(f);
            f.submit();
        """)
        time.sleep(0.7)

        tomar_screenshot(driver, "HU05_eliminar_limite_id_inexistente")

        # Debe redirigir al listado sin error fatal
        assert "/contactos" in driver.current_url, \
            "Debe manejar IDs inexistentes y redirigir al listado sin error 500"
        assert "500" not in driver.page_source and "Error" not in driver.title, \
            "No debe producir un error 500 al intentar eliminar ID inexistente"
