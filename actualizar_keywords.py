import json
import os

KEYWORDS_FILE = "keywords.json"
BLOG_DIR = "blog/"  # Carpeta donde se guardan tus archivos .html

def actualizar_keywords_json():
    if not os.path.exists(KEYWORDS_FILE):
        print(f"No se encontró el archivo {KEYWORDS_FILE}")
        return

    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        keywords_data = json.load(f)

    # Obtener los slugs de los artículos .html que actualmente existen en la carpeta blog/
    articulos_existentes = set()
    if os.path.exists(BLOG_DIR):
        for archivo in os.listdir(BLOG_DIR):
            if archivo.endswith(".html"):
                slug = archivo[:-5]  # Quitamos la extensión .html (5 caracteres)
                articulos_existentes.add(slug)

    keywords_activas = []
    keywords_recuperadas = []

    # Verificar cuáles keywords siguen teniendo su artículo vivo y cuáles fueron borradas
    for item in keywords_data:
        slug = item.get("slug")
        if slug in articulos_existentes:
            keywords_activas.append(item)
        else:
            print(f"¡Artículo eliminado detectado! Slug huérfano: {slug}. Rehabilitando keyword al final...")
            keywords_recuperadas.append(item)

    # Si se detectaron artículos borrados, movemos sus keywords al FINAL de la lista
    if keywords_recuperadas:
        keywords_activas.extend(keywords_recuperadas)
        print(f"Se han reubicado {len(keywords_recuperadas)} keyword(s) al final de la parrilla.")

    # Guardar el JSON limpio y reorganizado
    with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(keywords_activas, f, ensure_ascii=False, indent=2)
    
    print("¡Archivo keywords.json actualizado y sincronizado con éxito!")

if __name__ == "__main__":
    actualizar_keywords_json()
