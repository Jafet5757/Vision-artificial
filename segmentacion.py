import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import cv2
from sklearn.cluster import KMeans

IMAGE = None

def load_image():
    global IMAGE
    file = filedialog.askopenfilename(
        filetypes=[("Archivos de imagen", "*.jpg; *.jpeg; *.png; *.gif; *.bmp")],
        initialdir='./img',
    )
    if file:
        print(file)
        IMAGE = file
    else:
        print('No se seleccionó ningún archivo')

def segment_color_image():
    """ 
    Segmenta una imagen por color
    """
    print('Segmentar imagen por color')
    # Leemos la imagen
    img = plt.imread(IMAGE)
    # creamos un arreglo de ceros con las mismas dimensiones de la imagen
    seg_img = np.zeros((img.shape[0], img.shape[1]))
    # creamos un arreglo de registros de colores con la forma [(R, G, B), ...]
    colors = []
    # recorremos la imagen
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # obtenemos el color del pixel
            color = img[i, j]
            # si el color no está en la lista de colores
            if color.tolist() not in colors:
                # lo agregamos
                colors.append(color.tolist())
            # obtenemos el índice del color
            color_index = colors.index(color.tolist())
            # asignamos el color al pixel
            seg_img[i, j] = color_index
    # mostramos la cantidad de clases
    print(f'Número de clases: {len(colors)}')
    # mostramos la imagen segmentada
    plt.imshow(seg_img)
    plt.show()

def method_otsu():
    """
    Método de Otsu para segmentar una imagen
    """
    print('Segmentar imagen por método de Otsu')
    # Leemos la imagen
    img = cv2.imread(IMAGE, 0)
    # Aplicamos el método de Otsu
    _, otsu_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Mostramos la imagen segmentada
    plt.imshow(otsu_img, cmap='gray')
    plt.show()

def clusters(k=3, distance=False):
  print('Segmentar imagen por método de clusters')
  # Leemos la imagen en RGB
  img = plt.imread(IMAGE)
  img = img[:, :, :3]
  print(img.shape)
  characteristic_plane = []
  # Obtenemos las variables de cada pixel para ser representado en el plano característico
  for i in range(img.shape[0]):
    for j in range(img.shape[1]):
      r, g, b = img[i, j]
      if distance:
        x1, x2, x3, x4 = distance_to_vertices(i, j, img)
        characteristic_plane.append([r, g, b, x1, x2, x3, x4])
      else:
        characteristic_plane.append([r, g, b])
  # Convertimos la lista a un arreglo de numpy
  characteristic_plane = np.array(characteristic_plane)
  # Aplicamos el algoritmo de KMeans
  kmeans = KMeans(n_clusters=k, random_state=0).fit(characteristic_plane)
  # Obtenemos las etiquetas de cada pixel
  labels = kmeans.labels_
  # Creamos una imagen segmentada
  seg_img = np.zeros((img.shape[0], img.shape[1]))
  # Asignamos la etiqueta a cada pixel
  for i in range(img.shape[0]):
    for j in range(img.shape[1]):
      seg_img[i, j] = labels[i*img.shape[1] + j]
  # Mostramos la imagen segmentada
  plt.imshow(seg_img)
  plt.show()

def distance_to_vertices(x,y,img):
  """
    Calcula la distancia de un punto a los 4 vértices de la imagen  
  """
  # Obtenemos las dimensiones de la imagen
  rows, cols = img.shape[:2]
  # Calculamos la distancia a los 4 vértices
  d1 = np.sqrt(x**2 + y**2)
  d2 = np.sqrt((x-rows)**2 + y**2)
  d3 = np.sqrt(x**2 + (y-cols)**2)
  d4 = np.sqrt((x-rows)**2 + (y-cols)**2)
  return d1, d2, d3, d4


window = tk.Tk()
window.title("Segmentación de Imágenes")

window.geometry('500x500')

image_btn = tk.Button(window, text='cargar imagen', command=load_image)
image_btn.place(x=220, y=10)

segment_btn = tk.Button(window, text='segmentar por color', command=segment_color_image)
segment_btn.place(x=50, y=60)

otsu_btn = tk.Button(window, text='segmentar por método de Otsu', command=method_otsu)
otsu_btn.place(x=300, y=60)

cluster_btn = tk.Button(window, text='segmentar por método de clusters', command=clusters)
cluster_btn.place(x=150, y=100)

window.mainloop()