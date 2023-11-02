from pymodbus.client.tcp import ModbusTcpClient
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def cargar_clave_publica(cert_file):
    with open(cert_file, 'rb') as f:
        key = RSA.import_key(f.read())
    return key

cert_file = "public_key.pem"
public_key = cargar_clave_publica(cert_file)
cipher = PKCS1_OAEP.new(public_key)

client = ModbusTcpClient('[::1]', port=502)

while True:
    valor_encriptado = cipher.encrypt(b'1')
    print(valor_encriptado )
    client.write_coil(address=0, value=valor_encriptado)
    print("Interruptor encendido")
    time.sleep(10)

    valor_encriptado = cipher.encrypt(b'0')
    print(valor_encriptado )
    client.write_coil(address=0, value=valor_encriptado)
    print("Interruptor apagado")
    time.sleep(10)

client.close()
