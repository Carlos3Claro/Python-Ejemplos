import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm
from matplotlib.widgets import RadioButtons, Slider

# Configuración inicial
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, right=0.75, bottom=0.25)

# Parámetros de la galaxia
num_stars = 2000
galaxy_radius = 10
arm_count = 4
arm_width = 0.5
rotation_speed = 0.02
bulge_size = 3

# Crear datos de estrellas
np.random.seed(42)

# Posiciones radiales y angulares
r = np.random.uniform(0, galaxy_radius, num_stars)
theta = np.random.uniform(0, 2*np.pi, num_stars)

# Añadir estructura de brazos espirales
for i in range(num_stars):
    arm = (1 % arm_count) * (2*np.pi/arm_count)
    distance_to_arm = np.abs(theta[i] - arm) % (2*np.pi/arm_count)
    distance_to_arm = min(distance_to_arm, 2*np.pi/arm_count - distance_to_arm)
    
    if distance_to_arm < arm_width and r[i] > bulge_size:
        # Aumentar densidad en los brazos
        if np.random.random() < 0.7:
            theta[i] = arm + np.random.uniform(-arm_width, arm_width)

# Temperaturas estelares (en Kelvin)
# Más calientes cerca del centro, más frías en los brazos
temperatures = np.random.uniform(3000, 30000, num_stars)
temperatures = temperatures * (1 - 0.5 * r/galaxy_radius) + 3000 * (r/galaxy_radius)

# Convertir temperatura a color RGB
def temperature_to_rgb(temperature):
    temperature = np.clip(temperature, 1000, 40000)
    
    # Normalizar temperatura
    t = (temperature - 1000) / 39000
    
    # Rojo para temperaturas bajas
    r = np.clip(1.0 - 0.8 * (t - 0.1) if t > 0.1 else 1.0, 0, 1)
    
    # Verde
    g = np.clip(1.0 - 2.0 * abs(t - 0.5), 0, 1)
    
    # Azul para temperaturas altas
    b = np.clip(1.0 - 0.8 * (0.9 - t) if t < 0.9 else 1.0, 0, 1)
    
    return (r, g, b)

# Tamaños de las estrellas (basado en temperatura y posición)
sizes = 10 + 50 * (temperatures / 30000) * (1 - 0.5 * r/galaxy_radius)

# Convertir todas las temperaturas a colores
colors = np.array([temperature_to_rgb(t) for t in temperatures])

# Coordenadas cartesianas
x = r * np.cos(theta)
y = r * np.sin(theta)

# Dibujar las estrellas
scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.8, edgecolors='none')

# Configuración del gráfico
ax.set_xlim(-galaxy_radius*1.2, galaxy_radius*1.2)
ax.set_ylim(-galaxy_radius*1.2, galaxy_radius*1.2)
ax.set_title('Simulación de Galaxia con Filtros de Color', pad=20)
ax.set_aspect('equal')
ax.axis('off')

# Crear widgets para los filtros
rax = plt.axes([0.78, 0.5, 0.15, 0.3])
radio = RadioButtons(rax, ('Visible', 'Infrarrojo', 'Ultravioleta', 'H-Alpha'), active=0)

# Crear slider para la rotación
ax_rot = plt.axes([0.2, 0.1, 0.6, 0.03])
rot_slider = Slider(
    ax=ax_rot, label='Velocidad Rotación', 
    valmin=0, valmax=0.1, valinit=rotation_speed
)

# Función para aplicar filtros
def apply_filter(label):
    global colors
    
    if label == 'Visible':
        # Colores originales basados en temperatura
        new_colors = np.array([temperature_to_rgb(t) for t in temperatures])
    elif label == 'Infrarrojo':
        # En infrarrojo, mostramos más las estrellas frías
        new_colors = np.zeros((num_stars, 3))
        intensity = np.clip((temperatures - 2000) / 2000, 0, 1)
        new_colors[:, 0] = intensity  # Rojo para infrarrojo
    elif label == 'Ultravioleta':
        # En ultravioleta, mostramos más las estrellas calientes
        new_colors = np.zeros((num_stars, 3))
        intensity = np.clip((40000 - temperatures) / 38000, 0, 1)
        new_colors[:, 2] = intensity  # Azul para ultravioleta
    elif label == 'H-Alpha':
        # Filtro H-Alpha (emisión de hidrógeno)
        new_colors = np.zeros((num_stars, 3))
        intensity = np.clip((temperatures - 5000) / 10000, 0, 1)
        new_colors[:, 0] = intensity  # Rojo para H-Alpha
    
    colors = new_colors
    scatter.set_color(colors)
    fig.canvas.draw_idle()

radio.on_clicked(apply_filter)

# Función de animación para rotación
def update(frame):
    global theta
    
    # Actualizar velocidad de rotación desde el slider
    rotation_speed = rot_slider.val
    
    # Rotar las estrellas (más rápido cerca del centro)
    theta += rotation_speed * (galaxy_radius / (r + 1))
    
    # Actualizar posiciones
    x_new = r * np.cos(theta)
    y_new = r * np.sin(theta)
    
    # Actualizar el scatter plot
    scatter.set_offsets(np.column_stack((x_new, y_new)))
    
    return scatter,

# Crear la animación
ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)

# Barra de color para temperatura
cax = plt.axes([0.78, 0.15, 0.03, 0.3])
cmap = LinearSegmentedColormap.from_list('temp_cmap', 
                                        [(1, 0, 0), (1, 1, 0), (1, 1, 1), (0.5, 0.7, 1)])
norm = plt.Normalize(3000, 30000)
cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax)
cb.set_label('Temperatura (K)')

plt.show()