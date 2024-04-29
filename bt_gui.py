from typing import Any, Callable, Literal, Tuple, Union
from typing_extensions import Literal
import customtkinter
from bluetooth import BluetoothBox
from servo_control import controlsFrame
from message import messageFram


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title("舵机调试工具 B20041230")
        # self.geometry("1110x560")

        self.controls_frame = controlsFrame(self, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.controls_frame.grid(
            row=0, column=0, padx=(10, 0), pady=(10, 10), sticky="nsew"
        )

        self.messBox = messageFram(self)
        self.messBox.grid(row=0, column=1, padx=(10, 0), pady=(10, 10), sticky="nsew")

        self.bluetoothBox = BluetoothBox(self)
        self.bluetoothBox.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="nsew")

        # set width and height of window to title
        self.bind(self.set_width_height_to_title)
        self.configure(bg="white")

    def set_width_height_to_title(self):
        # get the width and height of the window
        width = self.winfo_width()
        height = self.winfo_height()
        print(width, height)

        # set the width and height of the window to the title
        self.geometry(f"{width}x{height}")


app = App()
app.mainloop()
