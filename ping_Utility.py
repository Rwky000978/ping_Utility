import subprocess
import tkinter as tk
from tkinter import Label, Button, Frame, Text, Scrollbar
import threading
import re
import winsound  # Import the winsound module

# Flag to signal the ping thread to stop
stop_ping_flag = threading.Event()

def ping_host():
    ip = entry_ip.get()
    if not ip:
        status_label.config(text="Status: Enter IP Address", bg='#800000', fg='white')
        return
    start_ping(ip)

def start_ping(ip):
    global ping_thread
    ping_thread = threading.Thread(target=ping_ip, args=(ip,))
    ping_thread.start()

def stop_ping():
    stop_ping_flag.set()  # Set the flag to signal the ping thread to stop
    button_stop.config(state=tk.DISABLED)  # Disable the stop button temporarily
    button_start.config(state=tk.NORMAL)   # Enable the start button

def tracert_ip(ip):
    try:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result = subprocess.run(['tracert', ip], capture_output=True, text=True, timeout=90)
        result_text.insert(tk.END, result.stdout)
    except Exception as e:
        print("Error:", e)
    finally:
        result_text.config(state=tk.DISABLED)

def ping_ip(ip):
    try:
        stop_ping_flag.clear()  # Clear the stop flag at the beginning of the ping operation
        while not stop_ping_flag.is_set():  # Continue pinging until the stop flag is set
            result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=5)
            match = re.search(r"time=(\d+)ms", result.stdout)
            if match:
                round_trip_time = int(match.group(1))
                round_trip_time_str = f"{round_trip_time}ms"
                if round_trip_time > 200:
                    rt_label.config(fg='red')
                    winsound.Beep(1000, 200)
                elif round_trip_time > 100:
                    rt_label.config(fg='yellow')
                else:
                    rt_label.config(fg='white')
            else:
                round_trip_time_str = 'Round-trip time not found'
                rt_label.config(fg='white')

            if result.returncode == 0:
                status_label.config(text="Status: Online", bg='#008000')
            else:
                status_label.config(text="Status: Offline", bg='#800000')

            rt_label.config(text=f"Time: {round_trip_time_str}")
            status_label_ping.config(text=f"Pinging: {ip}")
            threading.Event().wait(1)

    except subprocess.TimeoutExpired:
        round_trip_time_str = 'Timeout'
        status_label.config(bg='#808000')
        rt_label.config(fg='white')
        rt_label.config(text=f"Time: {round_trip_time_str}")
    finally:
        button_stop.config(state=tk.NORMAL)  # Re-enable the stop button once the ping operation finishes
        status_label.config(text="Status: Idle")

root = tk.Tk()
root.title("Ping Utility")
root.configure(bg='#303030')
root.attributes('-alpha', 0.8)

frame = Frame(root, bg='#303030')
frame.pack(padx=10, pady=10)

label_ip = Label(frame, text="Enter IP Address:", bg='#303030', fg='white')
label_ip.pack(side=tk.LEFT, padx=(0, 10), pady=5)

entry_ip = tk.Entry(frame)
entry_ip.pack(side=tk.LEFT, padx=(0, 10), pady=5)

button_start = Button(frame, text="Start Ping", bg='#606060', fg='white', command=ping_host)
button_start.pack(side=tk.LEFT, padx=(0, 10), pady=5)

button_stop = Button(frame, text="Stop Ping", bg='#606060', fg='white', command=stop_ping)
button_stop.pack(side=tk.LEFT, padx=(0, 10), pady=5)

button_tracert = Button(frame, text="Tracert", bg='#606060', fg='white', command=lambda: tracert_ip(entry_ip.get()))
button_tracert.pack(side=tk.LEFT, padx=(0, 10), pady=5)

status_label = Label(root, text="Status: Idle", bg='#303030', fg='white')
status_label.pack(pady=5)

status_label_ping = Label(root, text="", bg='#303030', fg='white')
status_label_ping.pack(pady=5)

rt_label = Label(root, text="", bg='#303030', fg='white')
rt_label.pack(pady=5)

result_text_frame = Frame(root)
result_text_frame.pack(pady=10)

result_text = Text(result_text_frame, wrap=tk.WORD, height=10, width=60)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_scroll = Scrollbar(result_text_frame, orient=tk.VERTICAL, command=result_text.yview)
result_scroll.pack(side=tk.RIGHT, fill=tk.Y)

result_text.config(yscrollcommand=result_scroll.set, state=tk.DISABLED)

# Watermark
watermark_label = Label(root, text="Rwky00978", bg='#303030', fg='gray')
watermark_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()
