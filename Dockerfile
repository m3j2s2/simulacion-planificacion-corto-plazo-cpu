# Dockerfile para compilar el simulador en Linux
FROM python:3.11-slim

# Instalar dependencias del sistema (incluyendo binutils)
RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    binutils \
    && rm -rf /var/lib/apt/lists/*

# Instalar PyInstaller y dependencias de Python
RUN pip install --no-cache-dir \
    pyinstaller \
    matplotlib \
    numpy

# Crear directorio de trabajo
WORKDIR /app

# Copiar todos los archivos del proyecto
COPY . /app

# Compilar el ejecutable
RUN pyinstaller --onefile --windowed \
    --name "SimuladorProcesos" \
    --add-data "Tandas:Tandas" \
    interfaz.py

# El ejecutable estará en /app/dist/SimuladorProcesos
CMD ["echo", "Compilación completada"]