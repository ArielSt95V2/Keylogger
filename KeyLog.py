import streamlit as st
import keyboard
import threading
import datetime
import csv
import pandas as pd

class KeyLogger:
    def __init__(self):
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
                        if pressed_keys:
                            combination = '+'.join(pressed_keys) + '+' + key_name
                            writer.writerow([combination])
                        else:
                            writer.writerow([key_name])
                        pressed_keys.clear()
                    f.flush()
                elif event.event_type == keyboard.KEY_UP:
                    key_name = event.name
                    key_name = self.normalized_keys.get(key_name, key_name)
                    if key_name in self.special_keys:
                        pressed_keys.discard(key_name)

    def start_logging(self):
        if not self.is_logging:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.filename = f"log_{timestamp}.csv"
            self.is_logging = True
            self.stop_event.clear()
            self.log_thread = threading.Thread(target=self.log_keystrokes, daemon=True)
            self.log_thread.start()

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.stop_event.set()
            if self.log_thread:
                self.log_thread.join()

    def __enter__(self):
        self.start_logging()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_logging()

    def get_logged_data(self):
        if self.filename:
            return pd.read_csv(self.filename)
        return pd.DataFrame(columns=["Key Combination"])

# Streamlit UI setup
st.title('Keyboard Logger')

if st.button('Start Logging'):
    key_logger = KeyLogger()
    key_logger.__enter__()
    st.success(f"Logging started! Press 'Stop Logging' to stop and save to {key_logger.filename}.")
    st.session_state['key_logger'] = key_logger

if st.button('Stop Logging') and 'key_logger' in st.session_state:
    st.session_state['key_logger'].__exit__(None, None, None)
    st.success(f"Logging stopped! Check {st.session_state['key_logger'].filename} for recorded keystrokes.")
    logged_data = st.session_state['key_logger'].get_logged_data()
    st.write("Recorded Keystrokes:")
    st.dataframe(logged_data)
    del st.session_state['key_logger']
