import os
import random
import numpy as np
import matplotlib.pyplot as plt

# Carpeta de salida
output_dir = r"<Coloque aqui su ruta>"
os.makedirs(output_dir, exist_ok=True)

# Posibles tipos de gráfico
plot_types = ["line", "bar", "scatter"]

# Paletas de colores y estilos
colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'black', 'magenta']
linestyles = ['-', '--', '-.', ':']
markers = ['o', 's', '^', '*', 'x', 'D', 'P', 'v']

# Generar N gráficos
num_plots = 100

for i in range(1, num_plots + 1):
    plt.figure(figsize=(6, 4))
    plt.style.use(random.choice(plt.style.available))  # estilo aleatorio

    plot_type = random.choice(plot_types)
    num_points = random.randint(10, 100)
    x = np.linspace(0, 10, num_points)
    y = np.cumsum(np.random.randn(num_points))  # datos acumulados (simulan una tendencia)

    color = random.choice(colors)

    if plot_type == "line":
        plt.plot(x, y, color=color, linestyle=random.choice(linestyles), linewidth=random.uniform(1, 3))
    elif plot_type == "bar":
        plt.bar(x, y, color=color, width=0.5)
    elif plot_type == "scatter":
        plt.scatter(x, y, color=color, s=random.randint(10, 100), marker=random.choice(markers))

    # Opcionales: título, etiquetas
    if random.random() < 0.7:
        plt.title(f"Gráfico #{i}")
    if random.random() < 0.5:
        plt.xlabel("Eje X")
    if random.random() < 0.5:
        plt.ylabel("Eje Y")
    if random.random() < 0.3:
        plt.grid(True)

    # Guardar imagen
    filename = os.path.join(output_dir, f"plot_{i:03}.jpeg")
    plt.tight_layout()
    plt.savefig(filename, format='jpeg', dpi=150)
    plt.close()

    print(f"Guardado: {filename}")

print(f"\nGeneración finalizada. Total: {num_plots} gráficos.")
