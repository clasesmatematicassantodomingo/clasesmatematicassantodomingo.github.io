import json
import os

# Cargar el archivo json actualizado con la estructura sin canibalismo
with open("keywords.json", "r", encoding="utf-8") as f:
    keywords_data = json.load(f)

# Tomamos el primer elemento (o podemos adaptarlo secuencialmente)
articulo_actual = keywords_data[0]

keyword_principal = articulo_actual.get("keyword_principal")
long_tails = articulo_actual.get("long_tails", [])
titulo = articulo_actual.get("titulo")
enfoque = articulo_actual.get("enfoque")
slug = articulo_actual.get("slug")

# Generar el contenido HTML o Markdown del blog con enfoque Romuald Fons
contenido_markdown = f"""# {titulo}

> **Enfoque:** {enfoque}

Si estás buscando **{keyword_principal}** en Santo Domingo de los Tsáchilas, llegaste al lugar indicado. Sabemos que el sistema educativo tradicional falla porque enseña de manera masiva y aburrida. 

## ¿Por qué necesitas un especialista en {keyword_principal}?
A lo largo de nuestras sesiones abordamos términos clave de búsqueda como *{", ".join(long_tails)}*, garantizando un aprendizaje profundo y directo al grano, sin rodeos teóricos innecesarios.

### Beneficios directos de nuestro método:
* **Atención 100% personalizada:** Adaptada al ritmo real del estudiante.
* **Resultados rápidos:** Enfocados en aprobar exámenes, supletorios o materias difíciles.
* **Disponibilidad local y online:** En Santo Domingo y a domicilio.

¡No esperes a que sea demasiado tarde para rescatar el año escolar! Contáctanos hoy mismo y asegura el éxito académico.
"""

# Asegurarse de que exista la carpeta de posts o guardarlo directamente
os.makedirs("posts", exist_ok=True)
filename = f"posts/{slug}.md"

with open(filename, "w", encoding="utf-8") as out:
    out.write(contenido_markdown)

print(f"¡Artículo generado con éxito: {filename}!")
