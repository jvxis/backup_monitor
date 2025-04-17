import os
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# ==========================
# Configurações do Usuário
# ==========================

# Lista de diretórios que serão monitorados (adicione quantos quiser)
directories_to_monitor = [
    "/home/admin/lnbits/data",
    "/home/admin/node-check"
]

# Pasta onde todos os backups serão salvos
backup_folder = "/brln_backup"

# Arquivos para ignorar no backup (relativos ao diretório monitorado)
files_to_ignore = [
    "logs/lnbits.log",
    "logs/debug.log"
]

# ==========================
# Preparação
# ==========================

# Cria o diretório de backup se não existir
os.makedirs(backup_folder, exist_ok=True)

# Configura o arquivo de log
log_file = os.path.join(backup_folder, "backup_log.txt")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

# ==========================
# Classe de Monitoramento
# ==========================

class DirectoryBackupHandler(FileSystemEventHandler):
    def handle_event(self, event):
        if event.is_directory:
            return

        src_path = event.src_path

        # Ignorar arquivos temporários de journal do SQLite
        if src_path.endswith("-journal"):
            logging.info(f"Ignorado arquivo temporário: {src_path}")
            return

        # Identificar de qual diretório monitorado o evento veio
        matching_base = None
        for base_dir in directories_to_monitor:
            if src_path.startswith(base_dir):
                matching_base = base_dir
                break

        if not matching_base:
            logging.info(f"Ignorado arquivo fora dos diretórios monitorados: {src_path}")
            return

        # Caminho relativo ao diretório base
        rel_path = os.path.relpath(src_path, matching_base)

        # Ignorar arquivos específicos
        if rel_path in files_to_ignore:
            logging.info(f"Ignorado arquivo configurado para ignorar: {rel_path}")
            return

        # Montar o caminho do backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.basename(rel_path)
        dirname = os.path.dirname(rel_path)

        # Backup organizado por subpasta conforme o diretório monitorado
        backup_subfolder = matching_base.strip("/").replace("/", "_")  # Ex: home_admin_lnbits_data
        backup_path = os.path.join(backup_folder, backup_subfolder, dirname, f"BCK_{filename}_{timestamp}")

        # Cria subdiretórios necessários
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        try:
            shutil.copy2(src_path, backup_path)
            logging.info(f"Backup realizado: {rel_path} => {backup_path}")
        except FileNotFoundError as e:
            logging.error(f"Erro ao copiar {src_path}: {e}")

    def on_modified(self, event):
        self.handle_event(event)

    def on_created(self, event):
        self.handle_event(event)

# ==========================
# Função Principal
# ==========================

def monitor_directories():
    event_handler = DirectoryBackupHandler()
    observer = Observer()

    # Agendar monitoramento para todos os diretórios da lista
    for directory in directories_to_monitor:
        observer.schedule(event_handler, directory, recursive=True)

    observer.start()

    try:
        logging.info(f"Iniciado monitoramento para: {', '.join(directories_to_monitor)}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# ==========================
# Execução
# ==========================

if __name__ == "__main__":
    monitor_directories()
