from PIL import Image, ImageDraw
import os

# Deshabilitar el límite de píxeles de PIL
Image.MAX_IMAGE_PIXELS = None

def recortar_imagen(input_path, output_folder, recorte_width=1920, recorte_height=1080, margen=50, max_recortes=50):
    # Abre la imagen
    imagen = Image.open(input_path)
    # Obtiene las dimensiones de la imagen original
    img_width, img_height = imagen.size

    # Crear una copia de la imagen original para marcar los recortes
    imagen_con_cuadros = imagen.copy()
    draw = ImageDraw.Draw(imagen_con_cuadros)

    # Redimensionar la imagen original a 1080p (si es necesario)
    # Mantener la proporción de la imagen si es mayor que 1080p
    imagen_resized = imagen.resize((recorte_width, recorte_height), Image.Resampling.LANCZOS)
    
    # Calcular el centro de la imagen
    center_x = img_width // 2
    center_y = img_height // 2

    # Definir el tamaño inicial del paso (distancia desde el centro)
    step = recorte_width  # Los pasos aumentan con el tamaño de los recortes

    # Iniciar la espiral desde el centro
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Movimiento: derecha, abajo, izquierda, arriba
    dir_index = 0  # Dirección inicial (derecha)
    x, y = center_x, center_y  # Comenzar desde el centro

    # Asegurarse de que no salimos de los límites
    max_x = img_width - recorte_width
    max_y = img_height - recorte_height

    # Variables para los índices de recorte
    recortes = 0

    # Recorre la imagen en espiral
    while recortes < max_recortes:
        # Define las coordenadas del recorte
        left = max(0, min(x - recorte_width // 2, max_x))
        top = max(0, min(y - recorte_height // 2, max_y))
        right = left + recorte_width
        bottom = top + recorte_height

        # Recorta la imagen
        recorte = imagen.crop((left, top, right, bottom))

        # Comprobar si el recorte tiene las dimensiones exactas requeridas (1920x1080)
        if recorte.size != (recorte_width, recorte_height):
            print(f"Recorte de tamaño incorrecto (ignorado): ({recorte.size})")
            break  # Si no tiene la resolución adecuada, termina el proceso

        # Marca el área del recorte en la imagen con un cuadro
        draw.rectangle([left, top, right, bottom], outline="red", width=5)

        # Guarda el recorte
        output_path = os.path.join(output_folder, f"recorte_{recortes}.png")
        recorte.save(output_path)
        recortes += 1

        print(f"Recorte guardado en: {output_path}")

        # Moverse en espiral
        dx, dy = directions[dir_index]  # Obtener la dirección actual
        x += dx * step
        y += dy * step

        # Cambiar la dirección
        dir_index = (dir_index + 1) % 4

        # Después de dos direcciones, aumentar el paso
        if dir_index % 2 == 0:
            step += recorte_width  # Aumentar el paso después de dos movimientos

    # Guardar la imagen con los cuadros
    output_image_path = os.path.join(output_folder, "imagen_con_cuadros.png")
    imagen_con_cuadros.save(output_image_path)
    print(f"Imagen con los cuadros guardada en: {output_image_path}")

    print("Recorte completado.")

# Ruta de la imagen original
input_image_path = "29-041-Izd2-w35-proSPC-4-les1.png"

# Carpeta donde guardar los recortes y la imagen con los cuadros
output_directory = "recortes_output"

# Ejecuta la función con margen de 50 píxeles entre recortes y un máximo de 50 recortes
recortar_imagen(input_image_path, output_directory, margen=50, max_recortes=50)
