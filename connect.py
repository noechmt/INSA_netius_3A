import Class.Encoder as encode
import threading as thread
<<<<<<< HEAD:connect.py
from p2p.socket_python import *
import subprocess
import os
=======
from socket_python import *

>>>>>>> endpoint:p2p/connect.py
def socket_init():
   Server(1235,4)
   
   thread_recv = thread.Thread(target=recv_data, args=(Server.socket,))
   thread_send = thread.Thread(target=send_data, args=("dataDePython",))
   thread_recv.start()
<<<<<<< HEAD:connect.py
   #thread_send.start()



os.system("make clean -C p2p")
os.system("make -C p2p")
LanProcess = subprocess.Popen(['./p2p/lan_connect',"192.168.7.31"])
send_data("Coucou2")
sleep(10)
encode.quit("Governor")
sleep(1)
LanProcess.kill()
=======
   thread_send.start()

Server(1235, 4)
send_data("coucou")
>>>>>>> endpoint:p2p/connect.py
