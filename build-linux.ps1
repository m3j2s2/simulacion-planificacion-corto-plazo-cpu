# Script para compilar para Linux con Docker

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  COMPILADOR DOCKER - LINUX" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Docker
Write-Host "[1/4] Verificando Docker..." -ForegroundColor Yellow
try {
    docker --version | Out-Null
    Write-Host "  OK - Docker instalado" -ForegroundColor Green
} catch {
    Write-Host "  ERROR - Docker no encontrado" -ForegroundColor Red
    Write-Host "  Instala Docker Desktop y vuélvelo a intentar" -ForegroundColor Yellow
    exit 1
}

# Construir imagen
Write-Host ""
Write-Host "[2/4] Construyendo imagen Docker..." -ForegroundColor Yellow
Write-Host "  (Esto tardara 2-3 minutos la primera vez)" -ForegroundColor Gray
docker build -t simulador-linux .

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR al construir imagen" -ForegroundColor Red
    exit 1
}
Write-Host "  OK - Imagen creada" -ForegroundColor Green

# Crear carpeta para el ejecutable
Write-Host ""
Write-Host "[3/4] Creando carpeta dist-linux..." -ForegroundColor Yellow
if (!(Test-Path "dist-linux")) {
    New-Item -ItemType Directory -Path "dist-linux" | Out-Null
}
Write-Host "  OK - Carpeta lista" -ForegroundColor Green

# Extraer ejecutable
Write-Host ""
Write-Host "[4/4] Extrayendo ejecutable de Linux..." -ForegroundColor Yellow
docker run --rm -v "${PWD}/dist-linux:/output" simulador-linux sh -c "cp /app/dist/SimuladorProcesos /output/"

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR al extraer ejecutable" -ForegroundColor Red
    exit 1
}

Write-Host "  OK - Ejecutable extraido" -ForegroundColor Green

# Resumen final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  COMPILACION EXITOSA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ejecutables disponibles:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  [WINDOWS] dist/SimuladorProcesos.exe" -ForegroundColor White
Write-Host "  [LINUX]   dist-linux/SimuladorProcesos" -ForegroundColor White
Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")