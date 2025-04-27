import openai
import os

# Obtener la API Key desde la variable de entorno
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Verificar si la API Key está correctamente configurada
if not api_key:
    print("Error: No se encontró la clave API.")
else:
    print("API Key detectada, probando conexión...")

    try:
        client = openai.Client()  # NUEVA FORMA DE USO
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hola, ¿cómo estás?"}]
        )
        print("Respuesta de ChatGPT:", response.choices[0].message.content)

    except Exception as e:
        print("Error al conectar con OpenAI:", e)
