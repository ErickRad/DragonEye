import socket
import threading
import psutil
import ipaddress
import requests
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp

interfacesList = []
devicesList = []
deviceInfos = []
interface = None
network_id = None
vendor = None
lock = threading.Lock()

def isConnected():
    global interfacesList, interface, network_id
    try:
        interfacesList = psutil.net_if_stats()
        for interface, status in interfacesList.items():
            if status.isup:
                for addr in psutil.net_if_addrs().get(interface, []):
                    if addr.family == socket.AF_INET:
                        network_id = str(ipaddress.IPv4Network(f"{addr.address}/{addr.netmask}", strict=False))

                socket.create_connection(("www.google.com", 80), 5)
                return True, interface, network_id

    except (socket.error, ConnectionError):
        return False

def scanDevices():
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network_id)
    result = srp(packet, timeout=4, verbose=0)[0]

    for sent, received in result:
        mac_formatted = "".join(received.hwsrc.upper().split(':')[:3])

        with open('util/macList.txt', 'r', encoding='utf-8') as file:

            for line in file:
                parts = line.strip().split()
                if len(parts) >= 2:
                    oui = parts[0].strip()
                    vendor = ' '.join(parts[1:]).strip()
                    if mac_formatted == oui:
                        vendor = ' '.join(parts[1:]).strip()
                        break

        deviceInfos = [received.psrc, str(received.hwsrc).upper(), vendor]
        devicesList.append(deviceInfos)

    return devicesList
