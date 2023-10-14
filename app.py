def main():
    from pygments import highlight
    from pygments.lexers import Python3Lexer
    from pygments.formatters import ImageFormatter
    from pygments.styles import get_style_by_name
    import moviepy.editor as mp
    import os

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

        # Crear las imágenes
        for idx, filename in enumerate(filenames):
            with open(filename, "wb") as image_file:
                highlighted_code = code[0:idx]
                img = highlight(highlighted_code, Python3Lexer(),
                                ImageFormatter(**formatter_options))
                image_file.write(img)

        # Generar clips y duración
        clips = [mp.ImageClip(filename).set_duration(0.05)
                 for filename in filenames]

        # Crear el video
        final_clip = mp.concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(
            "code_animation.mp4", fps=24, codec="libx264")

        print("Video generado como 'code_animation.mp4'")


if __name__ == "__main__":
    import sys
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
