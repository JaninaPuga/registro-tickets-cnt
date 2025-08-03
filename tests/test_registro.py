import pytest
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_formulario_carga(client):
    response = client.get('/')
    print("\n[DEBUG] Código de respuesta (GET /):", response.status_code)
    print("[DEBUG] HTML recibido:\n", response.data.decode())
    assert response.status_code == 200
    assert b'Formulario de Ticket' in response.data

def test_registro_ticket_valido(client):
    data = {
        'nombre': 'Juan',
        'contrato': '12345',
        'descripcion': 'Falla en internet',
        'categoria': 'Conectividad',
        'prioridad': 'Alta'
    }
    response = client.post('/registrar', data=data)
    print("\n[DEBUG] Código de respuesta (POST /registrar válido):", response.status_code)
    print("[DEBUG] HTML recibido:\n", response.data.decode())
    assert response.status_code == 200
    assert b'Ticket registrado exitosamente' in response.data

def test_registro_ticket_incompleto(client):
    data = {
        'nombre': '',
        'contrato': '12345',
        'descripcion': '',
        'categoria': 'Conectividad',
        'prioridad': 'Alta'
    }
    response = client.post('/registrar', data=data)
    print("\n[DEBUG] Código de respuesta (POST /registrar incompleto):", response.status_code)
    assert response.status_code == 400
