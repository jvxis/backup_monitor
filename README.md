# 📂 Backup Monitor

Este projeto monitora automaticamente alterações em vários diretórios e realiza o backup de arquivos modificados ou criados, adicionando prefixo BCK_ e timestamp para organização.
Todos os arquivos de backup são salvos em uma estrutura ordenada dentro de um único diretório de destino.

Ideal para proteger dados sensíveis como bases SQLite, arquivos de configuração e informações críticas de operação.

## ⚙️ Requisitos

Python 3.x instalado

Permissões de leitura nos diretórios monitorados

Permissões de escrita no diretório de backup

pip para instalação de pacotes

# 📦 Instalação
## 1. Crie e ative um ambiente virtual Python:

### Instale o venv caso ainda não tenha
```
sudo apt install python3-venv
```
### Navegue até a pasta onde deseja instalar o script
```
cd /home/admin/
```
### Crie o ambiente virtual
```
python3 -m venv backupenv
```
### Ative o ambiente virtual
```
source backupenv/bin/activate
```
## 2. Instale as dependências:
```
pip3 install watchdog
```
# 🛠️ Configuração

Diretórios Monitorados

Edite no script Python a lista:
```
directories_to_monitor = [
    "/home/admin/lnbits/data",
    "/home/admin/node-check",
    # Adicione mais diretórios se quiser
]
```
Todos os diretórios incluídos serão monitorados recursivamente.

Diretório de Backup

Defina o local onde os arquivos de backup serão salvos:

```
backup_folder = "/brln_backup"
Se o diretório não existir, será criado automaticamente.
```
Arquivos ignorados
O script ignora:

Arquivos temporários de SQLite (-journal)

Arquivos específicos listados em files_to_ignore:

```
files_to_ignore = [
    "logs/lnbits.log",
    "logs/debug.log"
]
```
## ▶️ Executando manualmente
Após configurar o ambiente virtual:

```
source /home/admin/backupenv/bin/activate
python3 seu_script_backup.py
```
(Altere seu_script_backup.py para o nome real do seu script.)

O terminal mostrará os eventos monitorados e os backups realizados em tempo real.

## 🖥️ Configurando como serviço systemd
Para deixar o monitoramento automático no boot do sistema:

### 1. Crie o arquivo de serviço:
```
sudo nano /etc/systemd/system/backup.service
```
### 2. Cole o conteúdo abaixo (ajuste o nome do seu script):
```
[Unit]
Description=Monitoramento e Backup automático LNbits
After=network.target

[Service]
User=admin
WorkingDirectory=/home/admin
Environment="PATH=/home/admin/backupenv/bin"
ExecStart=/home/admin/backupenv/bin/python3 /home/admin/seu_script_backup.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Importante: Trocar seu_script_backup.py pelo nome real do seu arquivo Python.

### 3. Ative e inicie o serviço:
   
Atualizar o systemd
```
sudo systemctl daemon-reload
```
Habilitar para iniciar automaticamente
```
sudo systemctl enable backup.service
```
Iniciar o serviço agora
```
sudo systemctl start backup.service
```
### Verificar o status
```
sudo systemctl status backup.service
```

# 🗂️ Estrutura dos backups

Os backups ficam organizados por subpastas, uma para cada diretório monitorado, conforme o exemplo:

```
/brln_backup/
  ├── home_admin_lnbits_data/
  │     └── wallets/
  │          └── HUB_database.sqlite3_20250417_120505
  ├── home_admin_node-check/
  │     └── HUB_keysend_rewards.db_20250417_120507
  └── backup_log.txt
```
# 📝 Observações
Todos os backups possuem o prefixo HUB_ seguido do timestamp no formato YYYYMMDD_HHMMSS.

O log completo de operações está disponível em:
/brln_backup/backup_log.txt

Para adicionar novos diretórios para monitorar, basta incluir na lista directories_to_monitor no código.

