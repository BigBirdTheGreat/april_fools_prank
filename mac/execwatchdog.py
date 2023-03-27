# -*- coding: utf-8 -*-

import sys, time, subprocess, os, psutil

#sets up some variables
nameoffile = "exechydra"
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
firsttime = True

hydra_path = os.path.join(base_dir, nameoffile) 
text_path = os.path.join(base_dir, 'variable.txt')


def find_or_start_process(process_name):
    global firsttime
    
    process = None

    if firsttime == True:
        for p in psutil.process_iter(['name']):
            if p.info['name'] == process_name:
                process = psutil.Process(p.pid)
                break
    
    if process is None:
        process = subprocess.Popen([hydra_path], stdin=subprocess.DEVNULL, preexec_fn=os.setsid)
    
    firsttime = False
    return process

process_name = "exechydra"
process = find_or_start_process(process_name)

while True:
    
    if isinstance(process, subprocess.Popen):
        if process.poll() is not None:
            process = find_or_start_process(process_name)
    elif isinstance(process, psutil.Process):
        if process.is_running():
            pass
        else:
            process = find_or_start_process(process_name)
        
    with open(text_path, "r") as f:
        data = int(f.read())
        f.close()
    if data == 1:
        sys.exit()
    time.sleep(0.2)
    