# Licensed with MIT
import os
import shutil
import glob
import argparse

parser = argparse.ArgumentParser(
    usage="docusort --path <path> [OPTIONS]"
)

parser.add_argument('--path', '-p', required=True, help='Ruta del directorio a organizar.')
parser.add_argument('--filter', '-f', required=False, help='Filtrar solo por tipo de archivo específico (ej. .txt)')
parser.add_argument('--recursive', '-r', action='store_true', help='Buscar archivos en subdirectorios de forma recursiva.')
parser.add_argument('--ignore', '-i', nargs='*', help='Lista de extensiones a ignorar (ej. .tmp .log)')
parser.add_argument('--log', help='Archivo para registrar las acciones realizadas por el script.')
parser.add_argument('--backup', help='Ruta del directorio para crear copias de seguridad de los archivos.')
parser.add_argument('--folder-prefix', help='Prefijo para las carpetas creadas (ej. "Archivos de").')
parser.add_argument('--min-size', type=int, help='Tamaño mínimo de los archivos a mover (en bytes).')
parser.add_argument('--copy', action='store_true', help='Copiar los archivos en lugar de moverlos.')
parser.add_argument('--dry-run', action='store_true', help='Mostrar qué archivos se moverían sin realizar la acción.')

file_extensions = {
    '.txt': 'Archivo de texto simple',
    '.doc': 'Documento de Microsoft Word',
    '.docx': 'Documento de Microsoft Word (nuevo formato)',
    '.xls': 'Hoja de cálculo de Microsoft Excel',
    '.xlsx': 'Hoja de cálculo de Microsoft Excel (nuevo formato)',
    '.ppt': 'Presentación de Microsoft PowerPoint',
    '.pptx': 'Presentación de Microsoft PowerPoint (nuevo formato)',
    '.pdf': 'Documento Portable Document Format',
    '.jpg': 'Imagen en formato JPEG',
    '.jpeg': 'Imagen en formato JPEG',
    '.png': 'Imagen en formato Portable Network Graphics',
    '.gif': 'Imagen en formato Graphics Interchange Format',
    '.bmp': 'Imagen en formato Bitmap',
    '.tiff': 'Imagen en formato Tagged Image File Format',
    '.tif': 'Imagen en formato Tagged Image File Format',
    '.csv': 'Archivo de valores separados por comas',
    '.xml': 'Archivo de lenguaje de marcado extensible',
    '.html': 'Archivo de documento HTML',
    '.htm': 'Archivo de documento HTML',
    '.css': 'Archivo de hojas de estilo en cascada',
    '.js': 'Archivo de JavaScript',
    '.py': 'Archivo de script de Python',
    '.java': 'Archivo de código fuente de Java',
    '.c': 'Archivo de código fuente en C',
    '.cpp': 'Archivo de código fuente en C++',
    '.exe': 'Archivo ejecutable de Windows',
    '.zip': 'Archivo comprimido en formato ZIP',
    '.rar': 'Archivo comprimido en formato RAR',
    '.7z': 'Archivo comprimido en formato 7-Zip',
    '.iso': 'Archivo de imagen de disco óptico',
    '.mp3': 'Archivo de audio en formato MPEG Audio Layer III',
    '.wav': 'Archivo de audio en formato Waveform Audio File Format',
    '.mp4': 'Archivo de vídeo en formato MPEG-4',
    '.avi': 'Archivo de vídeo en formato Audio Video Interleave',
    '.mkv': 'Archivo de vídeo en formato Matroska',
    '.apk': 'Archivo de paquete de aplicación de Android',
    '.svg': 'Gráficos vectoriales escalables',
    '.psd': 'Archivo de Adobe Photoshop',
    '.ai': 'Archivo de Adobe Illustrator',
    '.md': 'Archivo de MarkDown',
    '.json': 'Archivo de JSON'
}

def make_dirs(directory, existing_extensions, prefix='Archivos'):
    for ext in existing_extensions:
        folder_name = os.path.join(directory, f"{prefix} {ext}")
        try:
            os.makedirs(folder_name, exist_ok=True)
            print(f'Carpeta "{folder_name}" creada con éxito.')
        except Exception as e:
            print(f'Error al crear la carpeta "{folder_name}": {e}')

def get_file_size(file_path):
    return os.path.getsize(file_path)

def sort_files(directory='.', filter_ext=None, recursive=False, ignore_ext=None, log_file=None, backup_dir=None, folder_prefix='Archivos', min_size=None, copy=False, dry_run=False):
    existing_extensions = set()
    log_entries = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_ext = os.path.splitext(filename)[1]
            if filter_ext and file_ext != filter_ext:
                continue
            if ignore_ext and file_ext in ignore_ext:
                continue

            file_path = os.path.join(root, filename)
            if min_size and get_file_size(file_path) < min_size:
                continue
            
            existing_extensions.add(file_ext)

            destination_folder = os.path.join(directory, f"{folder_prefix} {file_ext}")
            os.makedirs(destination_folder, exist_ok=True)

            destination = os.path.join(destination_folder, filename)

            if dry_run:
                print(f'Se movería: "{filename}" a "{destination}".')
            else:
                try:
                    if copy:
                        shutil.copy(file_path, destination)
                        action = "Copiado"
                    else:
                        shutil.move(file_path, destination)
                        action = "Movido"

                    log_entries.append(f'{action}: "{filename}" a "{destination}".')
                    print(f'{action}: "{filename}" a "{destination}".')
                except Exception as e:
                    log_entries.append(f'Error al mover "{filename}": {e}')
                    print(f'Error al mover "{filename}": {e}')

        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not dir_name.startswith(folder_prefix):
                other_folder = os.path.join(directory, "Otros")
                os.makedirs(other_folder, exist_ok=True)
                new_dir_path = os.path.join(other_folder, dir_name)

                if dry_run:
                    print(f'Se movería la carpeta: "{dir_name}" a "{new_dir_path}".')
                else:
                    try:
                        shutil.move(dir_path, new_dir_path)
                        log_entries.append(f'Movido: carpeta "{dir_name}" a "{new_dir_path}".')
                        print(f'Movido: carpeta "{dir_name}" a "{new_dir_path}".')
                    except Exception as e:
                        log_entries.append(f'Error al mover la carpeta "{dir_name}": {e}')
                        print(f'Error al mover la carpeta "{dir_name}": {e}')

    make_dirs(directory, existing_extensions, folder_prefix)

    if log_file:
        with open(log_file, 'w') as log:
            for entry in log_entries:
                log.write(entry + '\n')

args = parser.parse_args()

path = args.path
filter_ext = args.filter
recursive = args.recursive
ignore_ext = args.ignore
log_file = args.log
backup_dir = args.backup
folder_prefix = args.folder_prefix or 'Archivos'
min_size = args.min_size
copy = args.copy
dry_run = args.dry_run

sort_files(path, filter_ext, recursive, ignore_ext, log_file, backup_dir, folder_prefix, min_size, copy, dry_run)
