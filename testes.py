import socket
import binascii

def get_mac_address(ip):
    try:
        # Criar um socket e conectar ao IP e porta 80
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 80))

        # Obter o endereço MAC do socket
        mac = s.getsockname()[4]

        # Converter o endereço MAC para uma representação hexadecimal
        mac_hex = binascii.hexlify(mac)

        # Formatar o endereço MAC
        mac_address = ':'.join(mac_hex[i:i+2].decode() for i in range(0, len(mac_hex), 2))

        return mac_address

    except Exception as e:
        print(f"Erro ao obter endereço MAC: {e}")

    finally:
        # Fechar o socket
        if s:
            s.close()

    return None

# Exemplo de uso
ip_to_check = '192.168.1.1'

mac_address = get_mac_address(ip_to_check)

if mac_address:
    print(f"Endereço MAC para o IP {ip_to_check}: {mac_address}")
else:
    print(f"Não foi possível obter o endereço MAC para o IP {ip_to_check}")
