import customtkinter
import binascii
import time
import serial.tools.list_ports
import serial
import struct

from serial_ import Communication


class servo_control_row(customtkinter.CTkFrame):
    def __init__(self, master, servo_id: int):
        super().__init__(master, width=310)

        self.servo_id = servo_id

        self.angle = 180

        # 打开串口通信
        self.serial_engine = Communication(
            "/dev/cu.usbserial-1120", 115200, 0.5, DEBUG=False
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
        )

        self.servo_angle_label = customtkinter.CTkLabel(self, text="180", width=20)

        # 控件布局
        self.servo_label.grid(row=0, column=0, padx=(10, 0), pady=5, stick="w")
        self.angle_slider.grid(row=0, column=1, padx=5, pady=5, stick="we")
        self.servo_angle_label.grid(row=0, column=2, padx=(0, 10), pady=5, stick="wsne")

    def slider_handel(self, value):
        value = int(value)
        self.servo_angle_label.configure(text=str(value))
        if str(value) == "180" or str(value) == "0":
            return
        print(f"Set {self.servo_id}, angle: {value}")
        self.serial_engine.send_servo_command(value, servo_id=self.servo_id)
        time.sleep(0.02)


class controlsFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master, width=320)

        self.lists = []

        for i, v in enumerate(values):
            conline = servo_control_row(self, v)
            conline.grid(
                row=i, column=0, padx=5, pady=(10, 0 if i != len(values) - 1 else 10)
            )

            self.lists.append(conline)
