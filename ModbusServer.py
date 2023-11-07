import logging
import asyncio
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server.async_io import StartAsyncTlsServer

logging.basicConfig(level=logging.INFO)

async def run_server():
    coils = ModbusSequentialDataBlock(1, [False])
    discrete_inputs = ModbusSequentialDataBlock(1, [False])
    holding_registers = ModbusSequentialDataBlock(1, [0])
    input_registers = ModbusSequentialDataBlock(1, [0])

    slave_context = ModbusSlaveContext(
        di=discrete_inputs,
        co=coils,
        hr=holding_registers,
        ir=input_registers
    )

    context = ModbusServerContext(slaves=slave_context, single=True)

    return await StartAsyncTlsServer(context=context, address=('127.0.0.1', 502), certfile='server.crt', keyfile='server.key')

async def async_helper():
    logging.info("Server Starting...")
    await run_server()

if __name__ == "__main__":
    asyncio.run(async_helper(), debug=True)
