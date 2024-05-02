from pickle import DICT
import customtkinter
import threading
from bleak import BleakScanner, BleakClient
import serial


class deviceBox(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.fontSetting = master.fontSetting

        self.SCAN_STATUS = customtkinter.StringVar(value="Stopped")
        self.mode = customtkinter.StringVar(value="Serial")
        self.devic_list = {}
        self.device_item_list = {}
        self.selected_device = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure((0, 2, 3), weight=0)

        self.devicesLabel = customtkinter.CTkLabel(
            self, text="Devices", font=self.fontSetting
        )
        self.swichModeButton = customtkinter.CTkSwitch(
            self, text=self.mode.get(), command=self.switch_event, font=self.fontSetting
        )
        self.deviceItemBox = deviceFrame(master=self, item_list=self.devic_list)
        self.scanButton = customtkinter.CTkButton(
            self,
            text="Start Scan Device",
            font=self.fontSetting,
            command=self.scan_event,
        )
        self.deviceInfoLabel = customtkinter.CTkLabel(
            self, text="Device Info", font=self.fontSetting
        )
        self.deviceInfoBox = BluetoothDeviceInfoBox(self)
        self.connectButton = customtkinter.CTkButton(
            self, text="Connect", font=self.fontSetting
        )

        self.devicesLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nws")
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

    def switch_event(self):
        if self.mode.get() == "BLE":
            self.mode.set("Serial")
            self.swichModeButton.configure(text="Serial")
            print("switch toggled, current value:", self.mode.get())
        elif self.mode.get() == "Serial":
            self.mode.set("BLE")
            self.swichModeButton.configure(text="BLE")
            print("Switch toggled, current value:", self.mode.get())

    def scan_Serial_Devices(self):
        for device_item in self.device_item_list:
            device_item.forgetgrid()

        ports_list = list(serial.tools.list_ports.comports())

        for comport in ports_list:
            self.devic_list[comport.name] = comport
            self.add_item(comport.name)
        self.scan_event()

    def scan_BLE_Devices(self):
        self.devic_list = {}
        ports_list = list(serial.tools.list_ports.comports())
        for comport in ports_list:
            print(comport[0], comport[1])
            self.add_item(comport[0])

    def scan_event(self):
        if self.SCAN_STATUS.get() == "Stopped":
            print("Start scan")
            self.SCAN_STATUS.set("Scanning")
            self.scanButton.configure(text="Stop Scan Device")
            if self.mode.get() == "Serial":
                self.scan_Serial_Devices()
        elif self.SCAN_STATUS.get() == "Scanning":
            print("Stopping scan")
            self.SCAN_STATUS.set("Stopped")
            self.scanButton.configure(text="Start Scan Device")
            if self.mode.get() == "BLE":
                self.scan_BLE_Devices()

    def add_item(self, name):
        self.device_item_list[name] = customtkinter.CTkButton(
            self.deviceItemBox,
            text=name,
            command=lambda: threading.Thread(
                target=self.select_device_handle, args=(name,), daemon=True
            ).start(),
        )
        self.device_item_list[name].pack(expand=True, fill="x", padx=5, pady=5)

    def select_device_handle(self, name):
        device = self.devic_list[name]
        # create multi line label about the info in device
        self.selected_device = device
        self.master.device = device
        # print(device.description)
        # print(device.device)
        # print(device.hwid)
        # print(device.interface)
        # print(device.location)
        # print(device.manufacturer)
        # print(device.name)
        # print(device.pid)
        # print(device.product)
        # print(device.serial_number)
        # print(device.vid)
        threading.Thread(target=self.deviceInfoBox.updateInfo, daemon=True).start()


class BluetoothDevice(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = customtkinter.CTkLabel(self, text="Device")
        self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")


class BluetoothDeviceInfoBox(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=180)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.des = customtkinter.StringVar()

        self.info_label = customtkinter.CTkLabel(
            self, text="No Device Selected", textvariable=self.des
        )
        self.info_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def fetch(self):
        self.selected_device = self.master.selected_device
        self.des = customtkinter.StringVar(value=self.selected_device.description)

    def updateInfo(self):
        self.fetch()
        selected_device = self.master.selected_device
        self.info_label.configure(text=selected_device.description)


class deviceFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, height=180, **kwargs)
        self.command = command
        self.device_list = []
        self.device_variable = customtkinter.StringVar()
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radioButton = customtkinter.CTkRadioButton(
            self, text=item, variable=self.device_variable, value=item
        )
        radioButton.grid(
            row=len(self.device_list), column=0, padx=10, pady=10, sticky="w"
        )
        self.device_list.append(radioButton)

    def get_checked_item(self):
        return self.device_variable.get()

    def radio_button_event(self):
        print("radiobutton toggled, current value:", self.device_variable.get())
