import socket
import subprocess
import threading
import psutil
import ipaddress
import platform

interfacesList = []
devicesList = []
interface = None
network_id = None
lock = threading.Lock()

def isConnected():
    global interfacesList, interface, network_id
    try:
        interfacesList = psutil.net_if_stats()
        for interface, status in interfacesList.items():
            if status.isup:
                for addr in psutil.net_if_addrs().get(interface, []):
                    if addr.family == socket.AF_INET:
                        network_id = ipaddress.IPv4Network(f"{addr.address}/{addr.netmask}", strict=False)
                        ipList = ipaddress.IPv4Network(network_id)

                socket.create_connection(("www.google.com", 80), 5)
                print(f"Connected by {interface} with Network ID {network_id}")
                return True

    except (socket.error, ConnectionError):
        print("Can't find any active network interface.")
        return False

def scanDevices():
    global devicesList

    def ping(ip):
        global devicesList
        system_platform = platform.system().lower()
        command = ["ping", "-n", "1", ip] if system_platform == "windows" else ["ping", "-c", "1", ip]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            output = result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            output = result.stdout.decode('latin-1')

        if ("TTL=" in output and system_platform == "windows") or ('ttl=' in output and system_platform != "windows"):
            print(f"Device: {ip}")
            devicesList.append(ip)

    threads = [threading.Thread(target=ping, args=[str(ip)]) for ip in ipaddress.IPv4Network(network_id)]
    timer_thread = threading.Timer(60, lambda: [t.join() for t in threads])

    for thread in threads: thread.start()
    timer_thread.start()

    for thread in threads: thread.join()
    timer_thread.cancel()

    print(f"Founded devices in Network: {devicesList}")

isConnected()
scanDevices()