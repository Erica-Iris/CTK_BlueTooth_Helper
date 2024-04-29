import customtkinter

from bleak import BleakScanner, BleakClient


class BluetoothBox(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.scan_status = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure((0, 2, 3), weight=0)

        self.devicesLabel = customtkinter.CTkLabel(self, text="Devices")
        self.devicesLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="snw")

        bluetooth_device_box = ScrollableBluetoothFrame(
            master=self, item_list=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        )
        bluetooth_device_box.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.scan_button = customtkinter.CTkButton(
            self, text="Start Scan", command=self.startscan
        )
        self.scan_button.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")

        blue_device_info_label = customtkinter.CTkLabel(self, text="Device Info")
        blue_device_info_label.grid(
            row=3, column=0, padx=10, pady=(10, 0), sticky="snw"
        )

        bluetooth_device_info_box = BluetoothDeviceInfoBox(self)
        bluetooth_device_info_box.grid(
            row=4, column=0, padx=10, pady=(10, 0), sticky="nsew"
        )

        self.connectButton = customtkinter.CTkButton(self, text="Connect")
        self.connectButton.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10, sticky="wse"
        )

    def startscan(self):
        if self.scan_status:
            print("stop scan")
            self.scan_status = False
            self.scan_button.configure(text="Start Scan")
        else:
            print("start scan")
            self.scan_status = True
            self.scan_button.configure(text="Stop Scan")


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


class ScrollableBluetoothFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, height=180, **kwargs)
        self.command = command
        self.device_list = []
        self.device_variable = customtkinter.StringVar()
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        # device = BluetoothDevice(self)
        # self.device_list.append(device)
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


# tk_textbox = customtkinter.CTkTextbox(self, activate_scrollbars=False)
# tk_textbox.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

# # create CTk scrollbar
# ctk_textbox_scrollbar = customtkinter.CTkScrollbar(
#     self, command=tk_textbox.yview
# )
# ctk_textbox_scrollbar.grid(
#     row=1, column=1, padx=(0, 1), pady=(10, 0), sticky="ns"
# )

# # connect textbox scroll event to CTk scrollbar
# tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)
