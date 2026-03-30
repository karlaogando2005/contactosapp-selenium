# ContactoApp — Tarea 4: Pruebas Automatizadas con Selenium

App de gestión de contactos con Flask + pruebas automatizadas con Selenium y Python.

---

## Estructura del proyecto

```
contactos-app/
├── app.py                 # Aplicación Flask (backend)
├── conftest.py            # Fixtures de Selenium (pytest)
├── tests_selenium.py      # Pruebas automatizadas (5 HU × 3 tipos)
├── pytest.ini             # Configuración de pytest
├── requirements.txt       # Dependencias
├── templates/
│   ├── login.html
│   ├── contactos.html
│   └── form_contacto.html
└── screenshots/           # Capturas generadas automáticamente
```

---

## Historias de usuario cubiertas

| ID     | Historia                        | Tipos de prueba              |
|--------|---------------------------------|------------------------------|
| HU-01  | Login de usuario                | Feliz, Negativo, Límites     |
| HU-02  | Crear contacto                  | Feliz, Negativo, Límites     |
| HU-03  | Listar contactos                | Feliz, Negativo, Límites     |
| HU-04  | Editar contacto                 | Feliz, Negativo, Límites     |
| HU-05  | Eliminar contacto               | Feliz, Negativo, Límites     |

---

## Instrucciones de instalación y ejecución

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la app (opcional, para verla en el browser)

```bash
python app.py
```
Abre: http://127.0.0.1:5000  
Usuario: `admin` | Contraseña: `admin123`

### 3. Ejecutar todas las pruebas y generar reporte

```bash
pytest
```

Esto genera:
- `reporte.html` — reporte HTML con resultados
- `screenshots/` — capturas de pantalla de cada escenario

### 4. Ver el reporte

Abre el archivo `reporte.html` en tu navegador.

---

## Tecnologías

- Python 3.10+
- Flask 3.x
- SQLite
- Selenium 4.x
- pytest + pytest-html
- WebDriver Manager (Chrome)
