import json
import os
import csv
from datetime import datetime
import urllib.request
import urllib.error

DOMINIO_BASE = "https://clasesmatematicassantodomingo.github.io/"
NUMERO_WHATSAPP = "593993117800"
CSV_PATH = "url_articulos.csv"
KEYWORDS_FILE = "keywords.json"
BLOG_DIR = "blog/"

print("Iniciando generación masiva de artículos SEO avanzados (Estilo Romuald Fons Dinámico)...")

def generar_texto_con_gemini(keyword, long_tails, related_questions):
    raw_key = os.getenv("GEMINI_API_KEY")
    if not raw_key:
        print("Error: No se encontró la variable de entorno GEMINI_API_KEY.")
        return None
    
    api_key = raw_key.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    long_tails_str = json.dumps(long_tails, ensure_ascii=False)
    related_str = json.dumps(related_questions, ensure_ascii=False)

    prompt = f"""
Actúa como un profesor experto de matemáticas y redactor SEO senior especializado en educación y rendimiento académico en Santo Domingo, Ecuador. Aplica el estilo directo, incisivo, persuasivo y estructurado de Romuald Fons (SEO de guerrilla, sin paja, directo al dolor del usuario).

Escribe un artículo extremadamente completo, profundo y de gran extensión (debe superar obligatoriamente las 1000 palabras de contenido de valor real) centrado en la keyword principal: "{keyword}".

Las subsecciones secundarias (long tails) obligatorias que debes desarrollar a profundidad son:
{long_tails_str}

Preguntas frecuentes orientadas a la intención de búsqueda que debes responder de forma natural:
{related_str}

Requisitos estrictos de redacción masiva y dinámica (CERO TEXTO REPETITIVO):
1. "intro": Escribe 4 párrafos largos, persuasivos y detallados abordando el dolor principal del estudiante en Santo Domingo (reprobaciones, la frustración con las matemáticas y el riesgo inminente de perder el año o quedarse a supletorios).
2. "por_que": Escribe 3 párrafos extensos explicando por qué la educación tradicional y las academias masivas fallan estrepitosamente al explicar conceptos abstractos sin conectar con la realidad local del estudiante.
3. "long_tails_desarrollo": Para cada una de las subsecciones (long tails) listadas arriba, redacta un bloque completo con un título H3 optimizado y original, seguido de CUATRO párrafos extensos, técnicos pero accesibles, con ejemplos prácticos aplicados a colegios o situaciones cotidianas en Santo Domingo, Ecuador.
4. "faqs_desarrollo": Responde a cada una de las preguntas frecuentes proporcionadas con dos párrafos detallados por pregunta.
5. "conclusion": Escribe un cierre contundente de 3 párrafos que invite a la acción inmediata mediante WhatsApp.

Devuelve la respuesta EXCLUSIVAMENTE en formato JSON puro, sin bloques de código markdown adicionales (nada de ```json), con esta estructura exacta de llaves:
{{
  "intro": "Párrafo 1... Párrafo 2... Párrafo 3... Párrafo 4...",
  "por_que": "Párrafo 1... Párrafo 2... Párrafo 3...",
  "long_tails_desarrollo": [
    {{
      "h3": "Título H3 optimizado",
      "contenido": "Párrafo 1... Párrafo 2... Párrafo 3... Párrafo 4..."
    }}
  ],
  "faqs_desarrollo": [
    {{
      "pregunta": "Pregunta exacta de la lista",
      "respuesta": "Párrafo 1 detallado... Párrafo 2 detallado..."
    }}
  ],
  "conclusion": "Párrafo 1... Párrafo 2... Párrafo 3..."
}}
"""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            texto_generado = res_json['candidates'][0]['content']['parts'][0]['text']
            return json.loads(texto_generado)
    except Exception as e:
        print(f"Error al conectar con la API de Gemini: {e}")
        return None

def main():
    if not os.path.exists(KEYWORDS_FILE):
        print("No se encontró el archivo keywords.json")
        return

    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        keywords_data = json.load(f)

    if not keywords_data:
        print("El archivo keywords.json está vacío.")
        return

    item_actual = keywords_data[0]
    keyword = item_actual.get("keyword_principal")
    slug = item_actual.get("slug")
    titulo = item_actual.get("titulo")
    long_tails = item_actual.get("long_tails", [])
    related_questions = item_actual.get("related_questions", [])

    print(f"Procesando keyword: {keyword} (Slug: {slug})")

    datos_articulo = generar_texto_con_gemini(keyword, long_tails, related_questions)
    if not datos_articulo:
        print("No se pudo generar el contenido del artículo.")
        return

    os.makedirs(BLOG_DIR, exist_ok=True)
    ruta_archivo = os.path.join(BLOG_DIR, f"{slug}.html")

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="description" content="Aprende y domina {keyword} en Santo Domingo con clases particulares y refuerzo escolar especializado. Resultados garantizados.">
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans leading-relaxed">
    <header class="bg-indigo-900 text-white py-6 shadow-md">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <a href="{DOMINIO_BASE}" class="font-bold text-xl tracking-wide">Clases de Matemáticas Santo Domingo</a>
            <a href="[https://wa.me/](https://wa.me/){NUMERO_WHATSAPP}?text=Hola,%20necesito%20información%20sobre%20clases%20de%20matemáticas" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg font-semibold text-sm transition shadow">Asesoría WhatsApp</a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-10">
        <article class="bg-white p-8 md:p-12 rounded-2xl shadow-sm border border-slate-100">
            <h1 class="text-3xl md:text-4xl font-extrabold text-indigo-950 mb-6 leading-tight">{titulo}</h1>
            
            <div class="mb-8">
                <img src="[https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80](https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80)" alt="{keyword}" class="w-full h-72 object-cover rounded-xl shadow-inner">
            </div>

            <div class="prose max-w-none text-slate-700 space-y-4 mb-10 text-lg">
                {f"<p>{'</p><p>'.join(datos_articulo.get('intro', '').split('... '))}</p>"}
            </div>

            <section class="bg-indigo-50/60 border-l-4 border-indigo-600 p-6 rounded-r-xl mb-10">
                <h2 class="text-2xl font-bold text-indigo-950 mb-4">¿Por qué los métodos tradicionales ya no dan resultados?</h2>
                <div class="space-y-4 text-slate-700">
                    {f"<p>{'</p><p>'.join(datos_articulo.get('por_que', '').split('... '))}</p>"}
                </div>
            </section>

            <div class="space-y-10 mb-12">
"""

    for seccion in datos_articulo.get("long_tails_desarrollo", []):
        html_content += f"""
                <section>
                    <h2 class="text-2xl font-bold text-slate-900 mb-4 border-b pb-2">{seccion.get('h3')}</h2>
                    <div class="space-y-4 text-slate-700">
                        {f"<p>{'</p><p>'.join(seccion.get('contenido', '').split('... '))}</p>"}
                    </div>
                </section>
"""

    html_content += f"""
            </div>

            <section class="mb-12">
                <h2 class="text-2xl font-bold text-indigo-950 mb-6">Preguntas Frecuentes</h2>
                <div class="space-y-6">
"""

    for faq in datos_articulo.get("faqs_desarrollo", []):
        html_content += f"""
                    <div class="bg-slate-50 p-6 rounded-xl border border-slate-200">
                        <h3 class="font-bold text-lg text-slate-900 mb-2">{faq.get('pregunta')}</h3>
                        <p class="text-slate-700">{faq.get('respuesta')}</p>
                    </div>
"""

    html_content += f"""
                </div>
            </section>

            <section class="bg-indigo-900 text-white p-8 rounded-2xl text-center space-y-4 shadow-lg">
                <h2 class="text-2xl md:text-3xl font-bold">¿Vas a dejar que un mal promedio arruine tu futuro profesional?</h2>
                <div class="space-y-3 text-indigo-100 max-w-2xl mx-auto">
                    {f"<p>{'</p><p>'.join(datos_articulo.get('conclusion', '').split('... '))}</p>"}
                </div>
                <div class="pt-4">
                    <a href="[https://wa.me/](https://wa.me/){NUMERO_WHATSAPP}?text=Hola,%20quiero%20asegurar%20un%20profesor%20particular" class="inline-block bg-green-500 hover:bg-green-600 text-white font-bold px-8 py-4 rounded-xl shadow-md transition text-lg">¡Reserva tu cupo con profesor experto!</a>
                </div>
            </section>
        </article>
    </main>

    <footer class="bg-slate-900 text-slate-400 py-8 text-center text-sm border-t border-slate-800 mt-16">
        <p>&copy; {datetime.now().year} Clases de Matemáticas Santo Domingo. Todos los derechos reservados.</p>
    </footer>
</body>
</html>
"""

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"¡Artículo generado con éxito: {ruta_archivo}!")

    keyword_usada = keywords_data.pop(0)
    keywords_data.append(keyword_usada)

    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(keywords_data, f, ensure_ascii=False, indent=2)
    print("Parrilla de keywords actualizada y rotada correctamente.")

    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(["Fecha", "Keyword", "URL"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), keyword, f"{DOMINIO_BASE}blog/{slug}.html"])
    print("Registro agregado al archivo CSV de control.")

if __name__ == "__main__":
    main()
