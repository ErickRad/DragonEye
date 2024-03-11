import socket
import psutil
import ipaddress
import time
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1

interfacesList = []
devicesList = []
deviceInfos = []
responses = []

interface = None
network_id = None
vendor = None

count = 50
delay = 0.01
packet_len = " " * 32

icmp_packet = IP(dst="www.google.com") / ICMP() / packet_len

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
    isConnected()
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

def checkInternetSpeed():
    start = time.time()
    for _ in range(count):
        sent = time.time()
        response = sr1(icmp_packet, timeout=1, verbose=0)
        received = time.time()

        if response:
            response_time = (received - sent) * 1_000
            print(f"\rPing: {response_time:.2f} ms", end="")
            responses.append(response_time)
            time.sleep(delay)

    total_time = time.time() - start
    avg_ping = sum(responses[-20:]) / len(responses[-20:])
    speed = ((packet_len.__len__() * len(responses)) / total_time) / 100

    return [avg_ping, speed]