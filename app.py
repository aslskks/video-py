from pygments.lexers import Python3Lexer
import wave
import numpy as np
import sounddevice as sd
from tkinter import filedialog
import tkinter as tk
import os
import moviepy.editor as mp
from pygments.styles import get_style_by_name
from pygments.formatters import ImageFormatter
from pygments import highlight
from tkinter import messagebox


def main():
    pass


def record_audio():
    fs = 44100  # Frecuencia de muestreo
    duration = 5  # Duración de la grabación en segundos
    audio = sd.rec(int(fs * duration), samplerate=fs, channels=2)
    sd.wait()

    # Guardar la grabación en un archivo temporal
    audio_file = "temp_audio.wav"
    wf = wave.open(audio_file, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(fs)
    wf.writeframes(audio.tobytes())
    wf.close()

    return audio_file


def main(audio_file=None):
    # Definir la ruta completa al código de Python
    direccion_del_codigo = input("Dirección completa del código de Python: ")

    # Verificar si el archivo existe
    if not os.path.exists(direccion_del_codigo):
        print("El archivo especificado no existe.")
    else:
        with open(direccion_del_codigo, 'r', encoding='utf-8') as file:
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

        if audio_file:
            final_clip = final_clip.set_audio(mp.AudioFileClip(audio_file))

        final_clip.write_videofile(
            "code_animation.mp4", fps=24, codec="libx264")

        print("Video generado como 'code_animation.mp4'")


def select_audio_source():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    print("Selecciona la fuente de audio:")
    print("1. Grabar audio desde el micrófono")
    print("2. Seleccionar un archivo de audio")
    print("3. Omitir audio")
    choice = input("Escribe '1', '2', o '3' y presiona Enter: ")

    if choice == '1':
        audio_file = record_audio()
        main(audio_file)
    elif choice == '2':
        audio_file = filedialog.askopenfilename(
            title="Selecciona un archivo de audio")
        if audio_file:
            main(audio_file)
        else:
            main()
    elif choice == '3':
        main()


if __name__ == "__main__":
    import sys
    try:
        select_audio_source()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        messagebox.showerror(title="video de programacion", message=f"{e}")
