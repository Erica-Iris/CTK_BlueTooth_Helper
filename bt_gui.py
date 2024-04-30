import asyncio
from typing import Any, Callable, Literal, Tuple, Union
from typing_extensions import Literal
import customtkinter
from bluetooth import BluetoothBox
from servo_control import controlsFrame
from message import messageFram

customtkinter.set_appearance_mode("light")


class App(customtkinter.CTk):
    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__()

        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title("舵机调试工具 B20041230")
        # self.geometry("1110x560")

        self.controls_frame = controlsFrame(
            self, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        )
        self.controls_frame.grid(
            row=0, column=0, padx=(10, 0), pady=(10, 10), sticky="nsew"
        )

        self.messBox = messageFram(self, loop)
        self.messBox.grid(row=0, column=1, padx=(10, 0), pady=(10, 10), sticky="nsew")

        self.bluetoothBox = BluetoothBox(self)
        self.bluetoothBox.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="nsew")


loop = asyncio.get_event_loop()
app = App(loop)
loop.run_forever()
app.mainloop()
