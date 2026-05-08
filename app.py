from pathlib import Path
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = "saludya"
BASE_DIR = Path(__file__).resolve().parent
app.config["DATABASE"] = str(BASE_DIR / "saludya.db")

# =========================
# CREAR BASE DE DATOS
# =========================
def init_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    cursor = conn.cursor()

    # TABLA USUARIOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT,
            contraseña TEXT
        )
    ''')

    # TABLA CITAS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correo TEXT,
            fecha TEXT,
            hora TEXT,
            servicio TEXT
        )
    ''')

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def get_current_user():
    correo = session.get("usuario")
    if not correo:
        return None

    conn = get_db_connection()
    usuario = conn.execute(
        "SELECT nombre, correo FROM usuarios WHERE correo=?",
        (correo,),
    ).fetchone()
    conn.close()

    if usuario:
        return usuario

    return {"nombre": "", "correo": correo}


def get_password_from_form():
    return request.form.get("contraseña") or request.form.get("contrasena")

# =========================
# LOGIN
# =========================
@app.route('/')
def login():
    return render_template('login.html')

# =========================
# REGISTRO
# =========================
@app.route('/registro')
def registro():
    return render_template('registro.html')

# =========================
# GUARDAR USUARIO
# =========================
@app.route('/guardar', methods=['POST'])
def guardar():

    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    contrasena = get_password_from_form()

    if not nombre or not correo or not contrasena:
        flash("Completa todos los campos del registro.", "error")
        return redirect('/registro')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usuarios (nombre, correo, contraseña) VALUES (?, ?, ?)",
        (nombre, correo, contrasena)
    )

    conn.commit()
    conn.close()

    flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
    return redirect('/')

# =========================
# INGRESAR
# =========================
@app.route('/ingresar', methods=['POST'])
def ingresar():

    correo = request.form.get('correo', '').strip()
    contrasena = get_password_from_form()

    if not correo or not contrasena:
        flash("Ingresa tu correo y contraseña para continuar.", "error")
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE correo=? AND contraseña=?",
        (correo, contrasena)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        session['usuario'] = correo
        return redirect('/panel')

    flash("Datos incorrectos. Verifica tu correo y contraseña.", "error")
    return redirect('/')

# =========================
# PANEL PRINCIPAL
# =========================
@app.route('/panel')
def panel():

    if 'usuario' in session:
        usuario = get_current_user()
        return render_template('panel.html', usuario=usuario)

    return redirect('/')

# =========================
# FORMULARIO CITA
# =========================
@app.route('/cita')
def cita():

    if 'usuario' not in session:
        return redirect('/')

    usuario = get_current_user()
    return render_template('cita.html', usuario=usuario)

# =========================
# GUARDAR CITA
# =========================
@app.route('/guardar_cita', methods=['POST'])
def guardar_cita():

    if 'usuario' not in session:
        return redirect('/')

    correo = session['usuario']

    fecha = request.form['fecha']
    hora = request.form['hora']
    servicio = request.form['servicio']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO citas (correo, fecha, hora, servicio) VALUES (?, ?, ?, ?)",
        (correo, fecha, hora, servicio)
    )

    conn.commit()
    conn.close()

    flash("Cita agendada correctamente.", "success")
    return redirect('/historial')

# =========================
# HISTORIAL
# =========================
@app.route('/historial')
def historial():

    if 'usuario' not in session:
        return redirect('/')

    correo = session['usuario']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM citas WHERE correo=?",
        (correo,)
    )

    citas = cursor.fetchall()

    conn.close()

    usuario = get_current_user()
    return render_template('historial.html', citas=citas, usuario=usuario)

# =========================
# CERRAR SESIÓN
# =========================
@app.route('/logout')
def logout():

    session.pop('usuario', None)
    flash("Sesión cerrada correctamente.", "success")
    return redirect('/')

# =========================
# INICIAR APP
# =========================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
