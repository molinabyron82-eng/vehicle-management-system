#!/bin/bash

echo "🚀 Iniciando Sistema de Gestión de Vehículos..."

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "⚙️ Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "⚠️ Por favor, edita el archivo .env con tus configuraciones"
fi

echo ""
echo "✅ Configuración completa!"
echo ""
echo "Para iniciar el servidor ejecuta:"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Para ejecutar los tests:"
echo "  pytest"
echo ""
echo "Documentación API disponible en:"
echo "  http://localhost:8000/docs"
echo ""
