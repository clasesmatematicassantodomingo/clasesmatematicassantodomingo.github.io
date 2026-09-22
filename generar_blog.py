import json
import os
import csv
from datetime import datetime

DOMINIO_BASE = "https://clasesmatematicassantodomingo.github.io/"

# 1. Cargar la parrilla de keywords
if not os.path.exists("keywords.json"):
    print("El archivo keywords.json no existe.")
    exit()

with open("keywords.json", "r", encoding="utf-8") as f:
    keywords_data = json.load(f)

if not keywords_data:
    print("¡No quedan más palabras clave en la parrilla!")
    exit()

# Tomar el primer artículo disponible
articulo_actual = keywords_data.pop(0)

keyword_principal = articulo_actual.get("keyword_principal")
long_tails = articulo_actual.get("long_tails", [])
titulo = articulo_actual.get("titulo")
slug = articulo_actual.get("slug", "clases-de-supletorios-de-matematicas-en-santo-domingo")

url_articulo = f"{DOMINIO_BASE}blog/{slug}.html"

# 2. Generar el contenido HTML del nuevo artículo
html_contenido = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="description" content="Artículo especializado sobre {keyword_principal} en Santo Domingo. Clases particulares y apoyo académico efectivo.">
    <link rel="canonical" href="{url_articulo}">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 2rem;">
    <header style="border-bottom: 2px solid #eaeaea; padding-bottom: 1rem; margin-bottom: 2rem;">
        <span style="color: #0b2545; font-weight: bold; font-size: 0.9rem;">BLOG DE MATEMÁTICAS</span>
        <h1 style="color: #0b2545; font-size: 2.2rem; margin-top: 0.5rem;">{titulo}</h1>
    </header>
    
    <main>
        <p style="font-size: 1.1rem;">Bienvenido a nuestro espacio de asesoría académica. Si estás buscando mejorar el rendimiento en matemáticas mediante <strong>{keyword_principal}</strong>, estás en el lugar correcto.</p>
        
        <h2 style="color: #0b2545; margin-top: 2rem;">Clave del éxito académico</h2>
        <p>Muchos estudiantes enfrentan retos constantes con la materia. Abordar temas específicos como <em>{', '.join(long_tails)}</em> de forma personalizada marca una diferencia radical en sus calificaciones.</p>
        
        <div style="background: #f4f6f9; padding: 1.5rem; border-left: 4px solid #0b2545; margin: 2rem 0; border-radius: 4px;">
            <p style="margin: 0; font-weight: bold;">¿Necesitas ayuda inmediata con las notas de tu hijo?</p>
            <p style="margin: 0.5rem 0 0 0;">Contáctanos hoy mismo para asegurar su aprobación escolar con estrategias probadas.</p>
        </div>
    </main>

    <footer style="margin-top: 4rem; border-top: 1px solid #eaeaea; padding-top: 1rem; text-align: center; color: #777; font-size: 0.9rem;">
        <p>&copy; {datetime.now().year} Clases de Matemáticas Santo Domingo. Todos los derechos reservados.</p>
        <p><a href="../index.html" style="color: #0b2545; text-decoration: none;">← Volver al inicio</a></p>
    </footer>
</body>
</html>
"""

# Asegurar que la carpeta blog exista
os.makedirs("blog", exist_ok=True)
ruta_archivo = os.path.join("blog", f"{slug}.html")

with open(ruta_archivo, "w", encoding="utf-8") as f:
    f.write(html_contenido)

print(f"Artículo generado con éxito: {ruta_archivo}")

# 3. Guardar en el archivo CSV histórico de URLs
csv_path = "urls_articulos.csv"
file_exists = os.path.exists(csv_path)

with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["Titulo", "Slug", "URL para Search Console"])
    writer.writerow([titulo, slug, url_articulo])

# 4. Cargar los títulos históricos desde el CSV para mapearlos correctamente en el index
titulos_por_slug = {}
if os.path.exists(csv_path):
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Saltar cabecera
        for row in reader:
            if len(row) >= 2:
                titulos_por_slug[row[1]] = row[0]  # Mapea {slug: titulo real}

# 5. Generar o actualizar el sitemap.xml y las tarjetas para el index
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
            # Obtiene el título real del CSV o usa un genérico si no lo encuentra
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

# 6. Actualizar index.html automáticamente usando los marcadores
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

# 7. Guardar el archivo actualizado de keywords (removiendo el ya usado para que siga su ciclo automático)
with open("keywords.json", "w", encoding="utf-8") as f:
    json.dump(keywords_data, f, ensure_ascii=False, indent=4)

print("¡Proceso completado con éxito! Índices, tarjetas y parrilla actualizados.")
