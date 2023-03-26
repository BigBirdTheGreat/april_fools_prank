# -*- coding: utf-8 -*-

#importing things for hydra
from tkinter import ttk
import threading
import sys, time, random as rm, subprocess, tkinter as tk, os, psutil
root = tk.Tk()
root.withdraw()

hashed = "PleaseStopIt" # password
windows = [] #list of windows
entries = [] #list of password entries

#importing things to make sure watchdog lives
nameoffile = "watchdog.app" #name of resurrecting file
nameofotherfile = "hydra.app"
base_dir = os.path.dirname(os.path.abspath(sys.argv[0])).split('/') 
base_dir.pop(0)
path = "/"
firsttime = True

stop_event = threading.Event() # creates event to help stop threads at same time

#gets the directory allowing mayhem to begin
for i in range(len(base_dir)):
    if base_dir[i] == nameoffile or base_dir[i] == nameofotherfile:
        break
    else:
        path = os.path.join(path, base_dir[i])
    
#making the paths so it can run watchdog and check out the text path
dog_path = os.path.join(path, 'watchdog.app', 'Contents', 'MacOS', 'watchdog') # CHANGE WHEN BUNDLING
text_path = os.path.join(path, 'variable.txt')

#function that runs Hydra itself
def hydrafunc():
    
    #Function checks if the player wants to remove the "virus" and if so looks through all passwords
    def remove_virus():
        global entries
        
        #looks through each password entry to find right password
        for entry in entries:
            result = entry.get()
            if result == hashed:
                with open(text_path, "w") as k:
                    k.write("1") # tells watched to eliminate itself
                    k.close()
                stop_event.set() # sets stop event
                sys.exit() # kills program
                
        result_label.config(text="Incorrect password. Try again.") # if all passwords don't work it sets incorrect password label
        spawner()
    
    #function responsible for spawning new windows
    def spawner():
        
        #figures out how many it should make and saves it in case Hydra was removed with task manger
        with open(text_path, "r") as f:
            data = f.read()
            for i in range(int(data)):
                 
                create_window()
                time.sleep(float("0.0" + str(rm.randint(5, 10)))) # randomizes it to add some spice
                
            f.close()

    #where the magic happens, actually makes the window
    def create_window():    
        global root, remove_virus_entry, result_label
        
        #increases the spawning var by one
        with open(text_path, "r") as f:
            data = f.read()
            data = int(data) + 1
            with open(text_path, "w") as k:
                k.write(str(data))
        
        f.close() 
        k.close() 

        #text in window
        Line1 = "Lol you actually fell for it."    
        Line2 = "This is Hydra. Chop one head off, and it grows more." 
        Line3 = "To kill it put in the password."
        Line4 = "The easy way to get it is to ask me, the hard way is to find it from the source code."
        Line5 = "Good luck!"
        
        x = tk.Toplevel(root) # spawns in window
        
        #puts in text in window
        ttk.Label(x, text=Line1, anchor="center").pack(pady=(5, 5))
        ttk.Label(x, text=Line2, anchor="center").pack(pady=(0, 5))
        ttk.Label(x, text=Line3, anchor="center").pack(pady=(0, 0))
        ttk.Label(x, text=Line4, anchor="center").pack(pady=(0, 0))
        ttk.Label(x, text=Line5, anchor="center").pack(pady=(10, 0))
        
        #creates place to enter password and puts it in a list
        remove_virus_entry = ttk.Entry(x)
        entries.append(remove_virus_entry)
        remove_virus_entry.pack(pady=(20,0))
        
        #button to remove virus
        ttk.Button(x, text="Remove Virus", command=remove_virus).pack(pady=(5, 0))
        x.title("April Fools Day Virus")
        
        #results label
        result_label = ttk.Label(x)
        result_label.pack()

        #sets screen parameters 
        screen_width = x.winfo_screenwidth()
        screen_height = x.winfo_screenheight()

        #more magic, sets parameters which tell window to make noise, not close, etc.
        x.geometry('600x225-' + str(rm.randint(0, screen_width-600)) + "+" + str(rm.randint(0, screen_height-175)))
        x.resizable(False, False)
        x.attributes("-topmost", True)
        x.attributes("-alpha", 1)
        x.protocol("WM_DELETE_WINDOW", lambda: spawner())
        x.protocol("WM_CLOSE", lambda: spawner())
        x.deiconify()
        x.bell()

    #originally opens the variable file and makes windows accordingly
    with open(text_path, "r") as f:
        data = f.read()
        f.close()
        if int(data) > 2:
            spawner()
        else:
            create_window()

#function that makes sure watchdog is alive
def watchthedog():    
    
    #main function, checks to see if watchdog is alive and if not respawns it
    def find_or_start_process(process_name):
        global firsttime
        process = None
        
        #only runs on the first time the program is created to make it more efficient
        if firsttime:
            for p in psutil.process_iter(['name']):  #loops through list of all processes to find it
                if p.info['name'] == process_name:
                    process = psutil.Process(p.pid)
                    break

        #if there is no process it makes a new iteration
        if process is None:
            process = subprocess.Popen([dog_path])
            
        firsttime = False  #sets firstime to false
        
        return process

    process_name = "watchdog"
    process = find_or_start_process(process_name)

    #ensures loop stops once the stop_event is set
    while not stop_event.is_set():
        
        if isinstance(process, subprocess.Popen):
            if process.poll() is not None:
                process = find_or_start_process(process_name) #restarts it
                
        elif isinstance(process, psutil.Process):
            if process.is_running():
                pass
            else:
                process = find_or_start_process(process_name) #restarts it
        
        time.sleep(0.2) #saves some resources
        
#creates and starts threads
Hydra = threading.Thread(target=hydrafunc)
Watchdog = threading.Thread(target=watchthedog)
Hydra.start()
Watchdog.start()

#some things to cleanly end the program 
while not stop_event.is_set():
    root.mainloop()

root.destroy()
Watchdog.join()
Hydra.join()

sys.exit()