def send_data(data):
   print(data)

def build(username, coordinates, type):
   send_data("build;"
             +username+";"
             +str(coordinates)+";"
             +type)

class WalkerBuffer:

   buffer = "walker;"
   username = ""

   def add(self, action, coordinates, type):
      self.buffer = (self.buffer+"next;"
             +self.username+";"
             +action+";"
             +str(coordinates[0])+";"+str(coordinates[1])+";"
             +str(type))
   
   def send(self):
      send_data(self.buffer)
      self.buffer = "walker;"
