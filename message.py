import asyncio
import customtkinter
import logging
import structlog
import sys
import serial
import time
import threading
from const import ADDRESS, CHARACTERISTIC
from bleak import BleakScanner, BleakClient
from Device import DeviceNotFoundError
from serial_ import Communication


log = structlog.get_logger()


class messageFram(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.fontSetting = master.fontSetting

        # 设置grid布局权重
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 设置变量
        self.ADDRESS = "B5C7752B-8135-435E-CF59-3A14B7E1704C"
        self.CHARACTERISTIC = "0000ffe1-0000-1000-8000-00805f9b34fb"
        self.MAX_MESSAGE = 5

        self.device = self.master.device

        self.label = customtkinter.CTkLabel(
            self, text="MessageBox", font=self.fontSetting
        )
        self.messageBox = messageBox(
            self, address=ADDRESS, characteristic=CHARACTERISTIC
        )
        self.listenButton = customtkinter.CTkButton(
            self, text="Start Listen", font=self.fontSetting, command=self.start_listen
        )
        self.sendMessageLabel = customtkinter.CTkLabel(
            self, text="Send Message", font=self.fontSetting
        )
        self.sendMessageEntry = customtkinter.CTkEntry(self)

        self.sendButton = customtkinter.CTkButton(
            self, text="Send Message", command=self.send_msg, font=self.fontSetting
        )

        self.label.grid(
            row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w"
        )
        self.messageBox.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="news"
        )
        self.listenButton.grid(
            row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew"
        )
        self.sendMessageLabel.grid(
            row=3, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w"
        )
        self.sendMessageEntry.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="we")
        # self.hexSend.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="ew")
        self.sendButton.grid(
            row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

    def send_msg(self):
        # get value from entry and send it to the device
        message = self.sendMessage.get()
        print(message)

    def start_listen(self):
        self.device = self.master.device
        if self.device == None:
            log.info("No device select.")
            return
        self.serial_engine = Communication(self.device.device, 115200, 0.5, DEBUG=False)
        threading.Thread(target=self.serial_engine.Recive_data).start()


class messageBox(customtkinter.CTkScrollableFrame):
    def __init__(
        self,
        master,
        interval=1 / 60,
        address=ADDRESS,
        characteristic=CHARACTERISTIC,
    ):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.device_list = []
        self.device_list_item = []

        # 消息队列
        self.message_queue = asyncio.Queue()

        self.ADDRESS = address
        self.CHARACTERISTIC = characteristic

        self.msg_pointer = 0

        self.tasks = []

        self.client = None

    async def updater(self, interval) -> None:
        while True:
            self.update()
            await asyncio.sleep(interval)

    async def add_message(self, msg_str: str):
        msg_row = customtkinter.CTkLabel(
            self,
            text=msg_str,
            justify=customtkinter.LEFT,
            compound="left",
            bg_color="white",
        )
        msg_row.grid(row=self.msg_pointer, column=0, padx=5, pady=(5, 0), sticky="nw")
        self.msg_pointer += 1

    async def run_ble_client(self, queue: asyncio.Queue):
        logger.info("starting scan...")

        device = await BleakScanner.find_device_by_address(
            self.ADDRESS, cb=dict(use_bdaddr=False)
        )
        if device is None:
            logger.error("could not find device with address ")
            raise DeviceNotFoundError

        logger.info("connecting to device...")

        async def callback_handler(_, data):
            await queue.put((time.time(), data))

        async with BleakClient(device) as client:
            logger.info("connected")
            self.client = client
            await client.start_notify(self.CHARACTERISTIC, callback_handler)
            await asyncio.sleep(30.0)
            # await client.stop_notify(self.CHARACTERISTIC)
            # Send an "exit command to the consumer"
            await queue.put((time.time(), None))

        logger.info("disconnected")

    def stop_Lis(self):
        # await self.client.stop_notify(self.CHARACTERISTIC)
        asyncio.run(self.client.stop_notify(self.CHARACTERISTIC))

    async def start(self):
        await self.client.start_notify(self.CHARACTERISTIC)

    async def run_queue_consumer(self, queue: asyncio.Queue):
        logger.info("Starting queue consumer")

        while True:
            # Use await asyncio.wait_for(queue.get(), timeout=1.0) if you want a timeout for getting data.
            # epoch, data =  await asyncio.wait_for(queue.get(), timeout=5.0)
            epoch, data = await queue.get()
            if data is None:
                logger.info(
                    "Got message from client about disconnection. Exiting consumer loop..."
                )
                break
            else:
                logger.info("Received %r", data)
                await self.add_message(data.decode("utf-8"))
