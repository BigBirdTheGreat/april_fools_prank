# -*- coding: utf-8 -*-

from tkinter import ttk
import threading
import sys, time, random as rm, subprocess, tkinter as tk, os, psutil
root = tk.Tk()
root.withdraw()
hashed = "ShreyPleaseStop"
windows = []
entries = []

firsttime = True

stop_event = threading.Event()

path = os.getcwd()
    
print(str(path))
dog_path = os.path.join(path, 'watchdog.exe') # CHANGE WHEN BUNDLING
print(str(dog_path))
text_path = os.path.join(path, 'variable.txt')

with open(text_path, "w") as f:
    f.write("1")

def hydrafunc():
    def remove_virus():
        global entries
        for entry in entries:
            result = entry.get()
            if result == hashed:
                with open(text_path, "w") as k:
                    k.write("1")
                    stop_event.set()
                    print("time to die")
                    sys.exit()
                k.close()
        result_label.config(text="Incorrect password. Try again.") 
        spawner()
    
    def spawner():
        with open(text_path, "r") as f:
            data = f.read()
            for i in range(int(data)):
                create_window()
                time.sleep(float("0.0" + str(rm.randint(5, 10))))
                
            f.close()

    def create_window():    
        global root, remove_virus_entry, result_label
        
        with open(text_path, "r") as f:
            data = f.read()
            data = int(data) + 1
            with open(text_path, "w") as k:
                k.write(str(data))
        
        f.close() 
        k.close() 

        Line1 = "Lol you actually fell for it."    
        Line2 = "This is Hydra. Chop one head off, and it grows more." 
        Line3 = "To kill it put in the password."
        Line4 = "The easy way to get it is to ask me, the hard way is to find it from the source code."
        Line5 = "Good luck!"
        x = tk.Toplevel(root)
        
        ttk.Label(x, text=Line1, anchor="center").pack(pady=(5, 5))
        ttk.Label(x, text=Line2, anchor="center").pack(pady=(0, 5))
        ttk.Label(x, text=Line3, anchor="center").pack(pady=(0, 0))
        ttk.Label(x, text=Line4, anchor="center").pack(pady=(0, 0))
        ttk.Label(x, text=Line5, anchor="center").pack(pady=(10, 0))
        remove_virus_entry = ttk.Entry(x)
        entries.append(remove_virus_entry)
        remove_virus_entry.pack(pady=(20,0))
        
        ttk.Button(x, text="Remove Virus", command=remove_virus).pack(pady=(5, 0))
        x.title("April Fools Day Virus")
        
        result_label = ttk.Label(x)
        result_label.pack()

        screen_width = x.winfo_screenwidth()
        screen_height = x.winfo_screenheight()

        x.geometry('600x225-' + str(rm.randint(0, screen_width-600)) + "+" + str(rm.randint(0, screen_height-175)))
        x.resizable(False, False)
        x.attributes("-topmost", True)
        x.attributes("-alpha", 1)
        x.protocol("WM_DELETE_WINDOW", lambda: spawner())
        x.protocol("WM_CLOSE", lambda: spawner())
        x.deiconify()
        x.bell()

    with open(text_path, "r") as f:
        data = f.read()
        f.close()
        if int(data) > 2:
            spawner()
        else:
            create_window()

def watchthedog():    
    def find_or_start_process(process_name):
        global firsttime
        process = None
        
        if firsttime:
            for p in psutil.process_iter(['name']):
                if p.info['name'] == process_name:
                    process = psutil.Process(p.pid)
                    break


        if process is None:
            process = subprocess.Popen(["python", dog_path])
            
        firsttime = False    
        
        return process

    process_name = "watchdog"
    process = find_or_start_process(process_name)

    while not stop_event.is_set():
        
        if isinstance(process, subprocess.Popen):
            if process.poll() is not None:
                process = find_or_start_process(process_name)
        elif isinstance(process, psutil.Process):
            if process.is_running():
                pass
            else:
                process = find_or_start_process(process_name)
        
        time.sleep(0.2)
        

Hydra = threading.Thread(target=hydrafunc)
Watchdog = threading.Thread(target=watchthedog)
Hydra.start()
Watchdog.start()

while not stop_event.is_set():
    print()
    root.mainloop()

root.destroy()
Watchdog.join()
Hydra.join()

sys.exit()

