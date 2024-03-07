import subprocess
import os
import ctypes
import sys

npcap_installer = r'util\npcap.exe'

def install_requirements():
    os.system(f"pip install -r requirements.txt")

def install_npcap():
    if os.path.exists(npcap_installer):
        if ctypes.windll.shell32.IsUserAnAdmin():
            try:
                subprocess.run(
                    npcap_installer,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except subprocess.CalledProcessError as e:
                print(f"Erro durante a instalação do Npcap: {e}")
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        print("O instalador do Npcap não foi encontrado.")

install_requirements()