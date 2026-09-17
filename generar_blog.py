import json
import os
import csv

# 1. Cargar la parrilla de keywords
with open("keywords.json", "r", encoding="utf-8") as f:
    keywords_data = json.load(f)

articulo_actual = keywords_data[0]

keyword_principal = articulo_actual.get("keyword_principal")
long_tails = articulo_actual.get("long_tails", [])
titulo = articulo_actual.get("titulo")

# FORZAMOS el slug exacto que deseas para que coincida con tu landing page
slug = "clases-de-supletorios-de-matematicas-en-santo-domingo"

# URL base exacta apuntando a tu blog con el slug largo
URL_BASE = "https://clasesmatematicassantodomingo.github.io/blog/"
url_articulo = f"{URL_BASE}{slug}.html"

# 2. Generar el contenido con el diseño profesional y WhatsApp correcto
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
        .top-bar a:hover {{
            text-decoration: underline;
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
        <a href="https://clasesmatematicassantodomingo.github.io/">← Volver a la página principal de Clases de Matemáticas</a>
    </div>

    <div class="main-container">
        <div class="category">SEO & SUPLETORIOS - SANTO DOMINGO</div>
        <h1>{titulo}</h1>
        
        <img src="https://images.unsplash.com/photo-1580582932707-520aed937b7b?auto=format&fit=crop&w=1200&q=80" alt="Estudiantes en clase" class="featured-image">

        <p>Se acabó el tiempo de esperar un milagro o cruzar los dedos. Se acerca inexorablemente el periodo de exámenes supletorios y, cada año, observo exactamente el mismo patrón repetitivo y desgastante en los colegios de Santo Domingo: padres de familia estresados gastando dinero en opciones equivocadas, estudiantes frustrados con el autoestima por el suelo, y semanas enteras de merecidas vacaciones tiradas a la basura por culpa de una sola materia maldita.</p>

        <h2>El verdadero problema detrás de los {keyword_principal}</h2>

        <p>Cuando un estudiante suspende una asignatura clave, el error común de los padres es buscar una "recuperación rápida" basada en memorizar fórmulas sin entender su trasfondo real. En Santo Domingo de los Tsáchilas, las academias masivas suelen repetir el mismo esquema escolar que ya fracasó durante el quimestre: grupos grandes, explicaciones abstractas y cero atención individualizada.</p>

        <p>A lo largo de nuestras tutorías especializadas, abordamos de raíz términos clave de búsqueda como <em>{", ".join(long_tails)}</em>. Sabemos por experiencia que el cerebro de un adolescente no necesita más teoría acumulada, sino un puente directo entre la lógica matemática y su aplicación práctica.</p>

        <h2>Por qué las clases tradicionales fallan estrepitosamente</h2>
        <ul>
            <li><strong>Falta de diagnóstico previo:</strong> Nadie se detiene a averiguar si el alumno arrastra vacíos fundamentales desde años anteriores (como fracciones, despeje de ecuaciones o leyes de Newton).</li>
            <li><strong>Ritmo impersonal:</strong> Si el estudiante se queda atrás en el primer minuto de la explicación, se desconecta mentalmente el resto de la clase.</li>
            <li><strong>Ausencia de motivación emocional:</strong> El miedo al fracaso bloquea el aprendizaje cognitivo, generando un rechazo crónico hacia los números y las ciencias exactas.</li>
        </ul>

        <h2>Nuestra metodología de rescate académico intensivo</h2>

        <p>Para garantizar que el estudiante supere con éxito el examen supletorio y recupere su confianza, diseñamos un plan de choque estructurado en tres fases críticas:</p>

        <p><strong>Diagnóstico quirúrgico de vacíos conceptuales:</strong> En la primera sesión evaluamos exactamente dónde se rompió el aprendizaje. No perdemos tiempo repasando lo que el alumno ya domina; atacamos de frente los puntos críticos que le impiden aprobar.</p>

        <p><strong>Razonamiento lógico frente a memorización ciega:</strong> Las matemáticas y las ciencias exactas no se memorizan; se comprenden. Transformamos problemas complejos en ejercicios visuales y lógicos que cualquier estudiante puede resolver aplicando sentido común estructurado.</p>

        <p><strong>Simulación de exámenes reales bajo presión:</strong> Entrenamos al alumno con exámenes supletorios de años anteriores aplicados en los principales colegios de Santo Domingo. De esta forma, el día de la prueba real sabrá gestionar los tiempos, controlar los nervios y asegurar cada punto en juego.</p>

        <h2>Preguntas frecuentes que todo padre de familia se hace</h2>

        <p><strong>¿Cuánto tiempo toma ver resultados tangibles?</strong> Gracias a la alta intensidad y personalización de nuestras sesiones, desde la segunda clase el estudiante comienza a resolver ejercicios complejos de manera autónoma, cambiando por completo su perspectiva frente a la materia.</p>

        <p><strong>¿Las clases son a domicilio o virtuales?</strong> Ofrecemos total flexibilidad adaptada a las necesidades de tu hogar en Santo Domingo de los Tsáchilas, combinando apoyo presencial directo y tutorías online de alto rendimiento.</p>

        <h2>No esperes al último día: El tiempo corre en contra</h2>

        <p>Dejar pasar los días bajo la falsa ilusión de que "ya estudiará por su cuenta" es el camino más rápido hacia la pérdida del año escolar. El supletorio no es una segunda oportunidad de regalo; es una prueba de fuego que requiere estrategia, acompañamiento profesional y disciplina táctica.</p>

        <p>No permitas que una mala nota le arruine el futuro académico a tu hijo ni sus vacaciones familiares. Es el momento de actuar con firmeza y poner el aprendizaje en manos de un especialista con experiencia probada en Santo Domingo.</p>

        <div class="cta-section">
            <div class="cta-title">¿Listo para asegurar el año escolar de tu hijo hoy mismo?</div>
            <a href="https://wa.me/593993117800?text=Hola%20Profe%20Andrés,%20necesito%20información%20sobre%20clases%20de%20supletorios" class="whatsapp-btn" target="_blank">Consultar por WhatsApp con el Profe Andrés →</a>
        </div>
    </div>

</body>
</html>
"""

# 3. Guardar el archivo exactamente con el slug largo
os.makedirs("blog", exist_ok=True)
filename_post = f"blog/{slug}.html"
with open(filename_post, "w", encoding="utf-8") as out:
    out.write(contenido_html)

# 4. Registrar en el CSV la URL correcta
archivo_csv = "urls_articulos.csv"
with open(archivo_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Titulo", "Slug", "URL para Search Console"])
    writer.writerow([titulo, slug, url_articulo])

print(f"¡Artículo generado correctamente en /blog/{slug}.html!")
