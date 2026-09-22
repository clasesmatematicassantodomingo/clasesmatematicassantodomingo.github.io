import json
import os
import csv

# 1. Cargar la parrilla de keywords
# with open("keywords.json", "r", encoding="utf-8") as f:
    # keywords_data = json.load(f)
#
# Validar si quedan artículos en la parrilla
# if not keywords_data:
#    print("¡No quedan más palabras clave en la parrilla!")
#    exit()
#
# Tomar el primer artículo disponible
articulo_actual = keywords_data.pop(0) # Extrae y remueve el primer elemento
#
# keyword_principal = articulo_actual.get("keyword_principal")
# long_tails = articulo_actual.get("long_tails", [])
# titulo = articulo_actual.get("titulo")
# slug = articulo_actual.get("slug", "clases-de-supletorios-de-matematicas-en-santo-domingo")

# URL base exacta
DOMINIO_BASE = "https://clasesmatematicassantodomingo.github.io/"
# url_articulo = f"{DOMINIO_BASE}blog/{slug}.html"

# 2. Guardar el archivo actualizado de keywords (removiendo el ya usado)
# with open("keywords.json", "w", encoding="utf-8") as f:
   # json.dump(keywords_data, f, ensure_ascii=False, indent=4)

# 3. Generar el contenido HTML del artículo
contenido_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f6f9;
            color: #222;
            line-height: 1.6;
        }}
        .top-bar {{
            background-color: #0b2239;
            padding: 15px 20px;
            text-align: left;
        }}
        .top-bar a {{
            color: #ffffff;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }}
        .main-container {{
            max-width: 800px;
            margin: 40px auto;
            background: #ffffff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}
        .category {{
            font-size: 12px;
            font-weight: bold;
            color: #111;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        h1 {{
            font-size: 32px;
            color: #0b2239;
            margin-top: 0;
            line-height: 1.3;
        }}
        .featured-image {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0 30px 0;
        }}
        h2 {{
            font-size: 22px;
            color: #0b2239;
            margin-top: 35px;
            margin-bottom: 15px;
        }}
        p {{
            margin-bottom: 20px;
            font-size: 16px;
            color: #333;
        }}
        ul {{
            margin-bottom: 25px;
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 10px;
            font-size: 16px;
        }}
        .cta-section {{
            margin-top: 50px;
            text-align: center;
            padding: 30px;
            background: #f8fafc;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }}
        .cta-title {{
            font-size: 20px;
            font-weight: bold;
            color: #0b2239;
            margin-bottom: 20px;
        }}
        .whatsapp-btn {{
            display: inline-block;
            background-color: #25d366;
            color: white;
            padding: 14px 28px;
            font-size: 18px;
            font-weight: bold;
            text-decoration: none;
            border-radius: 6px;
            transition: background 0.3s ease;
        }}
        .whatsapp-btn:hover {{
            background-color: #20ba5a;
        }}
    </style>
</head>
<body>

    <div class="top-bar">
        <a href="{DOMINIO_BASE}">← Volver a la página principal de Clases de Matemáticas</a>
    </div>

    <div class="main-container">
        <div class="category">SEO & MATEMÁTICAS - SANTO DOMINGO</div>
        <h1>{titulo}</h1>
        
        <img src="https://images.unsplash.com/photo-1580582932707-520aed937b7b?auto=format&fit=crop&w=1200&q=80" alt="Estudiantes en clase" class="featured-image">

        <p>En el proceso de formación académica en Santo Domingo de los Tsáchilas, nos encontramos frecuentemente con desafíos relacionados con {keyword_principal}. Superar estas barreras requiere un enfoque estructurado, metodologías personalizadas y una guía constante para evitar retrasos en el rendimiento escolar.</p>

        <h2>Claves para dominar {keyword_principal} con éxito</h2>

        <p>A lo largo de nuestras tutorías especializadas, abordamos de raíz términos clave de búsqueda como <em>{", ".join(long_tails)}</em>. Comprendemos que cada estudiante posee un ritmo único de aprendizaje y necesita conectar la teoría matemática con aplicaciones prácticas y lógicas.</p>

        <h2>Por qué la metodología tradicional suele quedarse corta</h2>
        <ul>
            <li><strong>Falta de atención individualizada:</strong> Los grupos masivos impiden resolver las dudas específicas de cada alumno de manera oportuna.</li>
            <li><strong>Vacíos acumulados:</strong> Ignorar los cimientos teóricos de años anteriores dificulta la comprensión de nuevos temas avanzados.</li>
            <li><strong>Gestión del estrés:</strong> La presión de los exámenes genera bloqueos mentales que disminuyen drásticamente las calificaciones.</li>
        </ul>

        <h2>Nuestro enfoque de enseñanza en Santo Domingo</h2>

        <p>Diseñamos un plan de acompañamiento enfocado en potenciar las fortalezas del estudiante, transformar las debilidades en oportunidades y garantizar una sólida preparación orientada a resultados reales.</p>

        <div class="cta-section">
            <div class="cta-title">¿Listo para potenciar el rendimiento académico de tu hijo hoy mismo?</div>
            <a href="https://wa.me/593993117800?text=Hola%20Profe%20Andrés,%20necesito%20información%20sobre%20clases" class="whatsapp-btn" target="_blank">Consultar por WhatsApp con el Profe Andrés →</a>
        </div>
    </div>

</body>
</html>
"""

# 4. Guardar el archivo HTML del post
os.makedirs("blog", exist_ok=True)
filename_post = f"blog/{slug}.html"
with open(filename_post, "w", encoding="utf-8") as out:
    out.write(contenido_html)

# 5. Cargar los títulos históricos desde el CSV para mapearlos en el index
titulos_por_slug = {}
if os.path.exists("urls_articulos.csv"):
    with open("urls_articulos.csv", mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Saltar cabecera
        for row in reader:
            if len(row) >= 2:
                titulos_por_slug[row[1]] = row[0]  # {slug: titulo}

# 6. Generar o actualizar el sitemap.xml y las tarjetas para el index
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
            titulo_card = titulos_por_slug.get(slug_archivo, "Artículo de Matemáticas")
            url_dinamica = f"{DOMINIO_BASE}blog/{archivo_blog}"
            
            # Sitemap
            urls_sitemap.append(f"""    <url>
        <loc>{url_dinamica}</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")
            
            # Tarjeta visual para la página principal con su título correcto
            tarjeta = f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span style="font-size: 0.85rem; color: #0b2545; font-weight: bold;">SEO & MATEMÁTICAS</span>
                    <h3 style="font-size: 1.2rem; margin: 0.5rem 0; color: #111;">{titulo_card}</h3>
                    <p style="font-size: 0.95rem; color: #666; margin-bottom: 1.5rem;">Artículo especializado enfocado en potenciar el rendimiento académico y resolver las dudas clave de los estudiantes.</p>
                </div>
                <a href="blog/{archivo_blog}" target="_blank" style="color: #0b2545; font-weight: bold; text-decoration: none; font-size: 1rem;">Leer artículo completo →</a>
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

# 7. Actualizar index.html automáticamente si tiene los marcadores
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

print("¡Índice y sitemap actualizados correctamente con sus títulos reales!")
# 7. Registrar en el archivo CSV (modo append para conservar historial)
archivo_csv = "urls_articulos.csv"
file_exists = os.path.isfile(archivo_csv)

with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["Titulo", "Slug", "URL para Search Console"])
    writer.writerow([titulo, slug, url_articulo])

print(f"¡Artículo '{titulo}', sitemap e index.html actualizados correctamente con éxito!")
