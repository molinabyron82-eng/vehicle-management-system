#!/usr/bin/env python3
"""
Script de verificación para el proyecto antes de desplegar en Railway
"""

import sys
import os

def check_file_exists(filename, required=True):
    exists = os.path.exists(filename)
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {filename}: {'Existe' if exists else 'No existe'}")
    return exists

def check_procfile():
    """Verifica que el Procfile tenga el contenido correcto"""
    try:
        with open('Procfile', 'r') as f:
            content = f.read().strip()
        
        expected = "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT"
        
        if content == expected:
            print("✅ Procfile: Contenido correcto")
            return True
        else:
            print(f"❌ Procfile: Contenido incorrecto")
            print(f"   Actual: {content}")
            print(f"   Esperado: {expected}")
            return False
    except Exception as e:
        print(f"❌ Error leyendo Procfile: {e}")
        return False

def check_requirements():
    """Verifica que requirements.txt exista y tenga contenido"""
    try:
        with open('requirements.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if len(lines) > 0:
            print(f"✅ requirements.txt: {len(lines)} dependencias")
            
            # Verificar dependencias críticas
            critical = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic']
            for dep in critical:
                found = any(dep in line.lower() for line in lines)
                status = "✅" if found else "❌"
                print(f"   {status} {dep}")
            
            return True
        else:
            print("❌ requirements.txt: Archivo vacío")
            return False
    except Exception as e:
        print(f"❌ Error leyendo requirements.txt: {e}")
        return False

def check_app_structure():
    """Verifica la estructura de la aplicación"""
    required_files = [
        'app/__init__.py',
        'app/main.py',
        'app/core/config.py',
        'app/core/database.py',
        'app/core/security.py',
        'app/models/vehicle.py',
        'app/schemas/vehicle.py',
        'app/api/auth.py',
        'app/api/vehicles.py',
    ]
    
    print("\n📁 Estructura de la aplicación:")
    all_exist = True
    for file in required_files:
        exists = check_file_exists(file, required=True)
        if not exists:
            all_exist = False
    
    return all_exist

def check_no_conflicts():
    """Verifica que no existan archivos que causen conflictos"""
    conflict_files = ['runtime.txt', 'railway.json', 'nixpacks.toml', 'Dockerfile']
    
    print("\n⚠️  Archivos que NO deberían existir:")
    has_conflicts = False
    for file in conflict_files:
        if os.path.exists(file):
            print(f"❌ {file}: ELIMINAR ESTE ARCHIVO")
            has_conflicts = True
        else:
            print(f"✅ {file}: No existe (correcto)")
    
    return not has_conflicts

def verify_imports():
    """Intenta importar el módulo principal"""
    print("\n🔍 Verificando importaciones:")
    try:
        sys.path.insert(0, os.getcwd())
        from app.main import app
        print("✅ app.main importado correctamente")
        print(f"✅ FastAPI app encontrado: {app.title}")
        return True
    except Exception as e:
        print(f"❌ Error importando app.main: {e}")
        print("\nPosibles causas:")
        print("  - Falta instalar dependencias: pip install -r requirements.txt")
        print("  - Error de sintaxis en el código")
        print("  - Módulos faltantes")
        return False

def main():
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE PROYECTO PARA RAILWAY")
    print("=" * 60)
    
    print("\n📋 Archivos esenciales:")
    checks = []
    
    # Verificar archivos esenciales
    checks.append(check_file_exists('Procfile', required=True))
    checks.append(check_file_exists('requirements.txt', required=True))
    checks.append(check_file_exists('.env.example', required=False))
    
    print("\n🔧 Configuración:")
    checks.append(check_procfile())
    checks.append(check_requirements())
    
    # Verificar estructura
    checks.append(check_app_structure())
    
    # Verificar conflictos
    checks.append(check_no_conflicts())
    
    # Intentar importar (opcional, requiere dependencias instaladas)
    print("\n")
    import_ok = input("¿Deseas verificar importaciones? (requiere pip install) [s/N]: ")
    if import_ok.lower() == 's':
        checks.append(verify_imports())
    
    # Resultado final
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ TODAS LAS VERIFICACIONES PASARON")
        print("\n🚀 Tu proyecto está listo para desplegar en Railway!")
        print("\nPasos siguientes:")
        print("1. git add .")
        print("2. git commit -m 'Ready for Railway'")
        print("3. git push")
        print("4. En Railway, agrega PostgreSQL")
        print("5. Configura variables de entorno (SECRET_KEY, etc.)")
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("\nRevisa los errores arriba y corrígelos antes de desplegar.")
        sys.exit(1)
    print("=" * 60)

if __name__ == '__main__':
    main()
