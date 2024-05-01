import customtkinter

from bleak import BleakScanner, BleakClient


class deviceBox(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.fontSetting = master.fontSetting

        self.scan_status = False
        self.mode = customtkinter.StringVar(value="Serial")
        self.DEVICE = []

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
        self.bluetooth_device_box = deviceFrame(master=self, item_list=self.DEVICE)
        self.scanButton = customtkinter.CTkButton(
            self, text="Start Scan", font=self.fontSetting
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
        self.bluetooth_device_box.grid(
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
            print("switch toggled, current value:", self.mode.get())

    def startscan(self):
        if self.scan_status:
            print("stop scan")
            self.scan_status = False
            self.scanButton.configure(text="Start Scan")
        else:
            print("start scan")
            self.scan_status = True
            self.scanButton.configure(text="Stop Scan")


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

        self.info_label = customtkinter.CTkLabel(self, text="No Device Selected")
        self.info_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def set_current_device_info(self, device_info):
        self.info_label.config(text=device_info)


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
