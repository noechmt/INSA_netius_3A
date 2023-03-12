from time import sleep
import os
from Map import *

myMap = Map(5)
myMap.init_path()
#myMap.display()
# myMap.array[1][1] = House(1, 1, myMap)

#myMap.array[2][2] = Fountain(2, 2, myMap)
myMap.array[3][2].build("path")
myMap.array[2][2].build("path")
myMap.array[2][3].build("path")
myMap.array[2][4].build("path")
myMap.array[3][4].build("path")
myMap.array[3][0].build("house")
myMap.array[2][1].build("well")
#myMap.array[0][0] = Empty(0, 0, myMap, "water")
#myMap.array[1][0] = House(1, 0, myMap)
print(myMap)

for i in range(7):
   os.system("clear")
   myMap.update()
   print(myMap)
   print(myMap.walkers)
   sleep(1)

myMap.array[3][3].build("prefecture")
print("Build prefecture on cell 3,3")

while True:
   os.system("clear")
   myMap.update()
   print(myMap)
   print(myMap.walkers)
   sleep(1)
   
# myMap.array[3][0].prefect.leave_building()
# for i in range(15):
#     myMap.array[3][0].prefect.prefect_move()
#print(myMap.array[1][1].type_of_building)
#myMigrant = Migrant(myMap.array[3][0])



#TODO 
# risks
#house levels
#animation des walkers 
#archeduc 

