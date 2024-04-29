from typing import Tuple
import customtkinter
import tkinter
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak import BleakScanner, BleakClient
import asyncio
import logging
import time

logger = logging.getLogger(__name__)

# def radiobutton_event():
#     print("radiobutton toggled, current value:", radio_var.get())


# def handle_add_button():
#     a_list.append(radio_var)
#     print(a_list)


class DeviceNotFoundError(Exception):
    pass


ADDRESS = "B5C7752B-8135-435E-CF59-3A14B7E1704C"
CHARACTERISTIC = "0000ffe1-0000-1000-8000-00805f9b34fb"
MAX_MESSAGE = 5


class blue(customtkinter.CTkScrollableFrame):
    def __init__(self, master, loop, interval=1 / 60):
        super().__init__(master)

        self.device_list = []
        self.device_list_item = []
        self.message_queue = asyncio.Queue()

        # client_task = self.run_ble_client(self, self.message_queue)
        # quetask = self.queue_handler(self.message_queue)

        # asyncio.gather(client_task, quetask)

        self.tasks = []
        self.tasks.append(loop.create_task(self.run_ble_client(self.message_queue)))
        self.tasks.append(loop.create_task(self.run_queue_consumer(self.message_queue)))
        self.tasks.append(loop.create_task(self.updater(interval)))

    async def updater(self, interval) -> None:
        while True:
            self.update()
            await asyncio.sleep(interval)
            # if len(self.message_queue)>MAX_MESSAGE:
                # dele the first in queue
                # self.message_queue.get_nowait()

    def add_item(self, device_item: BLEDevice):
        device_item = customtkinter.CTkLabel(self, text=device_item.name)
        device_item.grid(
            row=len(self.device_list), column=0, padx=10, pady=10, sticky="w"
        )
        self.device_list.append(device_item)
        self.device_list_item.append(device_item)

    async def add_item_str(self, device_item: str):
        device_item = customtkinter.CTkLabel(self, text=device_item)
        device_item.grid(
            row=len(self.device_list), column=0, padx=10, pady=10, sticky="w"
        )
        self.device_list.append(device_item)
        self.device_list_item.append(device_item)

    def clear_items(self):
        self.device_list = []
        self.device_list_item = []

    async def start_scanner(self):

        async with BleakScanner() as scanner:
            print("Scanning...")

            n = 15
            print(f"\n{n} advertisement packets:")
            for bd, ad in scanner.advertisement_data():
                print(f" {n}. {bd!r} with {ad!r}")
                bdd = await bd
                self.add_item(bdd)
                n -= 1
                if n == 0:
                    break

            # n = 10
            # print(f"\nFind device with name longer than {n} characters...")
            # async for bd, ad in scanner.advertisement_data():
            #     found = len(bd.name or "") > n or len(ad.local_name or "") > n
            #     print(f" Found{' it' if found else ''} {bd!r} with {ad!r}")
            #     if found:
            #         break

    async def run_ble_client(self, queue: asyncio.Queue):
        logger.info("starting scan...")

        device = await BleakScanner.find_device_by_address(
            ADDRESS, cb=dict(use_bdaddr=False)
        )
        if device is None:
            logger.error("could not find device with address ")
            raise DeviceNotFoundError

        logger.info("connecting to device...")

        async def callback_handler(_, data):
            await queue.put((time.time(), data))

        async with BleakClient(device) as client:
            logger.info("connected")
            await client.start_notify(CHARACTERISTIC, callback_handler)
            await asyncio.sleep(30.0)
            await client.stop_notify(CHARACTERISTIC)
            # Send an "exit command to the consumer"
            await queue.put((time.time(), None))

        logger.info("disconnected")

    async def run_queue_consumer(self, queue: asyncio.Queue):
        logger.info("Starting queue consumer")

        while True:
            # Use await asyncio.wait_for(queue.get(), timeout=1.0) if you want a timeout for getting data.
            epoch, data = await queue.get()
            if data is None:
                logger.info(
                    "Got message from client about disconnection. Exiting consumer loop..."
                )
                break
            else:
                logger.info("Received ", data)
                await self.add_item_str(str(data))


class App(customtkinter.CTk):
    def __init__(self, loop):
        super().__init__()

        self.blue1 = blue(self, loop=loop)
        self.blue1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def start_scan(self):
        raise NotImplementedError


loop = asyncio.get_event_loop()
app = App(loop=loop)
loop.run_forever()
app.mainloop()

# a_list = []
# radio_var = tkinter.IntVar(value=0)
# radiobutton_1 = customtkinter.CTkRadioButton(
#     app, text="CTkRadioButton 1", command=radiobutton_event, variable=radio_var, value=5
# )
# radiobutton_1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
# radiobutton_2 = customtkinter.CTkRadioButton(
#     app, text="CTkRadioButton 2", command=radiobutton_event, variable=radio_var, value=2
# )
# radiobutton_2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
# addButton = customtkinter.CTkButton(app, text="add", command=handle_add_button)
# addButton.grid(row=2, column=0, padx=10, pady=10, sticky="w")
