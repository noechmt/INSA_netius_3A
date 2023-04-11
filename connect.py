import Class.Encoder as encode
import threading as thread
from p2p.socket_python import *
import subprocess
import os
def socket_init():
   Server(1235,4)
   
   thread_recv = thread.Thread(target=recv_data, args=(Server.socket,))
   #thread_send = thread.Thread(target=send_data, args=("dataDePython",))
   thread_recv.start()
   #thread_send.start()



os.system("make clean -C p2p")
os.system("make -C p2p")
LanProcess = subprocess.Popen(['./p2p/lan_connect',"192.168.7.31"])
sleep(1)
encode.quit("Governor")
sleep(1)
LanProcess.kill()