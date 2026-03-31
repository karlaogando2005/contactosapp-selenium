from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "clave_secreta_selenium_2025"
DB = "contactos.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT,
                usuario_id INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        # Usuario de prueba
        try:
            conn.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)",
                         ("admin", "admin123"))
            conn.commit()
        except:
            pass

init_db()

@app.route("/")
def index():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("contactos"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            error = "Por favor completa todos los campos."
        else:
            with get_db() as conn:
                user = conn.execute(
                    "SELECT * FROM usuarios WHERE username=? AND password=?",
                    (username, password)
                ).fetchone()
            if user:
                session["usuario"] = username
                session["usuario_id"] = user["id"]
                return redirect(url_for("contactos"))
            else:
                error = "Usuario o contraseña incorrectos."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/contactos")
def contactos():
    if "usuario" not in session:
        return redirect(url_for("login"))
    with get_db() as conn:
        lista = conn.execute(
            "SELECT * FROM contactos WHERE usuario_id=?",
            (session["usuario_id"],)
        ).fetchall()
    return render_template("contactos.html", contactos=lista, usuario=session["usuario"])

@app.route("/contactos/nuevo", methods=["GET", "POST"])
def nuevo_contacto():
    if "usuario" not in session:
        return redirect(url_for("login"))
    error = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre or not email:
            error = "Nombre y email son obligatorios."
        elif len(nombre) > 100:
            error = "El nombre no puede superar los 100 caracteres."
        elif len(email) > 150:
            error = "El email no puede superar los 150 caracteres."
        else:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO contactos (nombre, email, telefono, usuario_id) VALUES (?,?,?,?)",
                    (nombre, email, telefono, session["usuario_id"])
                )
                conn.commit()
            flash("Contacto creado exitosamente.", "success")
            return redirect(url_for("contactos"))
    return render_template("form_contacto.html", accion="Crear", contacto=None, error=error)

@app.route("/contactos/editar/<int:id>", methods=["GET", "POST"])
def editar_contacto(id):
    if "usuario" not in session:
        return redirect(url_for("login"))
    with get_db() as conn:
        contacto = conn.execute(
            "SELECT * FROM contactos WHERE id=? AND usuario_id=?",
            (id, session["usuario_id"])
        ).fetchone()
    if not contacto:
        return redirect(url_for("contactos"))
    error = None
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre or not email:
            error = "Nombre y email son obligatorios."
        elif len(nombre) > 100:
            error = "El nombre no puede superar los 100 caracteres."
        else:
            with get_db() as conn:
                conn.execute(
                    "UPDATE contactos SET nombre=?, email=?, telefono=? WHERE id=?",
                    (nombre, email, telefono, id)
                )
                conn.commit()
            flash("Contacto actualizado.", "success")
            return redirect(url_for("contactos"))
    return render_template("form_contacto.html", accion="Editar", contacto=contacto, error=error)

@app.route("/contactos/eliminar/<int:id>", methods=["GET", "POST"])
def eliminar_contacto(id):
    if "usuario" not in session:
        return redirect(url_for("login"))
    try:
        with get_db() as conn:
            conn.execute(
                "DELETE FROM contactos WHERE id=? AND usuario_id=?",
                (id, session["usuario_id"])
            )
            conn.commit()
    except Exception:
        pass
    flash("Contacto eliminado.", "success")
    return redirect(url_for("contactos"))
if __name__ == "__main__":
    app.run(debug=True, port=5000)
