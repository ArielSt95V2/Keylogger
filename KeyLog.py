import tkinter as tk
from tkinter import messagebox, scrolledtext
import keyboard
import threading
import datetime
import csv
import pandas as pd

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Logger")
        self.is_logging = False
        self.log_thread = None
        self.filename = None
        self.stop_event = threading.Event()
        self.special_keys = {'ctrl', 'shift', 'alt', 'right shift', 'right ctrl', 'alt gr', 'right alt'}
        self.normalized_keys = {
            'right ctrl': 'ctrl',
            'right shift': 'shift',
            'alt gr': 'alt',
            'right alt': 'alt'
        }

        # UI Elements
        self.start_btn = tk.Button(root, text="Start Logging", command=self.start_logging, bg='green', fg='white')
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(root, text="Stop Logging", command=self.stop_logging, bg='red', fg='white', state=tk.DISABLED)
        self.stop_btn.pack(pady=10)

        self.log_display = scrolledtext.ScrolledText(root, height=15, width=60)
        self.log_display.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Not Logging", fg='blue')
        self.status_label.pack(pady=5)

    def log_keystrokes(self):
        pressed_keys = set()
        with open(self.filename, "a", newline='', buffering=1) as f:
            writer = csv.writer(f)
            writer.writerow(["Key Combination"])
            while not self.stop_event.is_set():
                event = keyboard.read_event(suppress=False)
                if event.event_type == keyboard.KEY_DOWN:
                    key_name = event.name
                    key_name = self.normalized_keys.get(key_name, key_name)
                    if key_name in self.special_keys:
                        pressed_keys.add(key_name)
                    else:
                        combination = '+'.join(pressed_keys) + '+' + key_name if pressed_keys else key_name
                        writer.writerow([combination])
                        self.log_display.insert(tk.END, combination + "\n")
                        self.log_display.see(tk.END)
                        pressed_keys.clear()
                elif event.event_type == keyboard.KEY_UP:
                    key_name = event.name
                    key_name = self.normalized_keys.get(key_name, key_name)
                    pressed_keys.discard(key_name)

    def start_logging(self):
        if not self.is_logging:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.filename = f"log_{timestamp}.csv"
            self.is_logging = True
            self.stop_event.clear()
            self.log_thread = threading.Thread(target=self.log_keystrokes, daemon=True)
            self.log_thread.start()

            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text=f"Status: Logging (Saving to {self.filename})")

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.stop_event.set()
            if self.log_thread:
                self.log_thread.join()

            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text=f"Status: Logging Stopped. File: {self.filename}")
            messagebox.showinfo("Logging Stopped", f"Keystrokes saved to {self.filename}")

# Create and run the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
