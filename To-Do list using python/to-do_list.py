import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ModernToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern To-Do List")
        self.geometry("500x600")
        self.configure(bg="#1e1e1e")
        self.resizable(False, False)

        self.tasks = []
        self.history_file = "history.json"

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="📝 Modern To-Do", font=("Segoe UI", 24, "bold"))
        self.title_label.pack(pady=(20, 10))

        self.theme_switch = ctk.CTkSwitch(self, command=self.toggle_theme)
        self.theme_switch.pack(pady=(0, 10))

        if ctk.get_appearance_mode().lower() == "dark":
            self.theme_switch.select()
            self.theme_switch.configure(text="Dark Mode")
        else:
            self.theme_switch.deselect()
            self.theme_switch.configure(text="Light Mode")

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=10)

        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="Task", width=180)
        self.task_entry.grid(row=0, column=0, padx=10, pady=5)

        self.details_entry = ctk.CTkEntry(input_frame, placeholder_text="Details", width=180)
        self.details_entry.grid(row=0, column=1, padx=10, pady=5)

        self.task_listbox = ctk.CTkTextbox(self, height=250, corner_radius=10)
        self.task_listbox.pack(padx=20, pady=10, fill="both")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.add_btn = ctk.CTkButton(btn_frame, text="Add Task ✅", command=self.add_task, width=120, corner_radius=10)
        self.add_btn.grid(row=0, column=0, padx=10)

        self.delete_btn = ctk.CTkButton(btn_frame, text="Delete Task ❌", command=self.delete_task,
                                        fg_color="#d9534f", hover_color="#c9302c", width=120, corner_radius=10)
        self.delete_btn.grid(row=0, column=1, padx=10)

        self.logs_btn = ctk.CTkButton(self, text="📜 Task History", command=self.show_history, width=240, corner_radius=10)
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

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{task} - {details} @ {timestamp}"
        self.tasks.append(entry)
        self.task_listbox.insert("end", entry + "\n")
        self.save_tasks()
        self.log_history(f"✅ Task Added: {entry}")

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
            removed_task = self.tasks.pop()
            self.task_listbox.delete("1.0", "end")
            for task in self.tasks:
                self.task_listbox.insert("end", task + "\n")
            self.save_tasks()
            self.log_history(f"❌ Task Deleted: {removed_task}")

    def show_history(self):
        log_win = ctk.CTkToplevel(self)
        log_win.title("Task History")
        log_win.geometry("450x400")

        log_box = ctk.CTkTextbox(log_win)
        log_box.pack(padx=10, pady=10, fill="both", expand=True)

        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                history = json.load(f)
                for record in history:
                    log_box.insert("end", record + "\n")
        else:
            log_box.insert("end", "No history available.")

    def log_history(self, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {action}"

        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                history = json.load(f)

        history.append(entry)

        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=4)

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            confirm = messagebox.askyesno("Load Saved Tasks", "Do you want to load your previously saved tasks?")
            if confirm:
                with open("tasks.json", "r") as f:
                    self.tasks = json.load(f)
                    for task in self.tasks:
                        self.task_listbox.insert("end", task + "\n")
            else:
                self.tasks = []  # Start with a fresh list


if __name__ == "__main__":
    app = ModernToDoApp()
    app.mainloop()
