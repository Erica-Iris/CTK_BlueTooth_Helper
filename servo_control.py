import customtkinter
import binascii
import time
import serial.tools.list_ports
import serial
import struct
import structlog
from serial_ import Communication

log = structlog.get_logger()


class servo_control_row(customtkinter.CTkFrame):
    def __init__(self, master, servo_id: int):
        super().__init__(master, width=310)

        self.fontSetting = master.fontSetting

        self.servo_id = servo_id

        self.angle = customtkinter.IntVar()

        # 打开串口通信
        self.serial_engine = Communication(
            "/dev/cu.usbserial-11120", 115200, 0.5, DEBUG=False
        )

        self.grid_columnconfigure((0, 1, 2), weight=1)

        # 定义需要用到的控件
        self.servo_label = customtkinter.CTkLabel(self, text=f"Servo {servo_id}")

        self.angle_slider = customtkinter.CTkSlider(
            self,
            from_=0,
            to=180,
            command=self.slider_handel,
            number_of_steps=180,
            hover=False,
            variable=self.angle,
        )
        self.angle_slider.set(180)

        self.servo_angle_label = customtkinter.CTkLabel(self, text="180", width=20)

        # 控件布局
        self.servo_label.grid(row=0, column=0, padx=(10, 0), pady=5, stick="w")
        self.angle_slider.grid(row=0, column=1, padx=5, pady=5, stick="we")
        self.servo_angle_label.grid(row=0, column=2, padx=(0, 10), pady=5, stick="wsne")

    def slider_handel(self, _):
        angle = self.angle.get()
        log.info(f"Value of slider is {angle}.")
        self.servo_angle_label.configure(text=str(angle))
        if angle == 180 or angle == 0:
            return
        try:
            self.serial_engine.send_servo_command(angle=angle, servo_id=self.servo_id)
        except Exception as e:
            log.info(e)
        time.sleep(0.02)


class controlsFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master, width=320)

        self.fontSetting = master.fontSetting

        self.lists = []

        for i, v in enumerate(values):
            conline = servo_control_row(self, v)
            conline.grid(
                row=i, column=0, padx=5, pady=(10, 0 if i != len(values) - 1 else 10)
            )

            self.lists.append(conline)
