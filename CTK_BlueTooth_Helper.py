"""
Servo control tool
Author: 1ris_W()
Version: 0.1
"""

try:
    import asyncio
    import os
    import structlog
    import sys
    import customtkinter
    from deviceBox import deviceBox
    from deviceBox import deviceBox
    from servo_control import controlsFrame
    from message import messageFram
except Exception as e:
    import os

    os.system("pip install -r requirements.txt")

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("./purple.json")

log = structlog.get_logger()


class App(customtkinter.CTk):

    DIRPATH = os.path.join(os.path.dirname(__file__))

    def __init__(self, loop: asyncio.AbstractEventLoop):
        super().__init__()
        if sys.platform.startswith("win"):
            self.font = "Segoe UI"
        else:
            self.font = customtkinter.ThemeManager.theme["CTkFont"]["family"]

        self.fontSetting = (self.font, 17, "bold")

        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title("Servo Testing Toolkit")
        self.width = int(self.winfo_screenwidth() / 2)
        self.height = int(self.winfo_screenheight() / 1.5)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(880, 800)

        self.device = None

        self.controls_frame = controlsFrame(
            self, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        )
        self.messageBox = messageFram(self, loop)
        self.bluetoothBox = deviceBox(self)

        self.controls_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="news")
        self.messageBox.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="news")
        self.bluetoothBox.grid(row=0, column=2, padx=10, pady=10, sticky="news")
        
        os.system("clear")
        
        log.info("App loadding done.")


loop = asyncio.get_event_loop()
app = App(loop)
loop.run_forever()
app.mainloop()
