USERNAME = ""

def set_username(username):
   USERNAME = username

def send_data(data):
   pass

def build(coordinates, type):
   send_data("build;"
             +USERNAME+";"
             +str(coordinates.x)+";"+str(coordinates).y+";"
             +type)

def walker(action, coordinates, type):
   send_data("walker;"+action+";"
             +USERNAME+";"
             +str(coordinates.x)+";"+str(coordinates.y)+";"
             +str(type))
