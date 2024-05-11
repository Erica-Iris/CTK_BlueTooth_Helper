import customtkinter as ctk
import threading
import serial
import structlog
from bleak import BleakScanner, BleakClient


log = structlog.get_logger()


class deviceBox(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.fontSetting = master.fontSetting

        self.SCAN_STATUS = ctk.StringVar(value="Stopped")
        self.mode = ctk.StringVar(value="Serial")
        self.device_list = {}
        self.device_item_list = {}
        self.selected_device = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure((0, 2, 3), weight=0)

        self.deviceLabel = ctk.CTkLabel(self, text="Devices", font=self.fontSetting)
        self.swichModeButton = ctk.CTkSwitch(
            self,
            text=self.mode.get(),
            command=self.switch_toggle,
            font=self.fontSetting,
        )
        self.deviceItemBox = deviceFrame(master=self)
        self.scanButton = ctk.CTkButton(
            self,
            text="Start Scan Device",
            font=self.fontSetting,
            command=self.scan_event,
        )
        self.deviceInfoLabel = ctk.CTkLabel(
            self, text="Device Info", font=self.fontSetting
        )
        self.deviceInfoBox = deviceInfoBox(self)
        self.connectButton = ctk.CTkButton(self, text="Connect", font=self.fontSetting)

        self.deviceLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nws")
        self.swichModeButton.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nws")
        self.deviceItemBox.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="news"
        )
        self.scanButton.grid(
            row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="news"
        )
        self.deviceInfoLabel.grid(
            row=3, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nws"
        )
        self.deviceInfoBox.grid(
            row=4, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="news"
        )
        self.connectButton.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ews"
        )

    def switch_toggle(self):
        if self.mode.get() == "BLE":
            self.mode.set("Serial")
            self.swichModeButton.configure(text="Serial")
            log.info(f"Switch toggled, current value: {self.mode.get()}.")
        elif self.mode.get() == "Serial":
            self.mode.set("BLE")
            self.swichModeButton.configure(text="BLE")

    def scan_event(self):
        self.toggle_scan_status()
        if self.mode.get() == "Serial":
            self.scan_Serial_Devices()
        elif self.mode.get() == "BLE":
            self.scan_BLE_Devices()
            log.info(f"Switch toggled, current value: {self.mode.get()}.")

    def scan_Serial_Devices(self):
        log.info(self.device_list)
        self.deviceItemBox.remove_all()
        ports_list = list(serial.tools.list_ports.comports())

        for comport in ports_list:
            self.device_list[comport.name] = comport
            self.deviceItemBox.add_item(comport.name)

        self.toggle_scan_status()

    def scan_BLE_Devices(self):
        self.device_list = {}
        ports_list = list(serial.tools.list_ports.comports())
        for comport in ports_list:
            self.add_item(comport[0])

    def toggle_scan_status(self):
        if self.SCAN_STATUS.get() == "Stopped":
            log.info("Start scanning...")
            self.SCAN_STATUS.set("Scanning")
            self.scanButton.configure(text="Stop Scan Device")
        elif self.SCAN_STATUS.get() == "Scanning":
            log.info("Scan finished/stopped.")
            self.SCAN_STATUS.set("Stopped")
            self.scanButton.configure(text="Start Scan Device")

    def add_item(self, name):
        self.device_item_list[name] = ctk.CTkButton(
            self.deviceItemBox,
            text=name,
            fg_color="gray65",
            command=lambda: threading.Thread(
                target=self.select_device_handle, args=(name,), daemon=True
            ).start(),
        )
        self.device_item_list[name].pack(expand=True, fill="x", padx=5, pady=5)

    def select_device_handle(self, name):
        device = self.device_list[name]
        # create multi line label about the info in device
        self.selected_device = device
        self.master.device = device
        log.info(device.description)
        log.info(device.device)
        log.info(device.hwid)
        log.info(device.interface)
        log.info(device.location)
        log.info(device.manufacturer)
        log.info(device.name)
        log.info(device.pid)
        log.info(device.product)
        log.info(device.serial_number)
        log.info(device.vid)
        threading.Thread(target=self.deviceInfoBox.updateInfo, daemon=True).start()


class deviceInfoBox(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=180)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.des = ctk.StringVar()

        self.info_label = ctk.CTkLabel(
            self, text="No Device Selected", textvariable=self.des
        )
        self.info_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def fetch(self):
        self.selected_device = self.master.selected_device
        # self.des = customtkinter.StringVar(value=self.selected_device.description)

    def updateInfo(self):
        log.info("Updating device info not implemented yet.")


class deviceFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, height=180, **kwargs)
        self.command = command
        self.device_list = []
        self.device_variable = ctk.StringVar()

    def add_item(self, name):
        button = ctk.CTkButton(self, text=name, fg_color="gray65")
        button.grid(row=len(self.device_list), column=0, sticky="ew")

    def remove_all(self):
        log.info("Removing all devices...")
        for device in self.device_list:
            device.destroy()
            log.info(f"Removeing {device.name}...")
        self.device_list = []
        log.info("All devices removed.")
