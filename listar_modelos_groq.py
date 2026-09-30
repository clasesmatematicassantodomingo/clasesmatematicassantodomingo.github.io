import os
from openai import OpenAI

api_key = os.getenv("GROQ_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

print(" Modelos disponibles en tu cuenta de Groq:\n")
try:
    models = client.models.list()
    for model in models.data:
        print(f"  ✅ {model.id} - {getattr(model, 'owned_by', 'desconocido')}")
except Exception as e:
    print(f"❌ Error: {e}")
