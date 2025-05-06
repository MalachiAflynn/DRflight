from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from drone import Drone
from environment import Environment
from controls import DroneController
import random

class DroneSimulator(Entity):
    def __init__(self):
        super().__init__()
        
        # Set up the window
        window.title = 'Drone Simulator'
        window.borderless = False
        window.exit_button.visible = False
        window.fps_counter.enabled = True
        
        # Create the environment
        self.environment = Environment()
        
        # Create the drone
        self.drone = Drone()
        
        # Create the controller
        self.controller = DroneController(self.drone)
        
        # Set up the camera
        camera.position = self.drone.position + Vec3(0, 5, -10)  # Position camera relative to drone's new height
        camera.look_at(self.drone)
        
        # Add UI elements
        self.setup_ui()
        
    def setup_ui(self):
        # Create UI elements for drone information
        self.altitude_text = Text(text='Altitude: 0m', position=(-0.85, 0.45))
        self.velocity_text = Text(text='Velocity: 0 m/s', position=(-0.85, 0.4))
        self.battery_text = Text(text='Battery: 100%', position=(-0.85, 0.35))
        self.gps_text = Text(text='GPS: 0, 0, 0', position=(-0.85, 0.3))
        self.health_text = Text(text='Health: 100%', position=(-0.85, 0.25))
        self.status_text = Text(text='Status: Flying', position=(-0.85, 0.2))
        self.reset_text = Text(text='Press SPACE to reset', position=(-0.85, 0.15))
        
    def update(self):
        # Check for reset
        if held_keys['space']:
            self.drone.reset()
            
        # Update drone information display
        self.altitude_text.text = f'Altitude: {self.drone.position.y:.1f}m'
        self.velocity_text.text = f'Velocity: {self.drone.velocity.length():.1f} m/s'
        self.battery_text.text = f'Battery: {self.drone.battery_level:.0f}%'
        self.gps_text.text = f'GPS: {self.drone.position.x:.1f}, {self.drone.position.y:.1f}, {self.drone.position.z:.1f}'
        self.health_text.text = f'Health: {self.drone.health:.0f}%'
        self.status_text.text = f'Status: {"Crashed" if self.drone.is_crashed else "Flying"}'
        
        # Update camera to follow drone
        camera.position = self.drone.position + Vec3(0, 5, -10)
        camera.look_at(self.drone)
        
        # Update controller
        self.controller.update()

if __name__ == '__main__':
    app = Ursina()
    simulator = DroneSimulator()
    app.run() 