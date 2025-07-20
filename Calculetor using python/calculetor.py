import customtkinter as ctk

class CompactCalculator:
    def __init__ (self, root):
        self.root = root
        self.root.title("Compact Calculator")
        self.root.geometry("320x540")  # Smaller window
        self.root.resizable(False, False)

        self.theme = "dark"
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.expression = ""
        self.input_text = ctk.StringVar()

        self.create_header()
        self.create_display()
        self.create_buttons()

    def create_header(self):
        top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=(10, 5))

        label = ctk.CTkLabel(top_frame, text="🧮 Calc", font=("Segoe UI", 16))
        label.pack(side="left")

        self.mode_btn = ctk.CTkButton(
            top_frame, text="☾", width=32, height=32,
            corner_radius=8, font=("Segoe UI", 18),
            fg_color="#333", hover_color="#555",
            command=self.toggle_mode
        )
        self.mode_btn.pack(side="right")

    def create_display(self):
        self.entry = ctk.CTkEntry(
            self.root, textvariable=self.input_text, font=("Segoe UI", 24),
            justify="right", width=280, height=50, corner_radius=8,
            fg_color=self.get_bg(),
            text_color="white" if self.theme == "dark" else "black"
        )
        self.entry.pack(pady=(10, 10), padx=15)

    def create_buttons(self):
        self.btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.btn_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.buttons = [
            ["AC", "%", "⌫", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["00", "0", ".", "="]
        ]

        self.render_buttons()

    def render_buttons(self):
        for widget in self.btn_frame.winfo_children():
            widget.destroy()

        for r, row in enumerate(self.buttons):
            for c, char in enumerate(row):
                bg = "#ff9f0a" if char == "=" else self.get_button_color()
                text_col = "white" if self.theme == "dark" or char == "=" else "black"

                btn = ctk.CTkButton(
                    self.btn_frame, text=char, font=("Segoe UI", 18),
                    width=60, height=60, corner_radius=8,
                    fg_color=bg, hover_color=self.get_hover_color(),
                    text_color=text_col, command=lambda ch=char: self.on_click(ch)
                )
                btn.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")

        for i in range(5):
            self.btn_frame.rowconfigure(i, weight=1)
        for i in range(4):
            self.btn_frame.columnconfigure(i, weight=1)

    def get_bg(self):
        return "#121212" if self.theme == "dark" else "#f5f5f5"

    def get_button_color(self):
        return "#2c2c2c" if self.theme == "dark" else "#d3d3d3"

    def get_hover_color(self):
        return "#3a3a3a" if self.theme == "dark" else "#bfbfbf"

    def toggle_mode(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        ctk.set_appearance_mode(self.theme)
        self.mode_btn.configure(text="☀" if self.theme == "light" else "☾")
        self.entry.configure(fg_color=self.get_bg(),
        text_color="black" if self.theme == "light" else "white")
        self.render_buttons()

    def on_click(self, char):
        if char == "AC":
            self.expression = ""
        elif char == "⌫":
            self.expression = self.expression[:-1]
        elif char == "=":
            try:
                exp = self.expression.replace("×", "*").replace("÷", "/")
                self.expression = str(eval(exp))
            except:
                self.expression = "Error"
        else:
            self.expression += str(char)
        self.input_text.set(self.expression)

if __name__ == "__main__":
    root = ctk.CTk()
    CompactCalculator(root)
    root.mainloop()
