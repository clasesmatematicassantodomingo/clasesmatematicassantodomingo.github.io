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
ESTADO_FILE = "estado_generacion.json"
YOUTUBE_CANAL = "https://www.youtube.com/channel/UCanMxWvOoiwtjLYm08Bo8QQ"
KHAN_ACADEMY = "https://es.khanacademy.org/"

print("Iniciando generación masiva de artículos SEO (Sistema de Reintentos con Fallback)...")

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

def cargar_estado():
    if os.path.exists(ESTADO_FILE):
        with open(ESTADO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "keyword_pendiente": None,
        "intentos_fallidos": 0,
        "ultimo_exito": None,
        "dias_desde_exito": 0,
        "keyword_actual": None,
        "slug_actual": None,
        "titulo_actual": None,
        "long_tails_actual": [],
        "related_questions_actual": []
    }

def guardar_estado(estado):
    with open(ESTADO_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)

def generar_texto_con_gemini(keyword, long_tails, related_questions, max_intentos_por_modelo=2):
    raw_key = os.getenv("GEMINI_API_KEY")
    if not raw_key:
        print("Error: No se encontró la variable de entorno GEMINI_API_KEY.")
        return None
    
    api_key = raw_key.strip()
    client = genai.Client(api_key=api_key)
    
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

    # Lista de modelos en orden de preferencia (Fallback automático)
    modelos = ['gemini-3.8-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
    tiempos_espera = [30, 60, 90]

    for modelo_actual in modelos:
        print(f"🔄 Probando modelo: {modelo_actual}")
        
        for intento in range(1, max_intentos_por_modelo + 1):
            try:
                print(f"  Intento {intento}/{max_intentos_por_modelo} con {modelo_actual}...")
                
                response = client.models.generate_content(
                    model=modelo_actual,
                    contents=prompt,
                )
                
                raw_text = response.text.strip()
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:]
                elif raw_text.startswith("```"):
                    raw_text = raw_text[3:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                
                print(f"✅ Éxito con {modelo_actual} en el intento {intento}")
                return json.loads(raw_text.strip())
                
            except json.JSONDecodeError as e:
                print(f"❌ Error: La API no devolvió un JSON válido con {modelo_actual}.")
                print(f"Respuesta cruda: {response.text[:300]}...")
                return None # Error de formato, no reintentar el mismo modelo
                
            except Exception as e:
                error_msg = str(e)
                if '503' in error_msg or 'UNAVAILABLE' in error_msg or '429' in error_msg:
                    tiempo_espera = tiempos_espera[intento - 1] if (intento - 1) < len(tiempos_espera) else 90
                    print(f"⚠️ {modelo_actual} saturado. Esperando {tiempo_espera} segundos...")
                    time.sleep(tiempo_espera)
                elif '404' in error_msg or 'NOT_FOUND' in error_msg:
                    print(f"❌ Modelo {modelo_actual} no disponible (404). Pasando al siguiente modelo...")
                    break # Rompe el bucle de este modelo y pasa al siguiente en la lista
                else:
                    print(f"❌ Error inesperado con {modelo_actual}: {e}")
                    break
        
        print(f"⚠️ {modelo_actual} agotó sus intentos. Probando siguiente modelo...")
    
    print("❌ Todos los modelos fallaron. Se reintentará mañana.")
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

    estado = cargar_estado()
    historial, keywords_publicadas = obtener_historial_articulos()

    # Calcular días desde el último éxito
    if estado.get("ultimo_exito"):
        fecha_ultimo_exito = datetime.fromisoformat(estado["ultimo_exito"])
        dias_desde_exito = (datetime.now() - fecha_ultimo_exito).days
        estado["dias_desde_exito"] = dias_desde_exito
    else:
        dias_desde_exito = 999

    # CASO 1: Hubo éxito hace menos de 3 días → NO hacer nada
    if dias_desde_exito < 3:
        print(f"✅ Último éxito hace {dias_desde_exito} día(s). Esperando {3 - dias_desde_exito} día(s) más.")
        guardar_estado(estado)
        return

    # CASO 2: Hay keyword pendiente de reintentar
    if estado.get("keyword_pendiente") and estado.get("intentos_fallidos", 0) < 3:
        print(f"🔄 Reintentando keyword pendiente: {estado['keyword_pendiente']} (Intento fallido acumulado: {estado['intentos_fallidos']}/3)")
        
        keyword = estado["keyword_pendiente"]
        slug = estado["slug_actual"]
        titulo = estado["titulo_actual"]
        long_tails = estado["long_tails_actual"]
        related_questions = estado["related_questions_actual"]
        
        datos_articulo = generar_texto_con_gemini(keyword, long_tails, related_questions)
        
        if datos_articulo:
            print(f"✅ Artículo generado en reintento: {slug}")
            estado["keyword_pendiente"] = None
            estado["intentos_fallidos"] = 0
            estado["ultimo_exito"] = datetime.now().isoformat()
            estado["dias_desde_exito"] = 0
            
            for idx, item in enumerate(keywords_data):
                if item.get("keyword_principal", "").strip().lower() == keyword.strip().lower():
                    keyword_usada = keywords_data.pop(idx)
                    keywords_data.append(keyword_usada)
                    break
            
            with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                json.dump(keywords_data, f, ensure_ascii=False, indent=2)
            
            generar_html(titulo, slug, keyword, datos_articulo, historial)
            
            file_exists = os.path.exists(CSV_PATH)
            with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                if not file_exists:
                    writer.writerow(["Fecha", "Keyword", "URL"])
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), keyword, f"{DOMINIO_BASE}blog/{slug}.html"])
            
            guardar_estado(estado)
            print("✅ Proceso completado exitosamente.")
            return
        else:
            estado["intentos_fallidos"] += 1
            print(f"⚠️ Reintento fallido. Total intentos fallidos: {estado['intentos_fallidos']}/3")
            
            if estado["intentos_fallidos"] >= 3:
                print("❌ 3 días consecutivos fallidos. Rotando keyword para no bloquear el sistema.")
                for idx, item in enumerate(keywords_data):
                    if item.get("keyword_principal", "").strip().lower() == keyword.strip().lower():
                        keyword_usada = keywords_data.pop(idx)
                        keywords_data.append(keyword_usada)
                        break
                
                with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
                    json.dump(keywords_data, f, ensure_ascii=False, indent=2)
                
                estado["keyword_pendiente"] = None
                estado["intentos_fallidos"] = 0
                estado["ultimo_exito"] = datetime.now().isoformat()
                estado["dias_desde_exito"] = 0
            
            guardar_estado(estado)
            return

    # CASO 3: No hay keyword pendiente → Seleccionar nueva
    print("📌 Seleccionando nueva keyword para generar...")
    
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

    estado["keyword_pendiente"] = keyword
    estado["intentos_fallidos"] = 0
    estado["keyword_actual"] = keyword
    estado["slug_actual"] = slug
    estado["titulo_actual"] = titulo
    estado["long_tails_actual"] = long_tails
    estado["related_questions_actual"] = related_questions
    guardar_estado(estado)

    datos_articulo = generar_texto_con_gemini(keyword, long_tails, related_questions)
    
    if not datos_articulo:
        print("⚠️ No se pudo generar el contenido hoy. Se reintentará mañana.")
        estado["intentos_fallidos"] = 1
        guardar_estado(estado)
        return

    print(f"✅ Artículo generado con éxito en el primer intento: {slug}")
    
    keyword_usada = keywords_data.pop(indice_a_remover)
    keywords_data.append(keyword_usada)

    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(keywords_data, f, ensure_ascii=False, indent=2)

    generar_html(titulo, slug, keyword, datos_articulo, historial)

    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(["Fecha", "Keyword", "URL"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), keyword, f"{DOMINIO_BASE}blog/{slug}.html"])
    print("Registro agregado al archivo CSV de control.")

    estado["keyword_pendiente"] = None
    estado["intentos_fallidos"] = 0
    estado["ultimo_exito"] = datetime.now().isoformat()
    estado["dias_desde_exito"] = 0
    guardar_estado(estado)

def generar_html(titulo, slug, keyword, datos_articulo, historial):
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

if __name__ == "__main__":
    main()
