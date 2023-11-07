import logging
import asyncio
import pymodbus.client as modbusClient

logging.basicConfig(level=logging.INFO)

HOST = '127.0.0.1'
PORT = 502
CERTFILE = 'client.crt'
KEYFILE = 'client.key'

def setup_async_client():
    client = modbusClient.AsyncModbusTlsClient(host=HOST, port=PORT, certfile=CERTFILE, keyfile=KEYFILE)
    return client

async def run_async_client(client):
    logging.info('External Client Starting...')
    try:
        await client.connect()
    except Exception as e:
        logging.error(f'Error connecting to server: {e}')
        return

    while True:
        try:
            option = int(input('1. Para encender \n0. Para apagar \nDigite: '))
        except ValueError:
            print('Por favor, ingrese un número válido.')
            continue

        try:
            actual = await client.read_coils(0,1)
        except Exception as e:
            logging.error(f'Error reading coil: {e}')
            break

        if (option == 1):
            if (actual.bits[0]):
                print('\n### El interruptor ya está encendido ###\n')
            else:
                try:
                    await client.write_coil(address=0, value=True)
                except Exception as e:
                    logging.error(f'Error writing to coil: {e}')
                    break
                print('\n### Interruptor encendido ###\n')
        
        elif (option == 0):
            if (not actual.bits[0]):
                print('\n### El interruptor ya está apagado ###\n')
            else:
                try:
                    await client.write_coil(address=0, value=False)
                except Exception as e:
                    logging.error(f'Error writing to coil: {e}')
                    break
                print('\n### Interruptor apagado ###\n')

    try:
        client.close()
    except Exception as e:
        logging.error(f'Error closing connection: {e}')

async def main():
    externalclient = setup_async_client()
    await run_async_client(externalclient)

if __name__ == '__main__':
    asyncio.run(main(), debug=False)
