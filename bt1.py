import asyncio
from bleak import BleakScanner
from bleak import BleakClient
from bleak import _logger as logger
import time
import structlog

log = structlog.get_logger()

UID_1 = "B5C7752B-8135-435E-CF59-3A14B7E1704C"


async def read_data(address):
    async with BleakClient(address) as client:
        # await client.start_notify("FFE1", notification_handler)  # You assigned this a name.  Use the name.
        # await client.write_gatt_char(
        #     "0000ffe2-0000-0000-0000-000000000000", bytearray([0xAA, 0x04, 0xB4, 0x62])
        # )
        await client.connect()
        await client.read_gatt_char(
            "0000ffe1-0000-1000-8000-00805f9b34fb",
        )
        time.sleep(1)
        while True:
            await client.write_gatt_char(
                "0000ffe2-0000-1000-8000-00805f9b34fb",
                bytearray([0xAA, 0x04, 0xB4, 0x62]),
            )
            await asyncio.sleep(1)
            await client.write_gatt_char(
                "0000ffe2-0000-1000-8000-00805f9b34fb",
                bytearray([0xAA, 0x04, 0x00, 0xAE]),
            )


async def notification_handler(sender, data):
    log.info("Sender:", sender)


async def main(address):
    await read_data(address)


asyncio.run(main(UID_1))
