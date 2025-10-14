from google import genai
import requests
import schedule
import time
import threading
import os
from flask import Flask

# === CONFIGURACIÓN DEL BOT ===
TOKEN = "8269117040:AAEme6PT8QprX_hW4leq2CTkn4EHtHqZ1d4"
CHAT_ID = "5817440886"  # 💗 Chat ID de Fernanda
PING_URL = "https://bot-fer.onrender.com"  # ⚠️ Reemplaza con la URL pública de tu app Render

# === GENERAR FRASE CON GEMINI ===
client = genai.Client(api_key="AIzaSyA1DR-hsQHYeY7ixUY3fJxJH_6Mt5yDWe0")

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

MENSAJE = response.text

# === FUNCIÓN PARA ENVIAR EL MENSAJE ===
def enviar_mensaje():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": MENSAJE}
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("✅ Mensaje enviado correctamente")
    else:
        print("❌ Error al enviar mensaje:", response.text)

# === FUNCIÓN AUTO-PING PARA MANTENER EL BOT DESPIERTO ===
def auto_ping():
    while True:
        try:
            res = requests.get(PING_URL)
            print(f"🔁 Auto-ping ejecutado: {res.status_code}")
        except Exception as e:
            print(f"⚠️ Error en auto-ping: {e}")
        time.sleep(600)  # cada 10 minutos

# === PROGRAMAR ENVÍO DIARIO ===
schedule.every(24).hours.do(enviar_mensaje)

# Enviar primer mensaje al iniciar
enviar_mensaje()

# === SERVIDOR FLASK PARA MANTENERLO ACTIVO EN RENDER ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot activo 💙", 200

if __name__ == "__main__":
    # Iniciar auto-ping en segundo plano
    threading.Thread(target=auto_ping, daemon=True).start()
    
    print("🤖 Bot iniciado... enviando mensajes cada 24 horas y auto-ping activo.")
    
    # Iniciar Flask
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))), daemon=True).start()

    # Bucle principal
    while True:
        schedule.run_pending()
        time.sleep(60)

