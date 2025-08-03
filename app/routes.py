from flask import Blueprint, render_template, request, redirect
import sqlite3

main = Blueprint('main', __name__)

def init_db():
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    contrato TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    prioridad TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@main.route('/')
def index():
    return render_template('formulario.html')

@main.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    contrato = request.form['contrato']
    descripcion = request.form['descripcion']
    categoria = request.form['categoria']
    prioridad = request.form['prioridad']

    if not all([nombre, contrato, descripcion, categoria, prioridad]):
        return "Error: Todos los campos son obligatorios", 400

    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()
    c.execute("INSERT INTO tickets (nombre, contrato, descripcion, categoria, prioridad) VALUES (?, ?, ?, ?, ?)",
              (nombre, contrato, descripcion, categoria, prioridad))
    conn.commit()
    conn.close()

    return render_template('confirmacion.html', nombre=nombre)
