import matplotlib.pyplot as plt

# Datos de ejemplo (proceso, [(inicio, duracion, tipo)])
procesos = {
    "P1": [(1,1,'tip'), (2,1,'tcp'), (3,10,'cpu'), (14,1,'cpu')],
    "P2": [(6,1,'tip'), (18,1,'tip'), (26,5,'cpu')],
    "P3": [(8,1,'tip'), (20,1,'tip'), (22,2,'cpu')],
    "P4": [(10,1,'tip'), (24,1,'tcp'), (34,5,'cpu')],
}

# Colores para cada tipo global
color_eventos = {
    'tip': 'cyan',
    'tcp': 'magenta',
    'tfp': 'yellow',
}

# Colores por proceso para CPU burst
color_cpu = {
    "P1": "lime",
    "P2": "lightblue",
    "P3": "orange",
    "P4": "red",
}

fig, ax = plt.subplots(figsize=(12,4))

y = 10
yticks = []
labels = []

for proceso, eventos in procesos.items():
    for inicio, dur, tipo in eventos:
        if tipo == 'cpu':
            color = color_cpu[proceso]
        else:
            color = color_eventos[tipo]
        
        ax.broken_barh([(inicio, dur)], (y, 5), facecolors=color, edgecolor="black")
    
    yticks.append(y + 2.5)
    labels.append(proceso)
    y += 10

ax.set_yticks(yticks)
ax.set_yticklabels(labels)
ax.set_xlabel("Tiempo")
ax.set_title("Diagrama de Gantt con TIP, TCP, CPU")

ax.grid(True)
plt.show()
