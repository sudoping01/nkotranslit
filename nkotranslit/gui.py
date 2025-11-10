#############################
#   Software Dependence     #
#############################
try:
    import tkinter
except ImportError:
    raise RuntimeError(
        "Tkinter is required for the GUI but is not installed. "
        "On Ubuntu/Debian, install it with: sudo apt install python3-tk"
    )




import customtkinter
from nkotranslit.convert import NkoLatinConverter

customtkinter.set_appearance_mode("system")


class NkoTranslitApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("NkoTranslit GUI (Latin ↔ N'Ko)")
        self.geometry("900x600")
        self.updating = False
        self.converter = NkoLatinConverter()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.latin_font = customtkinter.CTkFont(family="Arial", size=18)
        self.nko_font = customtkinter.CTkFont(family="Noto Sans NKo", size=18)

        customtkinter.CTkLabel(self, text="Bambara (Latin)", font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        customtkinter.CTkLabel(self, text="Bambara (N'Ko)", font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=0, column=1, padx=20, pady=(10, 0), sticky="w")

        self.latin_textbox = customtkinter.CTkTextbox(self, font=self.latin_font, wrap="word")
        self.latin_textbox.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        self.nko_textbox = customtkinter.CTkTextbox(self, font=self.nko_font, wrap="word")
        self.nko_textbox.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")

        self.mode_switch = customtkinter.CTkSwitch(self, text="Toggle Dark/Light", command=self.toggle_mode)
        self.mode_switch.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 10))
        if customtkinter.get_appearance_mode() == "Dark":
            self.mode_switch.select()


        self.latin_textbox.bind("<KeyRelease>", self.on_latin_change)
        self.nko_textbox.bind("<KeyRelease>", self.on_nko_change)

    def toggle_mode(self):
        mode = "dark" if self.mode_switch.get() else "light"
        customtkinter.set_appearance_mode(mode)

    def on_latin_change(self, event=None):
        if self.updating: return
        self.updating = True
        try:
            latin_text = self.latin_textbox.get("1.0", "end-1c")
            nko_text = self.converter.convert_text(latin_text, rules=self.converter.LATIN_TO_NKO_RULES)
            self.nko_textbox.delete("1.0", "end")
            self.nko_textbox.insert("1.0", nko_text)
        finally:
            self.updating = False

    def on_nko_change(self, event=None):
        if self.updating: return
        self.updating = True
        try:
            nko_text = self.nko_textbox.get("1.0", "end-1c")
            latin_text = self.converter.convert_text(nko_text, rules=self.converter.NKO_TO_LATIN_RULES)
            self.latin_textbox.delete("1.0", "end")
            self.latin_textbox.insert("1.0", latin_text)
        finally:
            self.updating = False


def launch_gui():
    app = NkoTranslitApp()
    app.mainloop()


if __name__ == "__main__":
    launch_gui()