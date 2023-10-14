from tqdm import tqdm
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name
from PIL import Image
import moviepy.editor as mp
import time
import os
import io

# Definir la ruta completa al código de Python
dirrecion_del_codigo = input("Dirección completa del código de Python: ")

# Verificar si el archivo existe
if not os.path.exists(dirrecion_del_codigo):
    print("El archivo especificado no existe.")
else:
    with open(dirrecion_del_codigo, 'r', encoding='utf-8') as file:
        code = file.read()

    # Opciones de formateo para Pygments
    formatter_options = {
        "style": get_style_by_name('monokai'),
        "font_size": 32
    }

    # Directorio para almacenar las imágenes
    os.makedirs("datos", exist_ok=True)
    filenames = [f"datos/{i}.png" for i in range(len(code) + 1)]
    filename_cleaned = []

    # Parámetros de velocidad, altura y zoom
    initial_duration = 0.15  # Duración inicial de cada imagen
    max_width = 1280  # Anchura máxima
    max_height = 720  # Altura máxima
    initial_height = 720  # Altura inicial
    final_height = 100  # Altura final
    zoom_factor = 0.76  # Factor de zoom (24% menos)

    # Crear una barra de progreso animada
    with tqdm(total=len(code) + 1, desc="Creating Images", ascii=True, unit="frame") as progress:
        for idx, filename in enumerate(filenames):
            if code[idx - 1].isspace():
                progress.update(1)
                continue

            # Resaltar el código
            highlighted_code = code[0:idx]
            img = highlight(highlighted_code, Python3Lexer(),
                            ImageFormatter(**formatter_options))

            # Abrir la imagen con Pillow para redimensionar y aplicar zoom
            img = Image.open(io.BytesIO(img))

            # Ajustar la altura gradualmente
            height = int(initial_height - (initial_height -
                         final_height) * idx / len(code))
            img = img.resize((int(max_width * zoom_factor), height))

            img.save(filename)
            filename_cleaned.append(filename)
            progress.update(1)
            time.sleep(0.1)  # Agregar un retraso para mostrar la animación

    # Generar clips y duración con velocidad variable
    clips = []
    for idx, filename in enumerate(filename_cleaned):
        clip = mp.ImageClip(filename).set_duration(
            initial_duration + idx * 0.01)
        clips.append(clip)

    # Cambiar la velocidad de reproducción del video a medida que avanza
    final_clip = mp.concatenate_videoclips(clips, method="compose")

    # Guardar el video
    final_clip.write_videofile("code_animation.mp4", fps=24, codec="libx264")

    print("Video generado como 'code_animation.mp4')
