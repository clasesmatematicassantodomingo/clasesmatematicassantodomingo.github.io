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

# Selección de imagen temática única basada en el slug o categoría
if "online" in slug:
    imagen_url = "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80"
elif "domicilio" in slug or "profesor" in slug:
    imagen_url = "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=1200&q=80"
elif "supletorio" in slug:
    imagen_url = "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=80"
else:
    imagen_url = "https://images.unsplash.com/photo-1596495577886-d920f1fb7238?auto=format&fit=crop&w=1200&q=80"

# 2. Generar contenido HTML con estilo persuasivo, dinámico y enfoque de conversión (Estilo Romuald Fons)
parrafos_long_tails = ""
for tail in long_tails:
    parrafos_long_tails += f"""
    <h3 style="color: #0b2545; margin-top: 2rem; font-size: 1.3rem; font-weight: 700;">El secreto detrás de {tail}</h3>
    <p style="font-size: 1.05rem; margin-bottom: 1rem;">Seamos honestos: el sistema educativo tradicional falla porque enseña matemáticas de memoria, sin conectar con la realidad. Cuando abordamos {tail} en Santo Domingo, rompemos con esa dinámica aburrida. Aquí vamos directo a lo que importa para que el estudiante entienda los conceptos de una vez por todas.</p>
    """

html_contenido = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="description" content="Guía definitiva sobre {keyword_principal} en Santo Domingo. Domina {', '.join(long_tails) if long_tails else keyword_principal} sin rodeos y asegura tus notas.">
    <link rel="canonical" href="{url_articulo}">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.8; color: #2c3e50; max-width: 800px; margin: 0 auto; padding: 2rem;">
    <header style="border-bottom: 2px solid #eaeaea; padding-bottom: 1.5rem; margin-bottom: 2rem;">
        <span style="color: #0b2545; font-weight: bold; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Rendimiento Escolar sin Excusas</span>
        <h1 style="color: #0b2545; font-size: 2.4rem; margin-top: 0.5rem; line-height: 1.2; font-weight: 800;">{titulo}</h1>
    </header>
    
    <main>
        <div style="margin-bottom: 2rem;">
            <img src="{imagen_url}" alt="{titulo}" style="width: 100%; height: 380px; object-fit: cover; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        </div>

        <p style="font-size: 1.15rem; font-weight: 600; color: #111;">¿Harto de ver malas calificaciones y horas de frustración frente al cuaderno? Si buscas dominar <strong>{keyword_principal}</strong> en Santo Domingo, detén lo que estás haciendo y presta atención, porque la solución no está en más tutorías masivas que aburren al estudiante, sino en un método que sí funciona.</p>
        
        <h2 style="color: #0b2545; margin-top: 2.5rem; font-size: 1.5rem; font-weight: 700;">¿Por qué las clases tradicionales de matemáticas ya no sirven?</h2>
        <p style="font-size: 1.05rem;">Metodologías anticuadas obligan a los jóvenes a repetir procesos mecánicos sin entender el <em>porqué</em>. Con un enfoque especializado en {keyword_principal}, cambiamos las reglas del juego: diagnosticamos el problema de raíz y atacamos los baches académicos antes de que sea demasiado tarde.</p>
        
        {parrafos_long_tails}

        <h2 style="color: #0b2545; margin-top: 2.5rem; font-size: 1.5rem; font-weight: 700;">La estrategia exacta para aprobar con éxito</h2>
        <p style="font-size: 1.05rem;">No venimos a dar teoría de relleno. Nuestro sistema se centra en simulacros de exámenes, resolución táctica de problemas y un acompañamiento constante que transforma las matemáticas en una ventaja competitiva real.</p>

        <div style="background: #f4f6f9; padding: 2rem; border-left: 5px solid #0b2545; margin: 2.5rem 0; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.03);">
            <p style="margin: 0; font-weight: 800; font-size: 1.2rem; color: #0b2545;">¿Vas a dejar que un mal promedio arruine el año escolar?</p>
            <p style="margin: 0.8rem 0 1.5rem 0; font-size: 1.05rem;">Toma el control ahora mismo. Escríbenos y asegura un profesor particular enfocado en resultados reales en Santo Domingo.</p>
            <a href="https://wa.me/" target="_blank" style="background: #0b2545; color: white; padding: 0.8rem 1.5rem; border-radius: 6px; text-decoration: none; font-weight: bold; display: inline-block;">¡Quiero agendar una asesoría ahora! →</a>
        </div>
    </main>

    <footer style="margin-top: 4rem; border-top: 1px solid #eaeaea; padding-top: 1.5rem; text-align: center; color: #777; font-size: 0.9rem;">
        <p>&copy; {datetime.now().year} Clases de Matemáticas Santo Domingo. Todos los derechos reservados.</p>
        <p><a href="../index.html" style="color: #0b2545; text-decoration: none; font-weight: bold;">← Volver a la página principal</a></p>
    </footer>
</body>
</html>
"""
os.makedirs("blog", exist_ok=True)
ruta_archivo = os.path.join("blog", f"{slug}.html")

with open(ruta_archivo, "w", encoding="utf-8") as f:
    f.write(html_contenido)

# 3. Guardar en el CSV histórico
csv_path = "urls_articulos.csv"
file_exists = os.path.exists(csv_path)

with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["Titulo", "Slug", "URL para Search Console"])
    writer.writerow([titulo, slug, url_articulo])

# 4. Cargar títulos desde el CSV para mapear el index
titulos_por_slug = {}
if os.path.exists(csv_path):
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 2:
                titulos_por_slug[row[1]] = row[0]

# 5. Generar sitemap y tarjetas para el index
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
            
            urls_sitemap.append(f"""    <url>
        <loc>{url_dinamica}</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")
            
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

# 6. Actualizar index.html
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

# 7. Guardar keywords actualizadas
with open("keywords.json", "w", encoding="utf-8") as f:
    json.dump(keywords_data, f, ensure_ascii=False, indent=4)

print("¡Proceso completado con contenido e imágenes dinámicas y únicas!")
