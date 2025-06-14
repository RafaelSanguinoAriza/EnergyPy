"""Script para construir EnergyPy en diferentes plataformas."""

import os
import sys
import platform
import shutil
import subprocess
import time

def clean_build_dirs():
    """Limpia los directorios de construcción anteriores."""
    # Intentar cerrar cualquier proceso que pueda estar usando los archivos
    if platform.system() == "Windows":
        try:
            # Intentar matar cualquier proceso que pueda estar usando los archivos
            subprocess.run(["taskkill", "/F", "/IM", "EnergyPy.exe"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL)
            # Esperar un momento para que los procesos se cierren
            time.sleep(1)
        except Exception:
            pass
    
    # Intentar limpiar directorios
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✓ Directorio {dir_name} eliminado correctamente")
            except PermissionError as e:
                print(f"⚠ No se pudo eliminar {dir_name}: {e}")
                print("Continuando con la construcción sin eliminar directorios anteriores...")
    print("✓ Proceso de limpieza completado")

def create_resources():
    """Asegura que existan los recursos necesarios."""
    resources_dir = 'resources'
    if not os.path.exists(resources_dir):
        os.makedirs(resources_dir)
    
    # Crear archivos de icono vacíos si no existen
    icon_files = {
        'icon.ico': 'Windows',
        'icon.icns': 'macOS',
        'icon.png': 'Linux'
    }
    
    for icon_file, platform_name in icon_files.items():
        icon_path = os.path.join(resources_dir, icon_file)
        if not os.path.exists(icon_path):
            print(f"⚠ Advertencia: {icon_file} no encontrado para {platform_name}")

def ensure_spec_file():
    """Verifica si existe el archivo .spec y lo crea si es necesario."""
    spec_file = 'EnergyPy.spec'
    if not os.path.exists(spec_file):
        print(f"⚠ Archivo {spec_file} no encontrado. Generando uno nuevo...")
        
        system = platform.system()
        icon_option = []
        
        # Configurar opciones específicas para cada plataforma
        if system == "Windows":
            icon_path = os.path.join('resources', 'icon.ico')
            if os.path.exists(icon_path):
                icon_option = ['--icon', icon_path]
            console_option = ['--console']  # Cambiar a '--windowed' para ocultar la consola
        elif system == "Darwin":  # macOS
            icon_path = os.path.join('resources', 'icon.icns')
            if os.path.exists(icon_path):
                icon_option = ['--icon', icon_path]
            console_option = ['--windowed']
        else:  # Linux
            icon_path = os.path.join('resources', 'icon.png')
            if os.path.exists(icon_path):
                icon_option = ['--icon', icon_path]
            console_option = ['--windowed']
        
        # Generar el archivo .spec
        cmd = ['pyinstaller', '--name', 'EnergyPy', '--noconfirm', '--onedir']
        cmd.extend(console_option)
        cmd.extend(icon_option)
        cmd.extend(['--add-data', f'resources{os.pathsep}resources'])
        cmd.append('main.py')
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✓ Archivo {spec_file} generado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al generar {spec_file}: {e}")
            sys.exit(1)
    return spec_file

def build_executable():
    """Construye el ejecutable para la plataforma actual."""
    system = platform.system()
    print(f"Construyendo para {system}...")
    
    # Limpiar construcciones anteriores
    clean_build_dirs()
    
    # Verificar recursos
    create_resources()
    
    # Asegurar que existe el archivo .spec
    spec_file = ensure_spec_file()
    
    # Construir con PyInstaller
    try:
        # Ejecutar PyInstaller directamente sin intentar limpiar
        cmd = ['pyinstaller', '--noconfirm', '--distpath', './dist_new', spec_file]
        subprocess.run(cmd, check=True)
        print(f"✓ Construcción completada para {system}")
        
        # Renombrar el directorio de salida si fue exitoso
        if os.path.exists('./dist_new'):
            if os.path.exists('./dist'):
                try:
                    shutil.rmtree('./dist')
                except PermissionError:
                    # Si no se puede eliminar, usar un nombre alternativo
                    if os.path.exists('./dist_new/EnergyPy'):
                        print("⚠ No se pudo eliminar el directorio dist anterior. Usando dist_new.")
                    else:
                        print("⚠ No se encontró el ejecutable generado en dist_new.")
            else:
                try:
                    os.rename('./dist_new', './dist')
                except PermissionError:
                    print("⚠ No se pudo renombrar dist_new a dist. Usando dist_new.")
        
        # Mostrar ubicación del ejecutable
        exe_paths = [
            os.path.join("dist", "EnergyPy", "EnergyPy.exe"),  # Windows
            os.path.join("dist_new", "EnergyPy", "EnergyPy.exe"),  # Windows (alternativo)
            os.path.join("dist", "EnergyPy", "EnergyPy"),  # macOS/Linux
            os.path.join("dist_new", "EnergyPy", "EnergyPy")  # macOS/Linux (alternativo)
        ]
        
        exe_found = False
        for exe_path in exe_paths:
            if os.path.exists(exe_path):
                print(f"✓ Ejecutable creado en: {os.path.abspath(exe_path)}")
                exe_found = True
                break
        
        if not exe_found:
            print("⚠ No se pudo encontrar el ejecutable generado")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la construcción: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()