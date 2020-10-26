import Location
import CostCalculation
import math
import json
import Drone

class hub:
    
    def __init__(self, name, no_of_present_drone, source_name, dest_name, supplies, supplies_status, order_dist, order_mass, weather):
        self.name = name
        self.no_of_present_drone = no_of_present_drone
        self.source_name = source_name
        self.dest_name = dest_name
        self.supplies = supplies
        self.supplies_status = supplies_status
        self.order_dist = order_dist
        self.order_mass = order_mass
        self.weather = weather
        
    def reinitialize(self):
        
        #supplies available
        
        #This can be stored in a database
        #where values can be updated
        self.supplies = {
                "RBC" : 10,
                "WBC" : 5,
                "Blood plasma" : 9,
                "Platelets" : 8,
                "Anti venom" : 7 
                }
        
        #These are the list of drones
        #available with default values
        
        #This can be stored in a database
        #where values can be changed
        #depending on the data sent
        #by the drone
        
        self.d1 = Drone.drone('1', 0, 50.0, 15.0, 15.0, '', 5.0, 0.0, 150.0, '')
        self.d2 = Drone.drone('2', 0, 600.0, 13.0, 3.0, '', 60.0, 0.0, 100.0, '')
        self.d3 = Drone.drone('3', 1, 300.0, 15.0, 8.0, '', 30.0, 5.0, 150.0, '')
        self.d4 = Drone.drone('4', 1, 50.0, 13.0, 7.0, '', 5.0, 10.0, 100.0, '')
        self.d5 = Drone.drone('5', 1, 1000.0, 14.0, 0.0, '', 100.0, 0.1, 150.0, '')    
        self.drones = [self.d1, self.d2, self.d3, self.d4, self.d5]
        self.selected = None

        
    def getDistance(self):
        l = Location.location(0, 0)
        
        #Radius of earth
        
        R = 6373.0
        
        #gets latitude and longitude of the destination
        
        dest_location = l.getLatLong(self.dest_name) 
        
        #gets latitude and longitude of the source
        
        source_location = l.getLatLong(self.source_name)
        
        lat1 = math.radians(dest_location[0])
        long1 = math.radians(dest_location[1])
        
        lat2 = math.radians(source_location[0])
        long2 = math.radians(source_location[1])
        
        dlong = abs(long2 - long1)
        dlat = abs(lat2 - lat1)
                
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        self.Order_dist = R*c
        
        return self.Order_dist
        
    #Calling all the functions
    def getOrder(self):
        
        self.reinitialize()
        
        #pick up point , drop point , list of supplies , estimated time
        return ("\n\nSelected drone id : " + str(self.efficientDrone()) + 
                "\n\nPick up point : " + str(self.source_name) +
                "\n\nDrop point : " + str(self.dest_name) + 
                "\n\nList of supplies : " + json.dumps(self.supplies) + 
                #Assuming velocity of drone to be 10
                "\n\nEstimated time : " + str(self.getDistance()/10.0) +
                "\n\nPresent at station : " + str(True if self.suppliesStatus() else False) +
                "\n\nOrder weight : " + str(self.getMass()) + 
                "\n\nWeather condition : " + str(self.weather) + 
                "\n\nFinal cost : " + str(self.setDelivery()))
    
    def efficientDrone(self):
        
        self.reinitialize()
        
        #removing item from the list which 
        #do not satisfy the given conditions
        
        for i in self.drones:
            if not(i.trav_dist > self.getDistance() and i.remain_capacity > self.order_mass):
                self.drones.remove(i)
                
        if len(self.drones) == 0:
            return "No available drones"
        
        #if only one drone satisfying 
        #the above condition
        
        if len(self.drones) == 1:
            return self.drones[0].drone_id
        
        #choosing the drone with 
        #smallest point distance
        
        for i in range(0, len(self.drones)-1):
            if self.drones[i].point_dist < self.drones[i+1].point_dist:
                self.selected = self.drones[i]
            else:
                self.selected = self.drones[i+1]
    
        #returning id of the selected drone                
        
        return self.selected.drone_id
    
    def setDelivery(self):
        
        #calling efficientDrone function
        #to get the object of the 
        #selected drone
        
        self.t = self.efficientDrone()
        if(self.t == "No available drones"):
            return -1
        
        self.c = CostCalculation.cost_calculation()
        
        self.cost = self.c.workDone(self.selected, self.source_name, self.dest_name, self.supplies, self.order_dist, self.order_mass, self.weather)
        
        return self.cost
    
    def getMass(self):
        
        #assuming 1 unit of mass per 
        #supply
        
        self.order_mass = 0
        for i in self.supplies.values():
            self.order_mass += i*1
        
        return self.order_mass
    
    def suppliesStatus(self):
        
        #calling this function to select the 
        #efficient drone to know its status
        
        self.t = self.efficientDrone()
        if(self.t == "No available drones") : 
            return -1
        self.supplies_status = self.selected.status
        return self.supplies_status
    

#These location values can be
#replaced by the original values
#sent by the drone GPS 
        
l = Location.location(0, 0)
h = hub("A", 5, "Raiwala", "Dehradun", {} , 0, 0, 0, l.getWeatherCond())
print("Details : " + str(h.getOrder()))
