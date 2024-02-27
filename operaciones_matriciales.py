import matplotlib.pyplot as plt
import numpy as np

def fill_color():
    # Creamos una matriz de 10x10x3 con el color aleatorio
    color = np.random.rand(3)
    matrix = np.full((100, 100, 3), color, dtype=np.float32)
    return matrix

# Función para escribir una imagen en formato BMP
def write_bmp(matrix, output_file):
    """ 
      width & 255: El operador & realiza una operación bit a bit de "AND" entre el valor de width y el número binario 11111111 (que es 255 en decimal). Esto extrae los primeros 8 bits (un byte) del valor de width. En otras palabras, obtiene el valor de width módulo 256, que es el residuo después de dividir width por 256. Este valor se coloca como el primer byte (el byte menos significativo) en la representación binaria del ancho de la imagen.

      54 bytes: Este es el tamaño del encabezado del archivo BMP, que incluye información como el tipo de archivo, el tamaño del archivo, el tamaño del encabezado de la imagen, el ancho y alto de la imagen, entre otros.

      3 * width * height bytes: Este es el tamaño de los datos de píxeles en bytes. En un archivo BMP sin compresión y con 24 bits por píxel (8 bits para cada uno de los canales de color rojo, verde y azul), cada píxel ocupa 3 bytes. 
    """
    height, width, _ = matrix.shape

    # Tamaño del archivo BMP
    file_size = 54 + 3 * width * height

    # Encabezado del archivo BMP
    header = bytearray([
        66, 77,             # Tipo de archivo BMP
        file_size & 255, (file_size >> 8) & 255, (file_size >> 16) & 255, (file_size >> 24) & 255,  # Tamaño del archivo
        0, 0, 0, 0,         # Reservado
        54, 0, 0, 0,        # Tamaño del encabezado de la imagen
        40, 0, 0, 0,        # Tamaño del encabezado de información
        width & 255, (width >> 8) & 255, 0, 0,  # Ancho de la imagen
        height & 255, (height >> 8) & 255, 0, 0,  # Altura de la imagen
        1, 0,               # Planos de color
        24, 0,              # Bits por píxel
        0, 0, 0, 0,         # Compresión (sin comprimir)
        0, 0, 0, 0,         # Tamaño de la imagen en bytes (0 para imágenes sin comprimir)
        0, 0, 0, 0,         # Resolución horizontal (píxeles por metro)
        0, 0, 0, 0,         # Resolución vertical (píxeles por metro)
        0, 0, 0, 0,         # Número de colores en la paleta
        0, 0, 0, 0          # Número de colores importantes
    ])

    # Datos de píxeles
    pixels = bytearray()
    for i in range(height - 1, -1, -1):
        for j in range(width):
            # Normalizar y convertir a entero antes de multiplicar por 255
            pixel = (matrix[i, j, 2], matrix[i, j, 1], matrix[i, j, 0])
            pixels += bytes([int(255 * c) for c in pixel])

    # Escribir al archivo BMP
    with open(output_file, 'wb') as f:
        f.write(header + pixels)


# generamos una matriz de 10x10 con valores aleatorios entre 0 y 255
matrix1 = fill_color()
matrix2 = fill_color()

# sumamos las matrices
matrix3 = matrix1 + matrix2

# restamos las matrices
matrix4 = matrix1 - matrix2

# multiplicamos las matrices
matrix5 = matrix1 * matrix2

# dividimos las matrices
matrix6 = matrix1 / matrix2

# mostramos las matrices
plt.subplot(231)
plt.imshow(matrix1)
plt.title('Matrix 1')

plt.subplot(232)
plt.imshow(matrix2)
plt.title('Matrix 2')

plt.subplot(233)
plt.imshow(matrix3)
plt.title('Suma')

plt.subplot(234)
plt.imshow(matrix4)
plt.title('Resta')

plt.subplot(235)
plt.imshow(matrix5)
plt.title('Multiplicación')

plt.subplot(236)
plt.imshow(matrix6)
plt.title('División')

plt.show()

# Escribimos las matrices en archivos como imágenes bmp
write_bmp(matrix1, 'matrix1.bmp')
write_bmp(matrix2, 'matrix2.bmp')