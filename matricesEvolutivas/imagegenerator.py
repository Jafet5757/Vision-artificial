import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class generator:

  def __init__(self, matrix):
    self.matrix = np.array(matrix)
    self.probabilisticMatrix = {}
    self.cumulativeProbabilisticMatrix = []
    self.keys = []

  def generateProbabilisticMatrix(self):
    matrixFlatten = self.matrix.flatten()
    # recorremos la matriz
    for (i, po) in enumerate(matrixFlatten):
      # Obtenemos el pixel anterior
      pv = matrixFlatten[i-1] if i > 0 else None
      tag = (str(pv) + ',' if pv is not None else '') + str(po)
      # agregamos este valor de pixel a la matriz probabilistica sumando en 1
      self.probabilisticMatrix[tag] = self.probabilisticMatrix[tag] + 1 if tag in self.probabilisticMatrix else 1

  def generateCumulativeProbabilisticMatrix(self):
    # Obtenemos las llaves de la matriz probabilistica
    keys = list(self.probabilisticMatrix.keys())
    # Ordenamos las llaves
    keys.sort()
    # seleccionamos una fila (todas las que inician con el mismo caracter)
    row = (keys[1].split(','))[0]
    sum = 0
    # iteramos sobre las llaves
    for key in keys[1:]:
      # si la fila es la misma sumamos
      if key.split(',')[0] == row:
        sum += self.probabilisticMatrix[key]
      else:
        # si la fila cambia agregamos la suma a la matriz acumulativa
        self.cumulativeProbabilisticMatrix.append(sum)
        row = key.split(',')[0]
        sum = self.probabilisticMatrix[key] if key[0] == row else 0
    self.cumulativeProbabilisticMatrix.append(sum)
    self.keys = keys[1:]
    return keys[1:]
  
  def getPrediction(self, pv):
    index = -1
    # Buscamos el pixel previo en las keys
    for (i, key) in enumerate(self.keys):
      if key[0].split(',') == str(pv):
        index = i
        break
    # Obtenemos su valor acumulado
    accumulated = self.cumulativeProbabilisticMatrix[index]
    # generamos un valor aleatorio entre 0 y el valor acumulado
    r = np.random.randint(0, accumulated)
    # obtenemos el valor de index + r
    po = self.keys[index + r].split(',')[1]
    return po

# probamos el generador
""" gen = generator([[1, 2, 3], [4, 5, 5], [7, 5, 5]])
gen.generateProbabilisticMatrix()
print(gen.probabilisticMatrix)
keys = gen.generateCumulativeProbabilisticMatrix()
print(gen.cumulativeProbabilisticMatrix)
print(keys)
print(gen.getPrediction(5)) """


# Probamos leyendo una imagen
# leemos la imagen en escala de grises
image = np.array(Image.open('image.jpg').convert('L'))
# Mostramos la imagen
plt.imshow(image)
plt.show()
# Obtenemos el alto y ancho de la imagen
height, width = image.shape
# Preparamos la matriz
gen = generator(image)
gen.generateProbabilisticMatrix()
keys = gen.generateCumulativeProbabilisticMatrix()

# Generamos una nueva imagen
newImage = np.zeros((height, width))

for i in range(height):
  for j in range(width):
    # Obtenemos el pixel anterior
    pv = image[i-1][j] if i > 0 else None
    # Obtenemos el pixel actual
    po = image[i][j]
    # Obtenemos la prediccion
    newImage[i][j] = gen.getPrediction(pv)

# Mostramos la nueva imagen
plt.imshow(newImage)
plt.show()

# Guardamos la nueva imagen
newImage = Image.fromarray(newImage)
newImage.save('newImage.jpg')
