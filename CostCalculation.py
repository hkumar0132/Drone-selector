import math
import Location
import Drone

class cost_calculation:
    
    def __init(self, work_done_cost, cost):
        self.work_done_cost = work_done_cost
        self.cost = cost
    
    #obj is the drone object
    def workDone(self, obj, source_name, dest_name, supplies, order_dist, order_mass, weather):
        self.work_done_cost = 0
        
        """calculating work_done_cost
        based on geographical location
        and weather conditions"""
        
        #Number 1 -> Height difference
        
        l = Location.location(0, 0)        
        d = Drone.drone(0, 0, 1, 0, 0, 0, 0, 0, 0, (0, 0, 0, 0))        
        
        source = l.getLatLong(source_name)
        dest = l.getLatLong(dest_name)
        
        lat1 = math.radians(source[0])
        lat2 = math.radians(dest[0])

        diffLong = math.radians(dest[1] - source[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        initial_bearing = math.degrees(initial_bearing)
        
        #This is the angle that
        #source makes wrt destination
        
        compass_bearing = (initial_bearing + 360) % 360
        
        #Using the formula
        #tanA = height/base
        #so, height = tanA * base
        
        self.height = d.getDistance(source_name, l.getLatLong(dest_name)) * math.tan(compass_bearing)
        
        #If difference between source and
        #destination altitude is >=
        #70, then we add additional cost
        #Assuming the additional cost
        #per unit of height to be 0.5
        #Replaceable value
        
        if self.height >= 50:
            self.work_done_cost = self.height*0.5
            
            
        
        #Number 2 -> weather conditions
        
        self.wind_speed = weather['Wind_speed']
        self.clouds = weather['Clouds']
        
        #Assuming 0.5 unit of extra work done
        #for every unit of wind speed, if wind
        #speed >=8 as it will resist the drone
        #Replaceable value
        
        if self.wind_speed >= 8:
            self.work_done_cost = self.wind_speed*0.5
        
        #Assuming 0.5 unit of extra work done
        #for per unit of clouds, if >= 5
        #as it will cause visibility issue        
        #Replaceable value
        
        if self.clouds >= 5:
            self.work_done_cost = self.clouds*0.5
            
        #Assuming 1 unit of battery expenditure 
        #per unit of distance
        #Replaceable value
        
        obj.battery = order_dist*1
        self.cost = self.costCalculation(self.work_done_cost, obj.battery)
    
        return self.cost
    
    #This function calculates the
    #final cost incurred
    def costCalculation(self, work_done_cost, battery, per_unit_battery_cost=0.5, maintenance_cost=1):
        
        #The per unit battery cost and
        #maintenance cost can be replaced 
        #by the original value
        
        return battery*per_unit_battery_cost + maintenance_cost + work_done_cost      

#For testing the functions

"""        
c = cost_calculation()
print("costCalculation() : " + str(c.costCalculation(0, 0)))

"""
