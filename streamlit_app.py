# streamlit_app.py
import subprocess
import sys

def launch_streamlit():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    launch_streamlit()
