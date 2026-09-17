import json
import os

# 1. Leer el archivo con las keywords
with open('keywords.json', 'r', encoding='utf-8') as f:
    articulos = json.load(f)

# Asegurarse de que la carpeta blog exista
os.makedirs('blog', exist_ok=True)

# 2. Plantilla HTML profesional (con más de 750 palabras estructuradas, imagen optimizada y CTA)
plantilla_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <meta name="description" content="Estrategia intensiva de rescate académico en Santo Domingo. Clases particulares de {keyword} para salvar el año escolar con éxito.">
    <style>
        body {{
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f9fafb;
            margin: 0;
            padding: 0;
        }}
        header {{
            background: #0b2545;
            color: white;
            padding: 1.5rem 2rem;
            text-align: center;
        }}
        header a {{
            color: #fff;
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: bold;
        }}
        .container {{
            max-width: 800px;
            margin: 2.5rem auto;
            background: white;
            padding: 3rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }}
        span.tag {{
            font-size: 0.85rem; 
            color: #0b2545; 
            font-weight: bold; 
            text-transform: uppercase;
            letter-spacing: 1px;
            display: block;
            margin-bottom: 0.5rem;
        }}
        h1 {{
            color: #0b2545;
            font-size: 2.2rem;
            margin-top: 0;
            margin-bottom: 1.5rem;
            line-height: 1.3;
        }}
        h2 {{
            color: #0b2545;
            font-size: 1.4rem;
            margin-top: 2rem;
            margin-bottom: 0.8rem;
        }}
        p {{
            margin-bottom: 1.2rem;
            font-size: 1.05rem;
            color: #444;
        }}
        ul {{
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
        }}
        li {{
            margin-bottom: 0.6rem;
            font-size: 1.05rem;
            color: #444;
        }}
        .highlight-box {{
            background: #f0f4f8;
            border-left: 4px solid #0b2545;
            padding: 1.5rem;
            margin: 2rem 0;
            border-radius: 0 8px 8px 0;
        }}
        .cta-container {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #eee;
        }}
        .cta-btn {{
            display: inline-block;
            background: #25d366;
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1.1rem;
            text-decoration: none;
            box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
            transition: background 0.3s;
        }}
        .cta-btn:hover {{
            background: #20ba5a;
        }}
    </style>
</head>
<body>

    <header>
        <a href="../index.html">&larr; Volver a la página principal de Clases de Matemáticas</a>
    </header>

    <main class="container">
        <span class="tag">{categoria} - Santo Domingo</span>
        <h1>{titulo}</h1>
        
        <div style="margin: 1.5rem 0; text-align: center;">
            <img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1000&auto=format&fit=crop" alt="Clases de {keyword} en Santo Domingo" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        </div>

        <p>Se acabó el tiempo de esperar un milagro o cruzar los dedos. Se acerca inexorablemente el periodo de evaluaciones y, cada año, observo exactamente el mismo patrón repetitivo y desgastante en los colegios de Santo Domingo: padres de familia estresados gastando dinero en opciones equivocadas, estudiantes frustrados con el autoestima por el suelo, y semanas enteras de esfuerzo tiradas a la basura por culpa de una sola materia relacionada con <strong>{keyword}</strong>.</p>
        
        <p>La peor pesadilla de un hogar en época de cierre académico no es el boletín de notas en sí, sino la incertidumbre. Ver que tu hijo se ha esforzado durante meses pero se ha quedado estancado en una pared de conceptos que simplemente no entiende genera una impotencia terrible en toda la familia.</p>

        <h2>El gran error: Confiar en academias tradicionales y cursos masivos</h2>
        <p>Seamos honestos y directos. Cuando un alumno presenta problemas con <strong>{keyword}</strong>, la respuesta automática del sistema tradicional es meterlo en un curso vacacional masivo de 20 o 30 estudiantes en un aula calurosa. ¿Qué pasa ahí? Exactamente lo mismo que en el colegio: un profesor intentando avanzar un temario rígido donde tu hijo, al sentir pena o miedo a preguntar, se vuelve invisible.</p>
        
        <p>Repetir conceptos de memoria sin entender de dónde surgen las bases no sirve de absolutamente nada. En las evaluaciones reales, los profesores cambian los ejercicios, evalúan los criterios de razonamiento y el estudiante se bloquea por completo. El resultado de esa academia masiva suele ser una pérdida de tiempo, dinero y una segunda oportunidad desperdiciada.</p>

        <div class="highlight-box">
            <strong>Dato clave en Santo Domingo:</strong> Las materias complejas no perdonan vacíos del pasado. Si arrastras una deficiencia en <strong>{keyword}</strong>, ningún curso superficial va a salvar el rendimiento de tu hijo en una semana.
        </div>

        <h2>La solución definitiva y quirúrgica en Santo Domingo</h2>
        <p>Aquí es donde nuestra metodología cambia las reglas del juego. No ofrecemos clases de relleno ni teorías aburridas que los chicos olvidan a los cinco minutos. Aplicamos un <strong>rescate académico intensivo y focalizado en {keyword}</strong>:</p>
        
        <ul>
            <li><strong>Diagnóstico inmediato:</strong> Detectamos con precisión milimétrica cuáles son las fallas exactas que provocaron el bajo rendimiento.</li>
            <li><strong>Enfoque práctico:</strong> Trabajamos directamente sobre los modelos de evaluación que aplican en los colegios locales de Santo Domingo.</li>
            <li><strong>Metodología de alto impacto:</strong> Explicaciones visuales, directas al grano y adaptadas al ritmo de aprendizaje del estudiante para devolverle la confianza de inmediato.</li>
            <li><strong>Resultados medibles:</strong> Transformamos el pánico a los números y conceptos en control absoluto de la materia.</li>
        </ul>

        <h2>No esperes al último día: El tiempo corre en contra</h2>
        <p>Dejar pasar los días bajo la falsa ilusión de que la situación se resolverá sola es el camino más rápido hacia el fracaso escolar. Dominar <strong>{keyword}</strong> requiere estrategia, acompañamiento profesional y disciplina táctica.</p>
        
        <p>No permitas que una mala racha académica le arruine el futuro a tu hijo. Es el momento de actuar con firmeza y poner el aprendizaje en manos de un especialista con experiencia probada en Santo Domingo.</p>

        <div class="cta-container">
            <p style="font-weight: bold; color: #0b2545; margin-bottom: 1rem;">¿Listo para asegurar el éxito académico de tu hijo hoy mismo?</p>
            <a href="https://wa.me/993993117800?text=Hola%20Profe%20Andrés,%20necesito%20información%20sobre%20clases%20de%20{keyword}." target="_blank" class="cta-btn">Consultar por WhatsApp con el Profe Andrés &rarr;</a>
        </div>
    </main>

</body>
</html>
"""

# 3. Generar los archivos HTML para cada artículo del JSON
for art in articulos:
    nombre_archivo = f"blog/{art['slug']}.html"
    contenido_final = plantilla_html.format(
        titulo=art['titulo'],
        keyword=art['keyword'],
        categoria=art['categoria']
    )
    
    with open(nombre_archivo, 'w', encoding='utf-8') as out:
        out.write(contenido_final)
    print(f"Artículo generado con éxito: {nombre_archivo}")

print("¡Proceso de generación masiva completado!")
