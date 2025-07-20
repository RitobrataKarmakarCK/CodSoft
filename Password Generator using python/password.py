import customtkinter as ctk
import random
import string
import pyperclip

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# App Window
app = ctk.CTk()
app.geometry("360x530")
app.title("Generate Password")

# ------------------- Password Generation Logic -------------------
def generate_password():
    password_entry.configure(state="normal")  # Enable entry temporarily
    length = int(length_slider.get())
    chars = ''
    if uppercase_var.get(): chars += string.ascii_uppercase
    if lowercase_var.get(): chars += string.ascii_lowercase
    if numbers_var.get(): chars += string.digits
    if symbols_var.get(): chars += string.punctuation

    password_entry.delete(0, ctk.END)

    if not chars:
        password_entry.configure(state="disabled")
        return

    password = ''.join(random.choice(chars) for _ in range(length))
    password_entry.insert(0, password)
    password_entry.configure(state="readonly")  # Make it readonly after generating

def copy_password():
    try:
        current_password = password_entry.get()
        # Only copy if there's actual text that looks like a password (not empty or "Select options")
        if current_password and current_password != "Select options":
            pyperclip.copy(current_password)
    except pyperclip.PyperclipException:
        print("Failed to copy to clipboard. Pyperclip might not be configured correctly.")


# ------------------- UI Layout -------------------

# Title
title_label = ctk.CTkLabel(app, text="Generate password", font=("Segoe UI", 20, "bold"))
title_label.pack(pady=(20, 10))

# Password Box Frame
password_frame = ctk.CTkFrame(app, fg_color="#2a2b36", corner_radius=12)
password_frame.pack(pady=(5, 10), padx=20, fill="x")

# Password Entry
password_entry = ctk.CTkEntry(password_frame, font=("Segoe UI", 16), height=40)
password_entry.pack(padx=10, pady=(10, 0), fill="x")
password_entry.configure(state="disabled")  # Disable the entry initially

# Copy & Refresh Buttons
btn_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
btn_frame.pack(pady=10)

copy_btn = ctk.CTkButton(btn_frame, text="📋", width=40, command=copy_password, fg_color="#3a3b4d", hover_color="#50516c", font=("Segoe UI", 16))
copy_btn.pack(side="left", padx=5)

refresh_btn = ctk.CTkButton(btn_frame, text="🔁", width=40, command=generate_password, fg_color="#3a3b4d", hover_color="#50516c", font=("Segoe UI", 16))
refresh_btn.pack(side="left", padx=5)

# Character Length
length_label = ctk.CTkLabel(app, text="Character Length:", font=("Segoe UI", 14))
length_label.pack(pady=(15, 0))

length_slider = ctk.CTkSlider(app, from_=4, to=32, number_of_steps=28, progress_color="#b36bff", button_color="#b36bff", button_hover_color="#a15ef0")
length_slider.set(12)
length_slider.pack(pady=(5, 0), padx=20, fill="x")

length_value = ctk.CTkLabel(app, text="12", font=("Segoe UI", 14))
length_value.pack(pady=(2, 10))

def update_slider_value(value):
    length_value.configure(text=str(int(value)))
    # The slider adjustment itself does not trigger password generation

length_slider.configure(command=update_slider_value)

# Toggle Settings
def create_toggle(text, variable):
    frame = ctk.CTkFrame(app, fg_color="#2a2b36", corner_radius=8)
    frame.pack(pady=5, padx=20, fill="x")
    label = ctk.CTkLabel(frame, text=text, font=("Segoe UI", 14))
    label.pack(side="left", padx=10)
    toggle = ctk.CTkSwitch(
        frame,
        variable=variable,
        text="",
        onvalue=True,
        offvalue=False,
        progress_color="#b36bff",  # Purple for the track when ON
        button_color="#FFFFFF",     # White for the thumb
        button_hover_color="#E0E0E0", # Light gray for thumb hover
        fg_color="#3a3b4d",         # Darker color for the track when OFF
        # Toggles themselves do not trigger password generation
    )
    toggle.pack(side="right", padx=10)
    return toggle

uppercase_var = ctk.BooleanVar(value=True)
lowercase_var = ctk.BooleanVar(value=True)
numbers_var = ctk.BooleanVar(value=True)
symbols_var = ctk.BooleanVar(value=False)

create_toggle("Include uppercase letters", uppercase_var)
create_toggle("Include lowercase letters", lowercase_var)
create_toggle("Include numbers", numbers_var)
create_toggle("Include symbols", symbols_var)

# Generate Button
generate_btn = ctk.CTkButton(
    app,
    text="Generate Password",
    height=40,
    fg_color="#b36bff",
    hover_color="#a15ef0",
    font=("Segoe UI", 14),
    corner_radius=16,
    command=generate_password
)
generate_btn.pack(pady=(20, 20), padx=40, fill="x")

# Run App
app.mainloop()
