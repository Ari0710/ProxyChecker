import tkinter as tk
from tkinter import messagebox
import threading
import requests
import pyperclip
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

# Function to check if a proxy is working using 1.1.1.1
def is_proxy_working(proxy, test_url="https://1.1.1.1", timeout=5):
    proxies_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        response = requests.get(test_url, proxies=proxies_dict, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Worker function to process proxies
def process_proxies(proxies, queue, progress_queue, working_count_queue):
    total = len(proxies)
    completed = 0
    working_count = 0

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(is_proxy_working, proxy): proxy for proxy in proxies}
        for future in futures:
            proxy = futures[future]
            try:
                if future.result():
                    working_count += 1
                    queue.put(proxy)
                    working_count_queue.put(working_count)
            except Exception:
                pass
            completed += 1
            progress_queue.put((completed, total))
    queue.put(None)
    progress_queue.put(None)
    working_count_queue.put(None)

# Function to update the GUI with results
def update_results(queue):
    while True:
        proxy = queue.get()
        if proxy is None:
            check_button.config(state=tk.NORMAL)
            copy_button.config(state=tk.NORMAL)
            return
        results.insert("end", f"{proxy}\n")

# Function to update the progress bar
def update_progress(progress_queue):
    while True:
        progress = progress_queue.get()
        if progress is None:
            progress_label.config(text="100% Done")
            return
        completed, total = progress
        percent = int((completed / total) * 100)
        progress_label.config(text=f"{percent}% Done")
        total_label.config(text=f"Total Proxies: {total}")

# Function to update the working proxy count
def update_working_count(working_count_queue):
    while True:
        working_count = working_count_queue.get()
        if working_count is None:
            return
        working_label.config(text=f"Working Proxies: {working_count}")

# Function to handle proxy checking
def check_proxies():
    proxies_text = proxies_input.get("1.0", "end-1c").strip()
    if not proxies_text:
        messagebox.showwarning("Input Error", "Please enter some proxies first.")
        return

    proxies = proxies_text.splitlines()
    results.delete(1.0, "end")
    progress_label.config(text="0% Done")
    total_label.config(text=f"Total Proxies: {len(proxies)}")
    working_label.config(text="Working Proxies: 0")

    check_button.config(state=tk.DISABLED)
    copy_button.config(state=tk.DISABLED)

    queue = Queue()
    progress_queue = Queue()
    working_count_queue = Queue()

    threading.Thread(target=process_proxies, args=(proxies, queue, progress_queue, working_count_queue), daemon=True).start()
    threading.Thread(target=update_results, args=(queue,), daemon=True).start()
    threading.Thread(target=update_progress, args=(progress_queue,), daemon=True).start()
    threading.Thread(target=update_working_count, args=(working_count_queue,), daemon=True).start()

# Function to copy working proxies to clipboard
def copy_working_proxies():
    working_proxies = results.get("1.0", "end-1c").strip()
    if working_proxies:
        pyperclip.copy(working_proxies)
        messagebox.showinfo("Copied", "Working proxies have been copied to clipboard.")
    else:
        messagebox.showwarning("No Proxies", "No working proxies to copy.")

# Create the main application window
root = tk.Tk()
root.title("Proxy Checker")
root.geometry("600x500")

# Create a frame for side-by-side layout
main_frame = tk.Frame(root)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Left Frame: Proxies
left_frame = tk.Frame(main_frame)
left_frame.pack(side="left", padx=10, expand=True)

proxies_input_label = tk.Label(left_frame, text="Proxies:")
proxies_input_label.pack(anchor="w", pady=5)

proxies_input = tk.Text(left_frame, height=15, width=30)
proxies_input.pack()

check_button = tk.Button(left_frame, text="Check Proxies", command=check_proxies)
check_button.pack(pady=5)

# Right Frame: Working Proxies
right_frame = tk.Frame(main_frame)
right_frame.pack(side="right", padx=10, expand=True)

results_label = tk.Label(right_frame, text="Working Proxies:")
results_label.pack(anchor="w", pady=5)

results = tk.Text(right_frame, height=15, width=30)
results.pack()

copy_button = tk.Button(right_frame, text="Copy Working Proxies", command=copy_working_proxies)
copy_button.pack(pady=5)

# Progress and Status Labels
progress_label = tk.Label(root, text="0% Done", font=("Arial", 12))
progress_label.pack(pady=5)

total_label = tk.Label(root, text="Total Proxies: 0", font=("Arial", 10))
total_label.pack(pady=2)

working_label = tk.Label(root, text="Working Proxies: 0", font=("Arial", 10))
working_label.pack(pady=2)

# Run the Tkinter event loop
root.mainloop()
