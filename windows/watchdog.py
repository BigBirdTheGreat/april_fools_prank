# -*- coding: utf-8 -*-

import sys, time, subprocess, os, psutil

path = os.getcwd()

firsttime = True

text_path = os.path.join(path, 'variable.txt')
hydra_path = os.path.join(path, 'hydra.py')

def check_taskmgr():
    for p in psutil.process_iter(['name']):
        if 'taskmgr' in p.info['name'].lower():
            subprocess.Popen(["python", hydra_path])

def find_or_start_process(process_name):
    global firsttime

    process = None

    if firsttime == True:
        for p in psutil.process_iter(['name']):
            if p.info['name'] == process_name:
                process = psutil.Process(p.pid)
                break
    
    if process is None:
        process = subprocess.Popen(["python", hydra_path])
    
    firsttime = False
    return process

process_name = "python.exe"
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
    check_taskmgr()
        
    with open(text_path, "r") as f:
        data = int(f.read())
        f.close()
    if data == 1:
        sys.exit()
    time.sleep(0.2)
    
sys.exit()