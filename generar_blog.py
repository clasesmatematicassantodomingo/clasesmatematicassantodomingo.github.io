import json
import os
import csv
import time
from datetime import datetime
from google import genai

DOMINIO_BASE = "https://clasesmatematicassantodomingo.github.io/"
NUMERO_WHATSAPP = "593993117800"
CSV_PATH = "url_articulos.csv"
KEYWORDS_FILE = "keywords.json"
BLOG_DIR = "blog/"
YOUTUBE_CANAL = "https://www.youtube.com/channel/UCanMxWvOoiwtjLYm08Bo8QQ"
KHAN_ACADEMY = "https://es.khanacademy.org/"

print("Iniciando generación masiva con Estructura SEO Romuald Fons y 3 imágenes...")

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

def generar_texto_con_gemini(keyword, long_tails, related_questions, max_intentos=4):
    raw_key = os.getenv("GEMINI_API_KEY")
    if not raw_key:
        print("Error: No se encontró la variable de entorno GEMINI_API_KEY.")
        return None
    
    api_key = raw_key.strip()
    client = genai.Client(api_key=api_key)
    
    long_tails_str = json.dumps(long_tails, ensure_ascii=False)
    related_str = json.dumps(related_questions, ensure_ascii=False)

    prompt = f"""
Actúa como un redactor SEO senior de alto rendimiento y un profesor experto aplicando el estilo directo, incisivo, agresivo y sin rodeos de Romuald Fons. Escribe para retener usuarios, usando párrafos cortos (máximo 3 líneas), negritas obligatorias en conceptos clave y un ritmo de lectura rápido y adictivo.

Escribe un artículo ultra completo de más de 1200 palabras centrado en la keyword principal: "{keyword}".

Las subsecciones secundarias (long tails) obligatorias son:
{long_tails_str}

Preguntas frecuentes:
{related_str}

Requisitos estrictos de redacción:
1. "intro": 4 párrafos cortos y directos al dolor del estudiante en Santo Domingo, Ecuador (miedo a perder el año, supletorios, dinero tirado en academias malas). Usa **negritas** en la keyword principal y términos clave.
2. "por_que": 3 párrafos destruyendo los métodos tradicionales de enseñanza con un tono desafiante.
3. "long_tails_desarrollo": Lista de bloques con H3, H4 opcional, párrafos cortos y viñetas (bullet points) usando HTML <ul><li> con **negritas** destacadas.
4. "ejercicios_practicos": Resolución visual y paso a paso de un problema real.
5. "faqs_desarrollo": Preguntas frecuentes con respuestas al grano.
6. "conclusion": Cierre contundente con llamado a la acción agresivo a WhatsApp.

Devuelve EXCLUSIVAMENTE en formato JSON puro (sin ```json):
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

    for intento in range(1, max_intentos + 1):
        try:
            print(f"Intentando conectar con Gemini (Intento {intento}/{max_intentos})...")
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            elif raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            return json.loads(raw_text.strip())
        except Exception as e:
            print(f"⚠️ Advertencia en intento {intento}: {e}")
            if intento < max_intentos:
                tiempo_espera = 15 * intento
                print(f"Esperando {tiempo_espera} segundos para reintentar...")
                time.sleep(tiempo_espera)
            else:
                print("❌ Se agotaron los reintentos.")
                return None

def main():
    if not os.path.exists(KEYWORDS_FILE):
        print("No se encontró keywords.json")
        return

    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        keywords_data = json.load(f)

    if not keywords_data:
        print("El archivo está vacío.")
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

    # 3 URLs de imágenes temáticas distribuidas en el diseño
    img_hero = "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80"
    img_mid = "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=1200&q=80"
    img_bottom = "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80"

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="description" content="Domina {keyword} en Santo Domingo con métodos directos y profesores expertos. ¡Resultados garantizados!">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .keyword-negrita {{ color: #0f172a; font-weight: 800; background-color: #fef08a; padding: 0 4px; border-radius: 4px; }}
        strong {{ font-weight: 700; color: #1e1b4b; }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 font-sans leading-relaxed">
    <header class="bg-indigo-950 text-white py-5 shadow-lg sticky top-0 z-50 border-b border-indigo-900">
        <div class="max-w-4xl mx-auto px-4 flex justify-between items-center">
            <a href="{DOMINIO_BASE}" class="font-extrabold text-lg md:text-xl tracking-tight text-amber-400">Matemáticas Santo Domingo</a>
            <a href="https://wa.me/{NUMERO_WHATSAPP}?text=Hola,%20necesito%20información%20urgente%20sobre%20clases" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-xl font-bold text-sm transition shadow-md">WhatsApp Directo</a>
        </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-12">
        <article class="bg-white p-6 md:p-14 rounded-3xl shadow-xl border border-slate-200">
            <h1 class="text-3xl md:text-5xl font-black text-indigo-950 mb-6 leading-tight tracking-tight">{titulo}</h1>
            
            <!-- Índice Interactivos Estilo Fons -->
            <nav class="bg-slate-900 text-white p-6 rounded-2xl mb-10 shadow-md">
                <h2 class="text-base font-bold text-amber-400 uppercase tracking-wider mb-3">Índice del Contenido</h2>
                <ul class="grid md:grid-cols-2 gap-2 text-sm font-medium text-slate-300">
                    <li>👉 <a href="#introduccion" class="hover:underline text-white">El Dolor y la Realidad</a></li>
                    <li>👉 <a href="#problema" class="hover:underline text-white">Por qué fallas en matemáticas</a></li>
                    <li>👉 <a href="#desarrollo" class="hover:underline text-white">Estrategias y Claves SEO</a></li>
                    <li>👉 <a href="#ejercicios" class="hover:underline text-white">Caso Práctico Resuelto</a></li>
                    <li>👉 <a href="#faqs" class="hover:underline text-white">Preguntas Frecuentes</a></li>
                </ul>
            </nav>
            
            <!-- Imagen 1: Hero Principal -->
            <div class="mb-10">
                <img src="{img_hero}" alt="{keyword}" class="w-full h-80 object-cover rounded-2xl shadow-inner border border-slate-100">
            </div>

            <!-- Introducción -->
            <section id="introduccion" class="space-y-4 mb-12 text-lg text-slate-700">
                {f"<p>{'</p><p>'.join(datos_articulo.get('intro', '').split('... '))}</p>"}
                <p class="p-4 bg-indigo-50 border-l-4 border-indigo-600 rounded-r-xl text-slate-800 font-medium">
                    Si quieres complementar tu estudio con teoría formal, revisa la plataforma global de <a href="{url_externo}" target="_blank" class="text-indigo-700 underline font-bold">Khan Academy</a>.
                </p>
            </section>

            <!-- Bloque de Agitación / Problema -->
            <section id="problema" class="bg-amber-50/70 border border-amber-200 p-8 rounded-2xl mb-12 shadow-sm">
                <h2 class="text-2xl font-black text-amber-900 mb-4">¿Por qué los métodos tradicionales te están haciendo perder el año?</h2>
                <div class="space-y-4 text-slate-800 text-base">
                    {f"<p>{'</p><p>'.join(datos_articulo.get('por_que', '').split('... '))}</p>"}
                </div>
            </section>

            <!-- Imagen 2: Mitad del artículo -->
            <div class="mb-12">
                <img src="{img_mid}" alt="Estudiante resolviendo problemas" class="w-full h-72 object-cover rounded-2xl shadow-md">
            </div>

            <!-- Desarrollo Long Tails -->
            <section id="desarrollo" class="space-y-12 mb-12">
"""

    for seccion in datos_articulo.get("long_tails_desarrollo", []):
        h4_html = f"<h4 class='text-lg font-bold text-indigo-950 mt-4 mb-2'>{seccion.get('h4')}</h4>" if seccion.get('h4') else ""
        html_content += f"""
                <div class="border-b border-slate-100 pb-8 space-y-4">
                    <h3 class="text-2xl font-black text-indigo-950">{seccion.get('h3')}</h3>
                    {h4_html}
                    <div class="space-y-3 text-slate-700 text-base">
                        {f"<p>{'</p><p>'.join(seccion.get('contenido', '').split('... '))}</p>"}
                    </div>
                </div>
"""

    ejercicio = datos_articulo.get("ejercicios_practicos", {})
    html_content += f"""
            </section>

            <!-- Ejercicio Práctico -->
            <section id="ejercicios" class="bg-slate-900 text-white p-8 md:p-10 rounded-3xl mb-12 shadow-xl border border-slate-800">
                <h2 class="text-2xl font-black mb-4 text-amber-400">{ejercicio.get('titulo', 'Caso Práctico')}</h2>
                <p class="text-slate-300 mb-6 leading-relaxed">{ejercicio.get('explicacion', '')}</p>
                <div class="bg-indigo-950 p-5 rounded-2xl border border-indigo-800 flex flex-col sm:flex-row justify-between items-center gap-4">
                    <span class="text-sm font-bold text-indigo-200">¿Necesitas ver la explicación paso a paso en video?</span>
                    <a href="{url_youtube}" target="_blank" class="bg-red-600 hover:bg-red-700 text-white font-black px-6 py-3 rounded-xl transition text-sm shadow">Ver Explicación en YouTube</a>
                </div>
            </section>

            <!-- Imagen 3: Cierre / Contexto Estudiantil -->
            <div class="mb-12">
                <img src="{img_bottom}" alt="Clases particulares en Santo Domingo" class="w-full h-72 object-cover rounded-2xl shadow-md">
            </div>

            <!-- Preguntas Frecuentes -->
            <section id="faqs" class="mb-12">
                <h2 class="text-2xl font-black text-indigo-950 mb-6">Preguntas Frecuentes (FAQs)</h2>
                <div class="space-y-4">
"""

    for faq in datos_articulo.get("faqs_desarrollo", []):
        html_content += f"""
                    <div class="bg-slate-50 p-6 rounded-2xl border border-slate-200 shadow-sm">
                        <h3 class="font-bold text-lg text-indigo-950 mb-2">{faq.get('pregunta')}</h3>
                        <p class="text-slate-700">{faq.get('respuesta')}</p>
                    </div>
"""

    html_content += f"""
                </div>
            </section>

            <!-- Enlaces de interés -->
            <section class="bg-indigo-50/80 p-6 rounded-2xl border border-indigo-100 mb-10">
                <h3 class="text-lg font-black text-indigo-950 mb-3">Artículos y Enlaces Relacionados</h3>
                <ul class="list-disc list-inside space-y-2 text-slate-700 font-medium">
                    <li>Descubre nuestros <a href="{url_planes}" class="text-indigo-700 underline font-bold">planes de asesoría y refuerzo académico</a>.</li>
                    <li>Vuelve al inicio en <a href="{url_landing}" class="text-indigo-700 underline font-bold">Clases de Matemáticas Santo Domingo</a>.</li>
                    <li>Lee nuestra guía anterior: <a href="{url_articulo_anterior}" class="text-indigo-700 underline font-bold">{titulo_articulo_anterior}</a>.</li>
                </ul>
            </section>

            <!-- CTA Final Agresivo -->
            <section class="bg-gradient-to-br from-indigo-950 to-indigo-900 text-white p-8 md:p-12 rounded-3xl text-center space-y-6 shadow-2xl">
                <h2 class="text-2xl md:text-4xl font-black tracking-tight">¿Vas a dejar que un examen arruine tu futuro profesional?</h2>
                <div class="space-y-3 text-indigo-100 max-w-2xl mx-auto text-lg">
                    {f"<p>{'</p><p>'.join(datos_articulo.get('conclusion', '').split('... '))}</p>"}
                </div>
                <div class="pt-4">
                    <a href="https://wa.me/{NUMERO_WHATSAPP}?text=Hola,%20quiero%20asegurar%20mi%20cupo%20con%20un%20profesor%20experto" class="inline-block bg-green-500 hover:bg-green-600 text-white font-black px-8 py-4 rounded-2xl shadow-xl transition text-lg transform hover:-translate-y-1">¡Reserva tu cupo de inmediato por WhatsApp!</a>
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
    print(f"¡Artículo generado con éxito bajo estructura Romuald Fons: {ruta_archivo}!")

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
