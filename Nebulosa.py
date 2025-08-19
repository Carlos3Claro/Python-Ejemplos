import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.widgets import Slider, Button

# Configuración inicial
plt.style.use('dark_background')

# Se corrige plt.subplot por plt.subplots
fig, ax = plt.subplots(figsize=(12, 10))
plt.subplots_adjust(left=0.1, right=0.85, bottom=0.25)

# Parámetros de la simulación
num_stars = 3000
num_nebula_paticles = 2000
simulation_size = 15
base_speed = 0.02
erosion_factor = 0.98

# Crear datos iniciales
np.random.seed(42)

# Estrellas
stars_r = np.random.uniform(0, simulation_size, num_stars)
stars_theta = np.random.uniform(0, 2 * np.pi, num_stars)
stars_speed = np.random.uniform(0.5, 1.5, num_stars)
stars_x = stars_r * np.cos(stars_theta)
stars_y = stars_r * np.sin(stars_theta)
stars_size = np.random.uniform(1, 8, num_stars)
# Variable stars_age no inicializada
stars_age = np.zeros(num_stars)

# Partículas nebulosa
nebula_x = np.random.uniform(-simulation_size * 1.5, simulation_size * 1.5, num_nebula_paticles)
nebula_y = np.random.uniform(-simulation_size * 1.5, simulation_size * 1.5, num_nebula_paticles)
nebula_size = np.random.uniform(0.1, 3, num_nebula_paticles)
nebula_alpha = np.random.uniform(0.05, 0.3, num_nebula_paticles)

# Gradiente de color basados en distancias al centro
def distance_to_color(distance):
    norm_dist = distance / (simulation_size * 1.5)
    r = np.clip(0.8 + 0.5 * norm_dist, 0, 1)
    g = np.clip(0.5 + 0.3 * norm_dist, 0, 1)
    b = np.clip(1.0 + 0.7 * norm_dist, 0, 1)
    return (r, g, b)

# Colores iniciales
stars_distances = np.sqrt(stars_x**2 + stars_y**2)
stars_colors = np.array([distance_to_color(d) for d in stars_distances])
nebula_distances = np.sqrt(nebula_x**2 + nebula_y**2)
nebula_colors = np.array([distance_to_color(d) for d in nebula_distances])

# Crear los scatter plots
stars_scatter = ax.scatter(stars_x, stars_y,
                           c=stars_colors,
                           s=stars_size,
                           alpha=0.9,
                           edgecolors='none')

nebula_scatter = ax.scatter(nebula_x, nebula_y,
                            c=nebula_colors,
                            s=nebula_size,
                            alpha=nebula_alpha,
                            edgecolors='none')

# Configuración del gráfico
ax.set_xlim(-simulation_size * 1.5, simulation_size * 1.5)
ax.set_ylim(-simulation_size * 1.5, simulation_size * 1.5)
ax.set_title('Nebulosa con Estrellas - Simulación', pad=20)
ax.set_aspect('equal')
ax.axis('off')

# Controles
ax_speed = plt.axes([0.2, 0.15, 0.6, 0.03])
speed_slider = Slider(ax_speed, 'Velocidad', 0, 0.1, valinit=base_speed)

ax_color = plt.axes([0.2, 0.1, 0.6, 0.03])
# Se corrige el nombre de la variable speed_slider por color_slider
color_slider = Slider(ax_color, 'Gradiente Color', 0, 1, valinit=0.5)

# Botón para acelerar
ax_button = plt.axes([0.8, 0.05, 0.1, 0.04])
# Se corrige ax.button por ax_button
boost_button = Button(ax_button, 'Turbo!', color='red')

# Barra de color
cax = plt.axes([0.07, 0.2, 0.03, 0.6])
cmap = LinearSegmentedColormap.from_list('nebula_cmap', [(0.8, 0.5, 1.0), (1.0, 0.8, 0.5), (1.0, 0.3, 0.1)])
norm = plt.Normalize(0, simulation_size * 1.5)
# Se corrige cm.ScalarMappble por cm.ScalarMappable
cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax)
cb.set_label('Distancia al centro')

# Variables para el efecto turbo
# Se corrige boosr_active por boost_active
boost_active = False
boost_factor = 3.8

def boost(event):
    global boost_active
    boost_active = not boost_active
    boost_button.color = 'green' if boost_active else 'red'
    fig.canvas.draw_idle()

boost_button.on_clicked(boost)

# Función de animación
def update(frame):
    global stars_x, stars_y, nebula_x, nebula_y, stars_theta, stars_age

    # Obtener valores de los controles
    current_speed = speed_slider.val
    # Se corrige color_balance por color_slider
    color_balance = color_slider.val

    # Aplicar turbo si está activo
    effective_speed = current_speed * (boost_factor if boost_active else 1.0)
    
    # Mover estrellas (movimiento espiral)
    # Se corrige stars_thets por stars_theta
    stars_theta += effective_speed * stars_speed * (1 - stars_r / (simulation_size * 2))
    stars_x = stars_r * np.cos(stars_theta)
    stars_y = stars_r * np.sin(stars_theta)

    # Mover partículas de nebulosa (movimiento más caótico)
    nebula_x += effective_speed * np.random.normal(0, 0.5, num_nebula_paticles)
    nebula_y += effective_speed * np.random.normal(0, 0.5, num_nebula_paticles)

    # Efecto de erosión (envejecimiento)
    # Se corrige Stars_age por stars_age
    stars_age += 0.001 * effective_speed
    # Aplicar un factor de erosión
    stars_size_adjusted = stars_size * (erosion_factor**stars_age)
    stars_alpha = 0.3 + 0.7 * (1 - stars_age)

    # Actualizar colores basados en el slider
    stars_distances = np.sqrt(stars_x**2 + stars_y**2)
    nebula_distances = np.sqrt(nebula_x**2 + nebula_y**2)

    def adjusted_color(distance, color_balance):
        norm_dist = distance / (simulation_size * 1.5)
        r = np.clip(0.8 + color_balance * norm_dist, 0, 1)
        g = np.clip(0.5 + (1 - color_balance) * norm_dist * 0.5, 0, 1)
        b = np.clip(1.0 - color_balance * norm_dist * 0.7, 0, 1)
        return (r, g, b)

    # Actualizar gráficos
    # Se corrigen los arrays de color y se actualizan los datos del scatter
    stars_colors_updated = np.array([adjusted_color(d, color_balance) for d in stars_distances])
    nebula_colors_updated = np.array([adjusted_color(d, color_balance) for d in nebula_distances])

    stars_scatter.set_offsets(np.column_stack((stars_x, stars_y)))
    stars_scatter.set_color(stars_colors_updated)
    stars_scatter.set_alpha(stars_alpha)
    stars_scatter.set_sizes(stars_size_adjusted)

    nebula_scatter.set_offsets(np.column_stack((nebula_x, nebula_y)))
    nebula_scatter.set_color(nebula_colors_updated)

    # Reubicar partículas que salen del área visible
    # Se corrige np.ads por np.abs
    out_of_bounds = (np.abs(nebula_x) > simulation_size * 2) | (np.abs(nebula_y) > simulation_size * 2)
    if out_of_bounds.any():
        nebula_x[out_of_bounds] = np.random.uniform(-simulation_size, simulation_size, out_of_bounds.sum())
        nebula_y[out_of_bounds] = np.random.uniform(-simulation_size, simulation_size, out_of_bounds.sum())
    
    # Se devuelve una tupla con los artistas que se actualizan
    return stars_scatter, nebula_scatter

# Crear animación
# Se corrige el argumento frames, ya que no se usa en la función update
ani = FuncAnimation(fig, update, interval=50, blit=True)

plt.show()