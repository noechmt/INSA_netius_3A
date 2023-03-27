class Wrapper:
   
   def __init__(self, map):
      self.map = map

   def wrap(data):
      header, user, array = data.split(";")
      match header:
         case 'build':
            map.getCell(array[0], array[1]).build(array[3], user)
         case 'walker':
            pass