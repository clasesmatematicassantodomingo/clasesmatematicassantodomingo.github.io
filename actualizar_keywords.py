import json
import os

# Rutas de tus archivos en el repositorio de GitHub
KEYWORDS_FILE = "keywords.json"
# Asume que tus artículos generados se guardan en una carpeta llamada 'posts/' o 'content/'
POSTS_DIR = "posts/" 

def actualizar_keywords_json():
    # 1. Cargar el archivo JSON actual de keywords
    if not os.path.exists(KEYWORDS_FILE):
        print(f"No se encontró el archivo {KEYWORDS_FILE}")
        return

    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        keywords_data = json.load(f)

    # 2. Obtener la lista de artículos actualmente publicados en el repositorio
    # (Basado en los archivos markdown generados, ej: 'clases-de-algebra.md' -> slug: 'clases-de-algebra')
    articulos_existentes = set()
    if os.path.exists(POSTS_DIR):
        for archivo in os.listdir(POSTS_DIR):
            if archivo.endswith(".md"):
                slug = archivo[:-3]  # Quitamos la extensión .md
                articulos_existentes.add(slug)

    keywords_activas = []
    keywords_recuperadas = []

    # 3. Separar las keywords cuyo artículo sigue publicado frente a las que se borró el artículo
    for item in keywords_data:
        slug = item.get("slug")
        if slug in articulos_existentes:
            keywords_activas.append(item)
        else:
            # ¡Detectó que se borró la URL/artículo! Recuperamos la keyword
            print(f"Artículo eliminado detectado para el slug: {slug}. Rehabilitando keyword...")
            keywords_recuperadas.append(item)

    # 4. Si hay keywords recuperadas, las mandamos al FINAL de la lista
    if keywords_recuperadas:
        keywords_activas.extend(keywords_recuperadas)
        print(f"Se han movido {len(keywords_recuperadas)} keyword(s) al final de la lista.")

        # Opcional: Aquí tu script puede disparar la lógica para redactar y crear 
        # el nuevo artículo correspondiente a estas keywords recuperadas al final.

    # 5. Guardar el archivo JSON actualizado en el repositorio
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(keywords_activas, f, ensure_ascii=False, indent=2)
    
    print("¡Archivo keywords.json actualizado con éxito en GitHub!")

if __name__ == "__main__":
    actualizar_keywords_json()
