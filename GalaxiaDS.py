import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Configuración del tamaño de la imagen
fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
ax.set_facecolor('black')

# Parámetros de la galaxia
size = 1000
x, y = np.meshgrid(np.linspace(-5, 5, size), np.linspace(-5, 5, size))

# Crear el núcleo de la galaxia
nucleo = np.exp(-(x**2 + y**2)/0.5)

# Crear los brazos espirales
angulo = np.arctan2(y, x)
radio = np.sqrt(x**2 + y**2)

# Función para los brazos espirales
brazos = np.sin(2 * radio + 5 * angulo) * np.exp(-radio/3)

# Combinar componentes
galaxia = nucleo + brazos

# Crear un colormap personalizado con dos colores (azul y dorado)
colors = ["#1a1a2e", "#e6b422"]  # Azul oscuro y dorado
cmap = LinearSegmentedColormap.from_list("andromeda", colors)

# Mostrar la galaxia
img = ax.imshow(galaxia, cmap=cmap, extent=[-5, 5, -5, 5], origin='lower')

# Añadir estrellas aleatorias como puntos brillantes
for _ in range(500):
    x_star = np.random.uniform(-5, 5)
    y_star = np.random.uniform(-5, 5)
    size_star = np.random.uniform(0.1, 1.5)
    ax.scatter(x_star, y_star, s=size_star, color='white', alpha=np.random.uniform(0.3, 1))

# Configuración del gráfico
ax.axis('off')
plt.tight_layout()

# Mostrar el resultado
plt.show()