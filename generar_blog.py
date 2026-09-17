import json
import os
import csv

# 1. Cargar la parrilla de keywords actualizada
with open("keywords.json", "r", encoding="utf-8") as f:
    keywords_data = json.load(f)

# Seleccionamos el primer artículo de la lista
articulo_actual = keywords_data[0]

keyword_principal = articulo_actual.get("keyword_principal")
long_tails = articulo_actual.get("long_tails", [])
titulo = articulo_actual.get("titulo")
enfoque = articulo_actual.get("enfoque")
slug = articulo_actual.get("slug")

# Definir la URL base de tu sitio web en GitHub Pages
URL_BASE = "https://clasesmatematicassantodomingo.github.io/posts/"
url_articulo = f"{URL_BASE}{slug}.html" # O ajusta la extensión si usas .md o rutas limpias

# 2. Generar el contenido completo de más de 750 palabras
contenido_markdown = f"""---
title: "{titulo}"
slug: "{slug}"
category: "SEO & SUPLETORIOS - SANTO DOMINGO"
image: "https://images.unsplash.com/photo-1580582932707-520aed937b7b?auto=format&fit=crop&w=1200&q=80"
---

# {titulo}

> **Enfoque estratégico:** {enfoque}

Se acabó el tiempo de esperar un milagro o cruzar los dedos. Se acerca inexorablemente el periodo de exámenes supletorios y, cada año, observo exactamente el mismo patrón repetitivo y desgastante en los colegios de Santo Domingo: padres de familia estresados gastando dinero en opciones equivocadas, estudiantes frustrados con el autoestima por el suelo, y semanas enteras de merecidas vacaciones tiradas a la basura por culpa de una sola materia maldita.

## 1. El verdadero problema detrás de los {keyword_principal}

Cuando un estudiante suspende una asignatura clave, el error común de los padres es buscar una "recuperación rápida" basada en memorizar fórmulas sin entender su trasfondo real. En Santo Domingo de los Tsáchilas, las academias masivas suelen repetir el mismo esquema escolar que ya fracasó durante el quimestre: grupos grandes, explicaciones abstractas y cero atención individualizada.

A lo largo de nuestras tutorías especializadas, abordamos de raíz términos clave de búsqueda como *{", ".join(long_tails)}*. Sabemos por experiencia que el cerebro de un adolescente no necesita más teoría acumulada, sino un puente directo entre la lógica matemática y su aplicación práctica.

### ¿Por qué las clases tradicionales fallan estrepitosamente?
* **Falta de diagnóstico previo:** Nadie se detiene a averiguar si el alumno arrastra vacíos fundamentales desde años anteriores (como fracciones, despeje de ecuaciones o leyes de Newton).
* **Ritmo impersonal:** Si el estudiante se queda atrás en el primer minuto de la explicación, se desconecta mentalmente el resto de la clase.
* **Ausencia de motivación emocional:** El miedo al fracaso bloquea el aprendizaje cognitivo, generando un rechazo crónico hacia los números y las ciencias exactas.

---

## 2. Nuestra metodología de rescate académico intensivo

Para garantizar que el estudiante supere con éxito el examen supletorio y recupere su confianza, diseñamos un plan de choque estructurado en tres fases críticas:

### Fase I: Diagnóstico quirúrgico de vacíos conceptuales
En la primera sesión evaluamos exactamente dónde se rompió el aprendizaje. No perdemos tiempo repasando lo que el alumno ya domina; atacamos de frente los puntos críticos que le impiden aprobar.

### Fase II: Razonamiento lógico frente a memorización ciega
Las matemáticas y las ciencias exactas no se memorizan; se comprenden. Transformamos problemas complejos en ejercicios visuales y lógicos que cualquier estudiante puede resolver aplicando sentido común estructurado.

### Fase III: Simulación de exámenes reales bajo presión
Entrenamos al alumno con exámenes supletorios de años anteriores aplicados en los principales colegios de Santo Domingo. De esta forma, el día de la prueba real sabrá gestionar los tiempos, controlar los nervios y asegurar cada punto en juego.

---

## 3. Preguntas frecuentes que todo padre de familia se hace

### ¿Cuánto tiempo toma ver resultados tangibles?
Gracias a la alta intensidad y personalización de nuestras sesiones, desde la segunda clase el estudiante comienza a resolver ejercicios complejos de manera autónoma, cambiando por completo su perspectiva frente a la materia.

### ¿Las clases son a domicilio o virtuales?
Ofrecemos total flexibilidad adaptada a las necesidades de tu hogar en Santo Domingo de los Tsáchilas, combinando apoyo presencial directo y tutorías online de alto rendimiento.

---

## Conclusión: No arriesgues el futuro académico de tu hijo

Dejar la preparación del supletorio para el último día es la forma más segura de perder el año escolar y condenar las vacaciones familiares al estrés absoluto. Tomar acción hoy significa garantizar un entorno de aprendizaje profesional, empático y enfocado estrictamente en resultados reales.

¡No esperes a que sea demasiado tarde! Contáctanos hoy mismo a través de nuestros canales oficiales y asegura el éxito definitivo en los **{keyword_principal}**.
"""

# Guardar el post en la carpeta de posts
os.makedirs("posts", exist_ok=True)
filename_post = f"posts/{slug}.md"
with open(filename_post, "w", encoding="utf-8") as out:
    out.write(contenido_markdown)

# 3. Registrar o actualizar automáticamente el archivo Excel/CSV con la URL
archivo_csv = "urls_articulos.csv"
existe_archivo = os.path.exists(archivo_csv)

# Abrir en modo 'append' (agregar) para no sobrescribir las anteriores
with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # Si el archivo es nuevo, escribimos la cabecera
    if not existe_archivo:
        writer.writerow(["Titulo", "Slug", "URL para Search Console"])
    writer.writerow([titulo, slug, url_articulo])

print(f"¡Artículo generado y URL registrada en {archivo_csv} con éxito!")
