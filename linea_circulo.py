import matplotlib.pyplot as plt
import numpy as np

matrix = np.zeros((300, 300))

# Linea Diagonal usando geometria analitica
def linea(matrix, x1, y1, x2, y2):
  m = (y2 - y1) / (x2 - x1)
  b = y1 - m * x1
  for x in range(len(matrix)):
    y = m * x + b
    matrix[int(round(x))][int(y)] = 1



# Círculo
def circ(matrix, x, y, r):
  d = 1 - r
  x = 0
  y = r
  while x <= y:
    print(x, y, d)
    matrix[x + 150][y + 150] = 1
    matrix[y + 150][x + 150] = 1
    matrix[-x + 150][y + 150] = 1
    matrix[-y + 150][x + 150] = 1
    matrix[-x + 150][-y + 150] = 1
    matrix[-y + 150][-x + 150] = 1
    matrix[x + 150][-y + 150] = 1
    matrix[y + 150][-x + 150] = 1
    if d < 0:
        d = d + 2 * x + 3
    else:
        d = d + 2 * (x - y) + 5
        y = y - 1
    x = x + 1


circ(matrix, 0, 0, 50)
linea(matrix, 0, 0, 150, 30)

plt.imshow(matrix, cmap='gray')
plt.show()