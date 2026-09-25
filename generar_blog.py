import json
import os
import csv
from datetime import datetime
import urllib.request
import urllib.error

DOMINIO_BASE = "https://clasesmatematicassantodomingo.github.io/"
NUMERO_WHATSAPP = "593993117800"
csv_path = "urls_articulos.csv"
api_key = os.environ.get("GEMINI_API_KEY")

print("Iniciando generación de blog con IA de Gemini (Estilo Romuald Fons)...")

def generar_texto_con_gemini(keyword, long_tails):
    if not api_key:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    long_tails_str = json.dumps(long_tails, ensure_ascii=False)
    
    prompt = """
    Actúa como un profesor experto de matemáticas y redactor SEO senior especializado en educación en Santo Domingo, Ecuador. Aplica el estilo directo, persuasivo y estructurado de Romuald Fons: párrafos cortos de lectura ágil, foco total en la intención de búsqueda, autoridad y resolución de dolores del usuario.
    Escribe un artículo extremadamente completo, profundo y de gran extensión (mínimo 1000 palabras) sobre la keyword principal: "{keyword}".
    Las subsecciones secundarias (long tails) que debes desarrollar obligatoriamente son:
    {long_tails_json}

    Requisitos estrictos de redacción:
    1. "intro": Escribe 3 párrafos persuasivos abordando el dolor principal del estudiante en Santo Domingo (malas notas, frustración con las matemáticas y el riesgo de perder el año).
    2. "por_que": Escribe 2 párrafos explicando por qué los métodos educativos tradicionales y las academias masivas fallan.
    3. "long_tails_desarrollo": Para cada una de las subsecciones (long tails) listadas arriba, redacta un bloque con un título H3 optimizado, y TRES párrafos largos, técnicos y prácticos por cada sección.
    4. Devuelve la respuesta EXCLUSIVAMENTE en formato JSON puro, sin bloques de código markdown adicionales, con esta estructura exacta de llaves:
    {{
      "intro": "Párrafo 1... Párrafo 2... Párrafo 3...",
      "por_que": "Párrafo 1... Párrafo 2...",
      "long_tails_desarrollo": [
        {{"h3": "Título H3 optimizado 1", "p1": "párrafo 1 detallado...", "p2": "párrafo 2 detallado...", "p3": "párrafo 3 detallado..."}},
        {{"h3": "Título H3 optimizado 2", "p1": "párrafo 1 detallado...", "p2": "párrafo 2 detallado...", "p3": "párrafo 3 detallado..."}}
      ]
    }}
    """.format(keyword=keyword, long_tails_json=long_tails_str)

    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            texto_generado = res_json["candidates"][0]["content"]["parts"][0]["text"]
            
            texto_limpio = texto_generado.strip()
            if texto_limpio.startswith("```json"):
                texto_limpio = texto_limpio[7:]
            if texto_limpio.endswith("```"):
                texto_limpio = texto_limpio[:-3]
                
            return json.loads(texto_limpio.strip())
    except Exception as e:
        print(f"Error al conectar con la API de Gemini: {e}")
        return None

# 1. Cargar la parrilla de keywords
if not os.path.exists("keywords.json"):
    print("Error crítico: El archivo keywords.json no existe.")
    exit()

with open("keywords.json", "r", encoding="utf-8") as f:
    keywords_data = json.load(f)

if keywords_data:
    articulo_actual = keywords_data.pop(0)

    keyword_principal = articulo_actual.get("keyword_principal")
    long_tails = articulo_actual.get("long_tails", [])
    titulo = articulo_actual.get("titulo")
    slug = articulo_actual.get("slug", "articulo-matematicas-santo-domingo")

    print(f"Procesando artículo SEO: {titulo}")

    url_articulo = f"{DOMINIO_BASE}blog/{slug}.html"
    extracto_card = f"Guía experta y definitiva sobre {keyword_principal} en Santo Domingo con métodos de enseñanza personalizados para asegurar tus notas."

    imagenes_banco = [
        "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80"
    ]
    imagen_url = imagenes_banco[len(slug) % len(imagenes_banco)]

    # Cargar historial CSV para Interlinking
    historial_posts = []
    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2 and row[1] != slug:
                    historial_posts.append((row[0], f"../blog/{row[1]}.html"))

    enlace_interno_html = ""
    if historial_posts:
        titulo_prev, url_prev = historial_posts[0]
        enlace_interno_html = f'<p style="margin-top: 1.5rem; font-size: 1.05rem; line-height: 1.7;">Te invitamos a revisar también nuestra guía especializada sobre <a href="{url_prev}" style="color: #0b2545; font-weight: bold; text-decoration: underline;">{titulo_prev}</a> para dominar por completo tus evaluaciones académicas.</p>'

    contenido_ia = generar_texto_con_gemini(keyword_principal, long_tails)
    
    if not contenido_ia:
        print("Usando contenido estructurado de respaldo...")
        contenido_ia = {
            "intro": f"Enfrentarse a materias complejas sin una guía adecuada en Santo Domingo suele terminar en reprobaciones y horas de desgaste innecesario frente a los libros. Dominar {keyword_principal} exige un cambio drástico de perspectiva, pasando de la memorización mecánica a la comprensión lógica y aplicada.",
            "por_que": f"El sistema de enseñanza tradicional en colegios y academias masivas ignora por completo el ritmo de aprendizaje individual del estudiante, generando bloqueos mentales severos.",
            "long_tails_desarrollo": [{"h3": f"Estrategias avanzadas para dominar {t}", "p1": f"Desglosamos cada concepto clave de {t} paso a paso.", "p2": "Implementamos ejercicios prácticos orientados a exámenes locales.", "p3": "Fomentamos la autonomía del estudiante."} for t in long_tails]
        }

    parrafos_long_tails = ""
    for i, item in enumerate(contenido_ia.get("long_tails_desarrollo", [])):
        h3_text = item.get("h3")
        p1_text = item.get("p1", "")
        p2_text = item.get("p2", "")
        p3_text = item.get("p3", "")

        enlace_externo = ""
        if i == 0:
            enlace_externo = ' Puedes complementar tus prácticas académicas con recursos en portales educativos de referencia como <a href="https://es.khanacademy.org" target="_blank" rel="noopener" style="color: #0b2545; text-decoration: underline;">Khan Academy</a>.'

        parrafos_long_tails += f"""
        <h3 style="color: #0b2545; margin-top: 2.5rem; font-size: 1.4rem; font-weight: 800; letter-spacing: -0.5px;">{h3_text}</h3>
        <p style="font-size: 1.05rem; margin-bottom: 1rem; color: #333; line-height: 1.8;">{p1_text}{enlace_externo}</p>
        <p style="font-size: 1.05rem; margin-bottom: 1rem; color: #333; line-height: 1.8;">{p2_text}</p>
        <p style="font-size: 1.05rem; margin-bottom: 1.5rem; color: #444; line-height: 1.8;">{p3_text}</p>
        """

    html_contenido = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="description" content="{extracto_card}">
    <link rel="canonical" href="{url_articulo}">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.8; color: #222; background-color: #fdfdfd; margin: 0; padding: 0;">
    <div style="max-width: 1000px; width: 90%; margin: 40px auto; background: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
        <header style="border-bottom: 2px solid #eaeaea; padding-bottom: 1.5rem; margin-bottom: 2rem;">
            <span style="color: #0b2545; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px;">Excelencia Académica en Santo Domingo</span>
            <h1 style="color: #0b2545; font-size: 2.4rem; margin-top: 0.5rem; line-height: 1.15; font-weight: 900; letter-spacing: -1px;">{titulo}</h1>
        </header>
        <main>
            <div style="margin-bottom: 2.5rem;">
                <img src="{imagen_url}" alt="{titulo}" style="width: 100%; height: 420px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.08);">
            </div>
            <p style="font-size: 1.15rem; font-weight: 700; color: #111; line-height: 1.7; margin-bottom: 1.5rem;">{contenido_ia.get("intro")}</p>
            
            <h2 style="color: #0b2545; margin-top: 3rem; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px;">¿Por qué los métodos tradicionales ya no dan resultados?</h2>
            <p style="font-size: 1.05rem; color: #333; line-height: 1.8; margin-bottom: 1rem;">{contenido_ia.get("por_que")}</p>
            
            {parrafos_long_tails}

            <h2 style="color: #0b2545; margin-top: 3rem; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px;">La ruta crítica para asegurar tu aprobación definitiva</h2>
            <p style="font-size: 1.05rem; color: #333; line-height: 1.8;">No pierdas más tiempo intentando descifrar libros complejos por tu cuenta. Conoce nuestros <a href="../index.html#planes" style="color: #0b2545; font-weight: bold; text-decoration: underline;">planes y tarifas de tutorías especializadas</a> diseñados para garantizar un progreso real en tus notas.</p>
            
            {enlace_interno_html}

            <div style="background: #f8fafc; padding: 2.5rem; border-left: 6px solid #0b2545; margin: 3rem 0; border-radius: 8px; box-shadow: 0 6px 15px rgba(0,0,0,0.04); text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <p style="margin: 0; font-weight: 900; font-size: 1.3rem; color: #0b2545; max-width: 600px;">¿Vas a dejar que un mal promedio arruine tu futuro profesional?</p>
                <p style="margin: 0.8rem 0 1.5rem 0; font-size: 1.1rem; color: #444; max-width: 600px;">Toma el control de tus calificaciones hoy mismo. Escríbenos directamente por WhatsApp y asegura un profesor particular enfocado en resultados rápidos en Santo Domingo.</p>
                <a href="https://wa.me/{NUMERO_WHATSAPP}?text=Hola,%20necesito%20información%20sobre%20clases%20de%20matemáticas%20para%20asegurar%20mis%20calificaciones." target="_blank" style="background: #25d366; color: white; padding: 0.9rem 2rem; border-radius: 6px; text-decoration: none; font-weight: 800; display: inline-block; font-size: 1.05rem; box-shadow: 0 4px 12px rgba(37,211,102,0.3);">¡Quiero asegurar mis calificaciones ahora! →</a>
            </div>
        </main>
        <footer style="margin-top: 4rem; border-top: 1px solid #eaeaea; padding-top: 1.5rem; text-align: center; color: #777; font-size: 0.9rem;">
            <p>&copy; {datetime.now().year} Clases de Matemáticas Santo Domingo. Todos los derechos reservados.</p>
            <p><a href="../index.html" style="color: #0b2545; text-decoration: none; font-weight: bold;">← Volver a la página principal</a></p>
        </footer>
    </div>
</body>
</html>
"""

    os.makedirs("blog", exist_ok=True)
    ruta_archivo = os.path.join("blog", f"{slug}.html")
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(html_contenido)
    print(f"Artículo generado con éxito: {ruta_archivo}")

    registros_csv = []
    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 4:
                    registros_csv.append(row)
    
    if not any(r[1] == slug for r in registros_csv):
        registros_csv.append([titulo, slug, url_articulo, extracto_card])

    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Titulo", "Slug", "URL para Search Console", "Extracto"])
        writer.writerows(registros_csv)
    print("CSV actualizado correctamente.")

datos_por_slug = {}
if os.path.exists(csv_path):
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 4:
                datos_por_slug[row[1]] = {"titulo": row[0], "extracto": row[3]}

urls_sitemap = [f"""    <url>
        <loc>{DOMINIO_BASE}</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>"""]

tarjetas_html = []
salto_linea = "\n"

if os.path.exists("blog"):
    for archivo_blog in sorted(os.listdir("blog"), reverse=True):
        if archivo_blog.endswith(".html"):
            slug_archivo = archivo_blog.replace(".html", "")
            info_articulo = datos_por_slug.get(slug_archivo, {"titulo": "Artículo de Matemáticas", "extracto": "Artículo especializado en rendimiento académico."})
            
            titulo_card = info_articulo["titulo"]
            extracto_card = info_articulo["extracto"]
            url_dinamica = f"{DOMINIO_BASE}blog/{archivo_blog}"
            
            urls_sitemap.append(f"""    <url>
        <loc>{url_dinamica}</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")
            
            tarjeta = f"""
            <div style="background: white; padding: 1.8rem; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.06); display: flex; flex-direction: column; justify-content: space-between; border: 1px solid #edf2f7;">
                <div>
                    <span style="font-size: 0.8rem; color: #0b2545; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">SEO & Matemáticas</span>
                    <h3 style="font-size: 1.25rem; margin: 0.6rem 0; color: #111; font-weight: 700; line-height: 1.4;">{titulo_card}</h3>
                    <p style="font-size: 0.95rem; color: #555; margin-bottom: 1.5rem; line-height: 1.5;">{extracto_card}</p>
                </div>
                <a href="blog/{archivo_blog}" target="_blank" style="color: #0b2545; font-weight: 800; text-decoration: none; font-size: 0.95rem; display: inline-flex; align-items: center;">Leer artículo completo →</a>
            </div>
            """
            tarjetas_html.append(tarjeta)

sitemap_contenido = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{salto_linea.join(urls_sitemap)}
</urlset>
"""

with open("sitemap.xml", "w", encoding="utf-8") as sm:
    sm.write(sitemap_contenido)

if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        index_content = f.read()
    
    start_marker = "<!-- BLOG_CARDS_START -->"
    end_marker = "<!-- BLOG_CARDS_END -->"
    
    if start_marker in index_content and end_marker in index_content:
        nuevo_bloque_blog = f"{start_marker}\n" + "".join(tarjetas_html) + f"\n{end_marker}"
        partes = index_content.split(start_marker)
        segunda_parte = partes[1].split(end_marker)[1]
        index_actualizado = partes[0] + nuevo_bloque_blog + segunda_parte
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(index_actualizado)

with open("keywords.json", "w", encoding="utf-8") as f:
    json.dump(keywords_data, f, ensure_ascii=False, indent=4)

print("¡Proceso finalizado correctamente!")
