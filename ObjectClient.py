import logging
import asyncio
import pymodbus.client as modbusClient

logging.basicConfig(level=logging.INFO)

def setup_async_client():
    client = modbusClient.AsyncModbusTlsClient(host='127.0.0.1', port=502, certfile='client.crt', keyfile='client.key')
    return client

async def run_async_client(client):
    logging.info('Object Client Starting...')
    await client.connect()
    last_state = None

    while True:
        actual = await client.read_coils(0,1)
        actual_state = actual.bits[0]

        if last_state is not None and actual_state != last_state:
            print(f'\n### El estado del coil ha cambiado a: {"Encendido" if actual_state else "Apagado"} ###\n')

        last_state = actual_state

        await asyncio.sleep(1)

    client.close()

async def main():
    externalclient = setup_async_client()
    await run_async_client(externalclient)

if __name__ == '__main__':
    asyncio.run(main(), debug=False)
