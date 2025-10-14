from google import genai
import requests
import schedule
import time
import threading
import os
from flask import Flask, request

# === CONFIGURACIÓN ===
TOKEN = "8269117040:AAEme6PT8QprX_hW4leq2CTkn4EHtHqZ1d4"
PING_URL = "https://bot-fer.onrender.com"  # tu URL pública en Render
client = genai.Client(api_key="AIzaSyA1DR-hsQHYeY7ixUY3fJxJH_6Mt5yDWe0")

# Lista de usuarios registrados
usuarios = set()

# === FUNCIÓN PARA ENVIAR MENSAJE ===
def enviar_mensaje(chat_id, texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": texto}
    requests.post(url, data=data)

# === GENERAR FRASE CON GEMINI ===
def generar_frase():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            "María Fernanda es mi pareja, tiene 19 años y estudia educación infantil. "
            "Ama los colores azul y negro, los peluches, las caricaturas para niños pequeños y el chocolate. "
            "Tiene una energía nostálgica pero muy tierna. Es sensible, dulce y cariñosa, "
            "aunque a veces duda de sí misma y aún siente el dolor de haber perdido a su mamá. "
            "Quiero que le envíes una frase motivacional del día que la llene de vida y esperanza, "
            "que le recuerde lo valiosa que es y le haga sentir acompañada, amada y con fuerzas para seguir sonriendo. "
            "Usa un tono cálido, tierno y levemente romántico, con emojis suaves y delicados (🌷💙🐻✨🍫), "
            "y si puedes, menciónala cariñosamente como 'mi reina' dentro de la frase. "
            "No menciones que eres una IA, ni des explicaciones, ni escribas más texto del necesario; "
            "solo devuelve la frase final, lista para enviarle."
        )
    )
    return response.text

# === ENVIAR MENSAJE A TODOS LOS USUARIOS ===
def enviar_a_todos():
    mensaje = generar_frase()
    for chat_id in usuarios:
        enviar_mensaje(chat_id, mensaje)
    print(f"✅ Mensaje enviado a {len(usuarios)} usuarios")

# === AUTO-PING PARA MANTENER ACTIVO ===
def auto_ping():
    while True:
        try:
            requests.get(PING_URL)
            print("🔁 Auto-ping ejecutado")
        except Exception as e:
            print(f"⚠️ Error en auto-ping: {e}")
        time.sleep(600)

# === FLASK APP PARA RECIBIR MENSAJES DEL BOT ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot activo 💙", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def recibir_update():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if chat_id not in usuarios:
            usuarios.add(chat_id)
            enviar_mensaje(chat_id, "¡Hola! 💙 Ahora recibirás frases motivacionales cada 30 minutos.")
            print(f"🆕 Nuevo usuario registrado: {chat_id}")
    return "ok", 200

# === PROGRAMAR ENVÍO CADA 30 MINUTOS ===
schedule.every(30).minutes.do(enviar_a_todos)

# === AUTO-PING EN HILO SEPARADO ===
threading.Thread(target=auto_ping, daemon=True).start()

# === BUCLE PRINCIPAL ===
def ejecutar_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=ejecutar_schedule, daemon=True).start()

if __name__ == "__main__":
    from flask import Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

