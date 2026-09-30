import json
import os
import csv
import time
from datetime import datetime
from openai import OpenAI

DOMINIO_BASE = "https://clasesmatematicassantodomingo.github.io/"
NUMERO_WHATSAPP = "593993117800"
CSV_PATH = "url_articulos.csv"
KEYWORDS_FILE = "keywords.json"
BLOG_DIR = "blog/"
YOUTUBE_CANAL = "https://www.youtube.com/channel/UCanMxWvOoiwtjLYm08Bo8QQ"
KHAN_ACADEMY = "https://es.khanacademy.org/"

print("Iniciando generación masiva de artículos SEO avanzados (Groq Ultra-Fast)...")

def obtener_historial_articulos():
    articulos_previos = []
    keywords_publicadas = set()
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    articulos_previos.append({"fecha": row[0], "keyword": row[1], "url": row[2]})
                    keywords_publicadas.add(row[1].strip().lower())
    return articulos_previos, keywords_publicadas

def generar_texto_con_gemini(keyword, long_tails, related_questions, max_intentos=3):
    raw_key = os.getenv("GROQ_API_KEY")
    if not raw_key:
        print("Error: No se encontró la variable de entorno GROQ_API_KEY.")
        return None
    
    api_key = raw_key.strip()
    
    # Cliente OpenAI configurado para Groq
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    long_tails_str = json.dumps(long_tails, ensure_ascii=False)
    related_str = json.dumps(related_questions, ensure_ascii=False)

    prompt = f"""
Actúa como un profesor experto de matemáticas y redactor SEO senior especializado en rendimiento académico en Santo Domingo, Ecuador. Aplica el estilo directo, incisivo, apasionado y sin rodeos de Romuald Fons (SEO de guerrilla: cero paja, directo al dolor del usuario, alta densidad de valor).

Escribe un artículo de más de 1200 palabras centrado en la keyword principal: "{keyword}".

Las subsecciones secundarias (long tails) a integrar de forma NATURAL son:
{long_tails_str}

Preguntas frecuentes a responder:
{related_str}

Requisitos estrictos de ESTRUCTURA y JERARQUÍA (OBLIGATORIO):
1. "intro": 3-4 párrafos. Empieza agitando el dolor (miedo a los supletorios, frustración). No uses frases genéricas como "En este artículo". Menciona el contexto local de Santo Domingo.
2. "por_que": 2-3 párrafos explicando por qué las academias masivas hacen perder tiempo y dinero por falta de personalización.
3. "long_tails_desarrollo": Genera 3 bloques (H3) que integren las keywords de forma natural. Ejemplos de H3: "Señales de que necesitas un profesor a domicilio YA", "Cómo la preparación para supletorios marca la diferencia", "La ventaja de un profesor de matemáticas en Santo Domingo". Cada bloque debe tener 3-4 párrafos con ejemplos prácticos locales.
4. "ejercicios_practicos": Resolución paso a paso de un problema típico, explicando la lógica, no solo la fórmula.
5. "faqs_desarrollo": Responde a las preguntas proporcionadas con 2 párrafos detallados y útiles por pregunta.
6. "conclusion": 2-3 párrafos con una Llamada a la Acción (CTA) urgente y directa a WhatsApp.

REGLAS DE ESTILO ROMUALD FONS:
- Usa **negritas** estratégicamente (1-2 por párrafo) en frases clave que contengan long-tail keywords.
- Frases cortas, párrafos separados por saltos de línea dobles (\n\n) para facilitar la lectura.
- Tono: Empático pero firme, de autoridad, como un mentor que tiene la solución.
- Devuelve EXCLUSIVAMENTE JSON puro (sin bloques ```json), con esta estructura exacta:
{{
  "intro": "...",
  "por_que": "...",
  "long_tails_desarrollo": [
    {{
      "h3": "...",
      "h4": "...",
      "contenido": "..."
    }}
  ],
  "ejercicios_practicos": {{
    "titulo": "...",
    "explicacion": "..."
  }},
  "faqs_desarrollo": [
    {{
      "pregunta": "...",
      "respuesta": "..."
    }}
  ],
  "conclusion": "..."
}}
"""

            # Modelos ACTUALES de Groq - formato legacy estable
    modelos = [
        'llama3-70b-8192',           # Legacy estable
        'llama3-8b-8192',            # Legacy ligero
        'meta-llama/llama-4-maverick',  # Formato nuevo con slash
        'meta-llama/llama-4-scout'       # Formato nuevo con slash
    ]

    for modelo_actual in modelos:
        print(f"🔄 Usando modelo: {modelo_actual}")
        
        for intento in range(1, max_intentos + 1):
            try:
                print(f"Intentando conectar con Groq (Intento {intento}/{max_intentos})...")
                
                response = client.chat.completions.create(
                    model=modelo_actual,
                    messages=[
                        {"role": "system", "content": "Eres un experto en SEO y redacción educativa. Responde SOLO con JSON válido, sin bloques de código markdown."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4096,
                )
                
                raw_text = response.choices[0].message.content.strip()
                
                # Limpieza de markdown por si acaso
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:]
                elif raw_text.startswith("```"):
                    raw_text = raw_text[3:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                
                return json.loads(raw_text.strip())
                
            except json.JSONDecodeError as e:
                print(f"❌ Error: La API no devolvió un JSON válido con {modelo_actual}.")
                print(f"Respuesta cruda: {raw_text[:300]}...")
                return None
                
            except Exception as e:
                error_msg = str(e)
                if '429' in error_msg or 'rate' in error_msg.lower():
                    print(f"⚠️ Límite de tasa alcanzado. Esperando 30 segundos...")
                    time.sleep(30)
                elif '404' in error_msg or 'not found' in error_msg.lower():
                    print(f"❌ Modelo {modelo_actual} no disponible. Pasando al siguiente...")
                    break
                else:
                    print(f"❌ Error con {modelo_actual}: {e}")
                    break
        
        print(f"⚠️ Modelo {modelo_actual} agotó reintentos. Probando siguiente modelo...")
    
    print(" Todos los modelos de Groq fallaron.")
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

    historial, keywords_publicadas = obtener_historial_articulos()

    item_actual = None
    indice_a_remover = -1

    for idx, item in enumerate(keywords_data):
        kw = item.get("keyword_principal", "").strip().lower()
        if kw not in keywords_publicadas:
            item_actual = item
            indice_a_remover = idx
            break

    if not item_actual:
        item_actual = keywords_data[0]
        indice_a_remover = 0

    keyword = item_actual.get("keyword_principal")
    slug = item_actual.get("slug")
    titulo = item_actual.get("titulo")
    long_tails = item_actual.get("long_tails", [])
    related_questions = item_actual.get("related_questions", [])

    print(f"Procesando artículo: {keyword} (Slug: {slug})")

    datos_articulo = generar_texto_con_gemini(keyword, long_tails, related_questions)
    if not datos_articulo:
        print("No se pudo generar el contenido.")
        return

    url_planes = f"{DOMINIO_BASE}#planes"
    url_landing = DOMINIO_BASE
    url_externo = KHAN_ACADEMY
    url_youtube = YOUTUBE_CANAL

    url_articulo_anterior = historial[-1]["url"] if historial else DOMINIO_BASE
    titulo_articulo_anterior = historial[-1]["keyword"] if historial else "nuestra guía principal"

    os.makedirs(BLOG_DIR, exist_ok=True)
    ruta_archivo = os.path.join(BLOG_DIR, f"{slug}.html")

    def format_parrafos(texto):
        if not texto:
            return ""
        parrafos = [p.strip() for p in texto.split('\n\n') if p.strip()]
        return f"<p>{'</p><p>'.join(parrafos)}</p>"

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="description" content="Aprende y domina {keyword} en Santo Domingo con clases particulares y refuerzo escolar especializado. Resultados garantizados.">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .keyword-negrita {{ color: #000000; font-weight: 700; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 font-sans leading-relaxed">
    <header class="bg-indigo-950 text-white py-6 shadow-md sticky top-0 z-50">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <a href="{DOMINIO_BASE}" class="font-bold text-xl tracking-wide">Clases de Matemáticas Santo Domingo</a>
            <a href="https://wa.me/{NUMERO_WHATSAPP}?text=Hola,%20necesito%20información%20sobre%20clases%20de%20matemáticas" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg font-semibold text-sm transition shadow">Asesoría WhatsApp</a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-10">
        <article class="bg-white p-8 md:p-12 rounded-2xl shadow-sm border border-slate-200">
            <h1 class="text-3xl md:text-5xl font-extrabold text-indigo-950 mb-6 leading-tight">{titulo}</h1>
            
            <nav class="bg-slate-100 p-6 rounded-xl mb-8 border border-slate-200">
                <h2 class="text-lg font-bold text-slate-900 mb-3">Índice del Artículo</h2>
                <ul class="list-disc list-inside space-y-2 text-indigo-950 font-medium">
                    <li><a href="#introduccion" class="hover:underline">Introducción y Panorama Educativo</a></li>
                    <li><a href="#problema" class="hover:underline">El problema de los métodos tradicionales</a></li>
                    <li><a href="#desarrollo" class="hover:underline">Desarrollo clave y estrategias</a></li>
                    <li><a href="#ejercicios" class="hover:underline">Ejemplo práctico de resolución</a></li>
                    <li><a href="#faqs" class="hover:underline">Preguntas Frecuentes</a></li>
                </ul>
            </nav>
            
            <div class="mb-8">
                <img src="https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80" alt="{keyword}" class="w-full h-80 object-cover rounded-xl shadow-inner">
            </div>

            <section id="introduccion" class="prose max-w-none text-slate-800 space-y-4 mb-10 text-lg">
                {format_parrafos(datos_articulo.get('intro', ''))}
                <p class="mt-4 text-slate-700">Para complementar tu aprendizaje con bases teóricas formales, te recomendamos visitar recursos de referencia internacional como <a href="{url_externo}" target="_blank" class="keyword-negrita underline">Khan Academy</a>.</p>
            </section>

            <section id="problema" class="bg-indigo-50/60 border-l-4 border-indigo-600 p-6 rounded-r-xl mb-10">
                <h2 class="text-2xl font-bold text-indigo-950 mb-4">¿Por qué los métodos tradicionales ya no dan resultados?</h2>
                <div class="space-y-4 text-slate-800">
                    {format_parrafos(datos_articulo.get('por_que', ''))}
                </div>
            </section>

            <section id="desarrollo" class="space-y-10 mb-12">
"""

    for seccion in datos_articulo.get("long_tails_desarrollo", []):
        h4_html = f"<h4 class='text-xl font-semibold text-indigo-900 mt-3'>{seccion.get('h4')}</h4>" if seccion.get('h4') else ""
        contenido_format = format_parrafos(seccion.get('contenido', ''))
        html_content += f"""
                <section class="space-y-4">
                    <h3 class="text-2xl font-bold text-slate-900 border-b pb-2">{seccion.get('h3')}</h3>
                    {h4_html}
                    <div class="space-y-4 text-slate-800">
                        {contenido_format}
                    </div>
                </section>
"""

    ejercicio = datos_articulo.get("ejercicios_practicos", {})
    html_content += f"""
            </section>

            <section id="ejercicios" class="bg-slate-900 text-white p-8 rounded-2xl mb-12 shadow-md">
                <h2 class="text-2xl font-bold mb-4 text-amber-400">{ejercicio.get('titulo', 'Resolución Práctica')}</h2>
                <p class="text-slate-300 mb-6">{ejercicio.get('explicacion', '')}</p>
                <div class="bg-indigo-900/80 p-4 rounded-xl border border-indigo-700 flex flex-col sm:flex-row justify-between items-center gap-4">
                    <span class="text-sm font-medium">¿Quieres dominar este ejercicio visualmente?</span>
                    <a href="{url_youtube}" target="_blank" class="bg-red-600 hover:bg-red-700 text-white font-bold px-5 py-2.5 rounded-lg transition text-sm">Ver en YouTube</a>
                </div>
            </section>

            <section id="faqs" class="mb-12">
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

            <section class="bg-slate-100 p-6 rounded-xl border border-slate-300 mb-10">
                <h3 class="text-xl font-bold text-indigo-950 mb-3">Enlaces de Interés y Siguientes Pasos</h3>
                <ul class="list-disc list-inside space-y-2 text-slate-700">
                    <li>Revisa nuestros <a href="{url_planes}" class="keyword-negrita underline">planes de asesoría y refuerzo escolar personalizados</a>.</li>
                    <li>Vuelve a la página principal en <a href="{url_landing}" class="keyword-negrita underline">Clases de Matemáticas Santo Domingo</a>.</li>
                    <li>Explora nuestro artículo anterior: <a href="{url_articulo_anterior}" class="keyword-negrita underline">{titulo_articulo_anterior}</a>.</li>
                </ul>
            </section>

            <section class="bg-indigo-950 text-white p-8 rounded-2xl text-center space-y-4 shadow-lg">
                <h2 class="text-2xl md:text-3xl font-bold">¿Vas a dejar que un mal promedio arruine tu futuro?</h2>
                <div class="space-y-3 text-indigo-100 max-w-2xl mx-auto">
                    {format_parrafos(datos_articulo.get('conclusion', ''))}
                </div>
                <div class="pt-4">
                    <a href="https://wa.me/{NUMERO_WHATSAPP}?text=Hola,%20quiero%20asegurar%20un%20profesor%20particular" class="inline-block bg-green-500 hover:bg-green-600 text-white font-bold px-8 py-4 rounded-xl shadow-md transition text-lg">¡Reserva tu cupo con profesor experto!</a>
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

    keyword_usada = keywords_data.pop(indice_a_remover)
    keywords_data.append(keyword_usada)

    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(keywords_data, f, ensure_ascii=False, indent=2)

    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(["Fecha", "Keyword", "URL"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), keyword, f"{DOMINIO_BASE}blog/{slug}.html"])
    print("Registro agregado al archivo CSV de control.")

if __name__ == "__main__":
    main()
