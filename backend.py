import socket
import psutil
import ipaddress
import speedtest
import flask
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp

interfacesList = []
devicesList = []
deviceInfos = []
interface = None
network_id = None
vendor = None

app = flask.Flask(__name__)
st = speedtest.Speedtest()

@app.route('/isConnected', methods=['GET'])
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
                return flask.jsonify({
                    'is_connected': True,
                    'interface': interface,
                    'network_id': network_id
                })

    except (socket.error, ConnectionError):
        return flask.jsonify({
            'is_connected': False
        })

@app.route('/scanDevices', methods=['GET'])
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

    return flask.jsonify({
        'devicesList': devicesList
    })

@app.route('/checkInternetSpeed', methods=['GET'])
def checkInternetSpeed():
    st = speedtest.Speedtest()
    download = st.download() / 1_000_000
    upload = st.upload() / 1_000_000

    return flask.jsonify({
        'download': download,
        'upload': upload
    })

app.run(debug=True)