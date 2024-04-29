import customtkinter


class servo_control_row(customtkinter.CTkFrame):
    def __init__(self, master, servo_id):
        super().__init__(master, width=310)

        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.servo_label = customtkinter.CTkLabel(
            self, text="Servo " + "{:02}".format(servo_id)
        )
        self.servo_label.grid(row=0, column=0, padx=(10, 0), pady=5, stick="w")

        self.angle_slider = customtkinter.CTkSlider(
            self,
            from_=0,
            to=180,
            command=self.slider_handel,
            number_of_steps=180,
            hover=True,
        )
        self.angle_slider.grid(row=0, column=1, padx=5, pady=5, stick="we")

        self.servo_angle_label = customtkinter.CTkLabel(self, text="090", width=20)
        self.servo_angle_label.grid(row=0, column=2, padx=(0, 10), pady=5, stick="wsne")

        # self.servo_angle_label.configure(command=self.set_label_text)

    def get_slider_value(self):
        return str(int(self.angle_slider.get()))

    def set_label_text(self):
        angle_float = self.get_slider_value
        self.servo_angle_label.configure(text=angle_float)

    def slider_handel(self, value):
        angle_float = self.angle_slider.get()
        self.servo_angle_label.configure(text="{:03}".format(int(angle_float)))


class controlsFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master, width=320)

        self.lists = []

        for i, v in enumerate(values):
            conline = servo_control_row(self, i)
            conline.grid(row=i, column=0, padx=5, pady=(10, 0))
            self.lists.append(conline)
