import psutil
import os
import signal
PROCNAME = "pyilper"
PROCNAME = "python"

for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        print (proc.pid)
        os.kill(proc.pid,signal.SIGQUIT)
