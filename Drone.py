import Location
import math

class drone:
    
    def __init__(self, drone_id, status, battery, capacity, remain_capacity, current_location, trav_dist, point_dist, work_done, weather):
        self.drone_id = drone_id
        self.status = status
        self.battery = battery
        self.capacity = capacity
        self.remain_capacity = remain_capacity
        self.current_location = current_location
        self.trav_dist = trav_dist
        self.point_dist = point_dist
        self.work_done = work_done
        self.weather = weather
  
    #This function calculates difference between 
    #2 points using their latitude and longitude
    
    def getDistance(self, curr_loc='Dehradun', pick_up_point=(0, 0)):
        l = Location.location(0, 0)
        
        #'Dehradun' shall be replaced by the original
        #value sent by the Drone GPS
        
        self.current_location = l.getLatLong(curr_loc)
        
        #Radius of earth
        
        R = 6373.0 
        
        lat1 = math.radians(self.current_location[0])
        long1 = math.radians(self.current_location[0])
        
        lat2 = math.radians(pick_up_point[0])
        long2 = math.radians(pick_up_point[0])
        
        dlong = abs(long2 - long1)
        dlat = abs(lat2 - lat1)
                
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        self.point_dist = R*c
        
        return self.point_dist
        
    def getOrder(self, velocity=10, force=1): #Assuming the velocity at which drones fly to be 10
        
        #force = power/velocity
        
        self.force = self.battery/velocity 
        
        #distance = work_done/force
        
        self.trav_dist = self.work_done/self.force
        
        return self.trav_dist
    
    def Capacity(self, current_weight):
        self.remain_capacity = self.capacity - current_weight
        if self.remain_capacity < 0:
            return -1
        return self.remain_capacity
    
    def operation(self):
        pass    
    

#For testing the functions
        
"""
d = drone(0, 0, 1, 0, 0, 0, 0, 0, 0, (0, 0, 0, 0))
print("getDistance() : " + str(d.getDistance((0, 0))))
print("getOrder() : " + str(d.getOrder()))
print("Capacity() : " + str(d.Capacity(0)))

"""
