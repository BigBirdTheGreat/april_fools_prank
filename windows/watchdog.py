# -*- coding: utf-8 -*-

import sys, time, subprocess, os, psutil

path = os.getcwd()

firsttime = True

text_path = os.path.join(path, 'variable.txt')
hydra_path = os.path.join(path, 'hydra.exe')

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

process_name = "hydra.exe"
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
        try:
            data = int(f.read())
        except ValueError:
            data = 2
        f.close()
    if data == 1:
        sys.exit()
    time.sleep(0.2)
    
sys.exit()