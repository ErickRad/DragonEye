import time
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1

respostas = []
count = 50
delay = 0.01
tamanho_pacote = " " * 32
pacote_icmp = IP(dst="8.8.8.8") / ICMP() / tamanho_pacote

print("Iniciando ping ...")

start = time.time()
for _ in range(count):
    sent = time.time()
    response = sr1(pacote_icmp, timeout=1, verbose=0)
    received = time.time()

    if response:
        response_time = (received - sent) * 1_000
        print(f"\rPing: {response_time:.2f} ms", end="")
        respostas.append(response_time)
        time.sleep(delay)

time = time.time() - sent
avg_ping = sum(responses[-20:]) / len(responses[-20:])
speed = ((packet_len.__len__() * len(responses)) / time) / 100

print(f"\nMédia de Ping: {ping_medio:.2f} ms")
print(f"Taxa de Download da Internet: {velocidade_internet:.2f} Mbps")
