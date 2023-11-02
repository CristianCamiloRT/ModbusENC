from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server.async_io import StartTcpServer
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def cargar_clave_privada(key_file):
    with open(key_file, 'rb') as f:
        key = RSA.import_key(f.read())
    return key

key_file = "private_key.pem"
private_key = cargar_clave_privada(key_file)
cipher = PKCS1_OAEP.new(private_key)

coils = ModbusSequentialDataBlock(1, [0])
discrete_inputs = ModbusSequentialDataBlock(1, [False])
holding_registers = ModbusSequentialDataBlock(1, [0])
input_registers = ModbusSequentialDataBlock(1, [0])

slave_context = ModbusSlaveContext(
    di=discrete_inputs,
    co=coils,
    hr=holding_registers,
    ir=input_registers
)

server_context = ModbusServerContext(slaves=slave_context, single=True)

print("El servidor está en funcionamiento.")
print("Estado inicial del interruptor:", coils.getValues(1, 1)[0])

import threading
threading.Thread(target=StartTcpServer, kwargs={'context': server_context, 'address': ('[::1]', 502)}).start()

last_state = coils.getValues(1, 1)[0]
while True:
    encrypted_state = coils.getValues(1, 1)[0]
    print(encrypted_state)
    # if encrypted_state:
    #     try:
    #         current_state_bytes = cipher.decrypt(encrypted_state)
    #         current_state = bool(int(current_state_bytes.decode()))
    #         if current_state != last_state:
    #             print("El estado del interruptor ha cambiado:", current_state)
    #             last_state = current_state
    #     except ValueError:
    #         print("Error al desencriptar el mensaje.")
    time.sleep(1)
