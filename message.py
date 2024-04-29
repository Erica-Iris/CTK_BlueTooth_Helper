import customtkinter


class messageFram(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=1)

        self.label = customtkinter.CTkLabel(self, text="MessageBox")
        self.label.grid(
            row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w"
        )

        self.messageBox = customtkinter.CTkTextbox(self)
        self.messageBox.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="wsne"
        )

        self.sendMessageLabel = customtkinter.CTkLabel(self, text="Send Message")
        self.sendMessageLabel.grid(
            row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="w"
        )

        self.sendMessage = customtkinter.CTkEntry(self)
        self.sendMessage.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="we")

        self.hexSend = customtkinter.CTkCheckBox(self, text="Hex")
        self.hexSend.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="we")

        self.sendButton = customtkinter.CTkButton(self, text="Send")
        self.sendButton.grid(
            row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we"
        )
