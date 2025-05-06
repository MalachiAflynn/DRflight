from ursina import *

class DroneController:
    def __init__(self, drone):
        self.drone = drone
        self.sensitivity = 2.0
        self.thrust_sensitivity = 4.0
        
    def update(self):
        # Get keyboard input
        thrust = 0
        pitch = 0
        roll = 0
        yaw = 0
        
        # Thrust control (Q for up, E for down)
        if held_keys['q']:
            thrust += self.thrust_sensitivity
        if held_keys['e']:
            thrust -= self.thrust_sensitivity
            
        # Movement control (WASD)
        if held_keys['w']:
            pitch += self.sensitivity
        if held_keys['s']:
            pitch -= self.sensitivity
        if held_keys['a']:
            roll -= self.sensitivity
        if held_keys['d']:
            roll += self.sensitivity
            
        # Yaw control (Q and E when holding shift)
        if held_keys['shift']:
            if held_keys['q']:
                yaw += self.sensitivity
            if held_keys['e']:
                yaw -= self.sensitivity
                
        # Apply controls to drone
        self.drone.apply_control(thrust, pitch, roll, yaw) 