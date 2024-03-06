import subprocess
import ipaddress
import platform
import threading

devicesList = []

def scanDevices():
    global devicesList

    def scan_with_timeout(ip):
        global devicesList
        system_platform = platform.system().lower()
        command = ["ping", "-n", "1", ip] if system_platform == "windows" else ["ping", "-c", "1", ip]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            output = result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            output = result.stdout.decode('latin-1')

        if ("TTL=" in output and system_platform == "windows") or ('ttl=' in output and system_platform != "windows"):
            print(f"IP ocupado: {ip}")
            devicesList.append(ip)

    threads = [threading.Thread(target=scan_with_timeout, args=[str(ip)]) for ip in ipaddress.IPv4Network(network_id)]
    timer_thread = threading.Timer(20, lambda: [t.join() for t in threads])

    for thread in threads: thread.start()
    timer_thread.start()

    for thread in threads: thread.join()
    timer_thread.cancel()

    print(f"Dispositivos encontrados na rede: {devicesList}")

# Exemplo de uso
network_id = '192.168.1.0/24'
scanDevices(network_id)
