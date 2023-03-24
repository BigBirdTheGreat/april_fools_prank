# -*- coding: utf-8 -*-

import sys, time, subprocess, os, psutil

#sets up some variables
nameoffile = "hydra.app"
base_dir = os.path.dirname(os.path.abspath(sys.argv[0])).split('/')
base_dir.pop(0)
path = "/"
firsttime = True

#finds directory of the file
for i in range(len(base_dir)):
    if base_dir[i] == nameoffile:
        break
    else:
        path = os.path.join(path, base_dir[i])

#makes the text paths
text_path = os.path.join(path, 'variable.txt')
hydra_path = os.path.join(path, 'hydra.app', 'Contents', 'MacOS', 'hydra')


def find_or_start_process(process_name):
    global firsttime
    
    process = None

    if firsttime == True:
        for p in psutil.process_iter(['name']):
            if p.info['name'] == process_name:
                process = psutil.Process(p.pid)
                break
    
    if process is None:
        process = subprocess.Popen([hydra_path])
    
    firsttime = False
    return process

process_name = "hydra"
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
    