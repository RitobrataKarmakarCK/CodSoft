import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import os

ctk.set_appearance_mode("System")  # Can be "Dark", "Light", or "System"
ctk.set_default_color_theme("blue")


class ModernToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern To-Do List")
        self.geometry("500x600")
        self.configure(bg="#1e1e1e")
        self.resizable(False, False)

        self.tasks = []

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        # Title
        self.title_label = ctk.CTkLabel(self, text="📝 Modern To-Do", font=("Segoe UI", 24, "bold"))
        self.title_label.pack(pady=(20, 10))

        # Theme Switch
        self.theme_switch = ctk.CTkSwitch(self, command=self.toggle_theme)
        self.theme_switch.pack(pady=(0, 10))

        # Set initial label based on current mode
        if ctk.get_appearance_mode().lower() == "dark":
            self.theme_switch.select()
            self.theme_switch.configure(text="Dark Mode")
        else:
            self.theme_switch.deselect()
            self.theme_switch.configure(text="Light Mode")

        # Task Inputs
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=10)

        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="Task", width=180)
        self.task_entry.grid(row=0, column=0, padx=10, pady=5)

        self.details_entry = ctk.CTkEntry(input_frame, placeholder_text="Details", width=180)
        self.details_entry.grid(row=0, column=1, padx=10, pady=5)

        # Task Listbox
        self.task_listbox = ctk.CTkTextbox(self, height=250, corner_radius=10)
        self.task_listbox.pack(padx=20, pady=10, fill="both")

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.add_btn = ctk.CTkButton(btn_frame, text="Add Task ✅", command=self.add_task, width=120, corner_radius=10)
        self.add_btn.grid(row=0, column=0, padx=10)

        self.delete_btn = ctk.CTkButton(btn_frame, text="Delete Task ❌", command=self.delete_task,
                                        fg_color="#d9534f", hover_color="#c9302c", width=120, corner_radius=10)
        self.delete_btn.grid(row=0, column=1, padx=10)

        self.logs_btn = ctk.CTkButton(self, text="📋 Daily Task Logs", command=self.show_logs, width=240, corner_radius=10)
        self.logs_btn.pack(pady=10)

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_switch.configure(text="Light Mode")

    def add_task(self):
        task = self.task_entry.get().strip()
        details = self.details_entry.get().strip()
        if not task or not details:
            messagebox.showwarning("Input Error", "Please enter both task and details.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry = f"{task} - {details} @ {timestamp}"
        self.tasks.append(entry)
        self.task_listbox.insert("end", entry + "\n")
        self.save_tasks()

        self.task_entry.delete(0, "end")
        self.details_entry.delete(0, "end")

    def delete_task(self):
        content = self.task_listbox.get("1.0", "end").strip().split("\n")
        if not content or not self.tasks:
            messagebox.showinfo("Empty", "No tasks to delete.")
            return

        selected_line = content[-1]
        confirm = messagebox.askyesno("Confirm Delete", f"Delete the last task?\n\n{selected_line}")
        if confirm:
            self.tasks.pop()
            self.task_listbox.delete("1.0", "end")
            for task in self.tasks:
                self.task_listbox.insert("end", task + "\n")
            self.save_tasks()

    def show_logs(self):
        log_win = ctk.CTkToplevel(self)
        log_win.title("Daily Task Logs")
        log_win.geometry("400x400")

        log_box = ctk.CTkTextbox(log_win)
        log_box.pack(padx=10, pady=10, fill="both", expand=True)

        for task in self.tasks:
            log_box.insert("end", task + "\n")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
                for task in self.tasks:
                    self.task_listbox.insert("end", task + "\n")


if __name__ == "__main__":
    app = ModernToDoApp()
    app.mainloop()
