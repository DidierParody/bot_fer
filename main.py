from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AIzaSyA1DR-hsQHYeY7ixUY3fJxJH_6Mt5yDWe0")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="María Fernanda es mi pareja, tiene 19 años y estudia educación infantil. Ama los colores azul y negro, los peluches, las caricaturas para niños pequeños y el chocolate. Tiene una energía nostálgica pero muy tierna. Es sensible, dulce y cariñosa, aunque a veces duda de sí misma y aún siente el dolor de haber perdido a su mamá. Quiero que le envíes una frase motivacional del día que la llene de vida y esperanza, que le recuerde lo valiosa que es y le haga sentir acompañada, amada y con fuerzas para seguir sonriendo. Usa un tono cálido, tierno y levemente romántico, con emojis suaves y delicados (🌷💙🐻✨🍫), y si puedes, menciónala cariñosamente como “mi reina” dentro de la frase. No menciones que eres una IA, ni des explicaciones, ni escribas más texto del necesario; solo devuelve la frase final, lista para enviarle."
)
print(response.text)


import requests
import schedule
import time

# Configura tus datos
TOKEN = "8269117040:AAEme6PT8QprX_hW4leq2CTkn4EHtHqZ1d4"
CHAT_ID = "7244969577"
MENSAJE = response.text

def enviar_mensaje():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": MENSAJE}
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("✅ Mensaje enviado correctamente")
    else:
        print("❌ Error al enviar mensaje:", response.text)

# Programar el envío cada 24 horas
schedule.every(24).hours.do(enviar_mensaje)

# (Opcional) Para enviar el primer mensaje inmediatamente al iniciar el script
enviar_mensaje()

print("🤖 Bot iniciado... enviando mensajes cada 24 horas")

# Mantener el script corriendo
while True:
    schedule.run_pending()
    time.sleep(60)

