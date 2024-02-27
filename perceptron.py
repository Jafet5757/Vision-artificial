import os
import numpy as np
import matplotlib.pyplot as plt

FOLDER_PATH = './images-numbers/2'
ANOTHER_FOLDER_PATH = './images-numbers/5'

# Leemos todos los archivos de la carpeta images-numbers/2 y los listamos
def list_images(path=FOLDER_PATH):
  images = []
  for filename in os.listdir(path):
      if filename.endswith('.png'):
          images.append(filename)
  return images

def sum_image(image, path=FOLDER_PATH):
  # Leemos la imagen
  img = plt.imread(path + '/' + image)
  # Sumamos todos los valores de la imagen
  return np.sum(img)

def graph_sample():
  # Listamos las imágenes
  images = list_images()
  # Sumamos los valores de las imágenes
  sums = [sum_image(image) for image in images]
  # Obtenemos el promedio de los valores
  mean = np.mean(sums)
  # Graficamos el promedio
  plt.axhline(y=mean, color='r', linestyle='-')
  # Graficamos los valores
  plt.plot(sums)
  plt.show()

def perceptron(vectors):
  # sumamos el vector
  suma = [np.sum(vector) for vector in vectors]
  umbral = np.mean(suma)
  return umbral

def predict(image, h, path=FOLDER_PATH):
  # Leemos la imagen
  img = plt.imread(path + '/' + image)
  # Sumamos los valores de la imagen en cada fila
  suma = [np.sum(row) for row in img]
  # Comparamos el umbral con el valor de la suma
  result = np.array(suma) > h
  # Contamos cuantos valores son mayores al umbral
  count = np.sum(result)
  # Si más de la mitad de los valores son mayores al umbral
  # entonces la imagen es un 2
  return count > len(result) / 2

def main(weight = 288):
  # Listamos las imágenes
  images = list_images()
  images2 = list_images(ANOTHER_FOLDER_PATH)
  # Genermos un vector h con los umbrales para cada fila de las imágenes
  h = np.zeros(weight)
  
  for i in range(weight):
    # Obtenemos la primer fila de las imagenes
    vectors = [plt.imread(FOLDER_PATH + '/' + image)[i] for image in images]
    # calculamos el umbral para cada fila de las imagenes
    umbral = perceptron(vectors)
    h[i] = umbral
  print(h)

  # generamos una imagen aleatoria
  random_image = np.random.choice(images)
  random_image2 = np.random.choice(images2)
  # predecimos si la imagen es un 2 o no
  result = predict(random_image, h)
  result2 = predict(random_image2, h, ANOTHER_FOLDER_PATH)
  print(result)
  print(result2)


main()