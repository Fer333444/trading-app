import openai
import os

# Obtener la API Key desde la variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: No se encontró la API Key.")
else:
    print("API Key detectada, probando conexión...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hola, ¿cómo estás?"}]
        )
        print("Respuesta de ChatGPT:", response["choices"][0]["message"]["content"])
    except Exception as e:
        print("Error al conectar con OpenAI:", e)
