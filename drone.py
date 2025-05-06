from ursina import *
import math

class Drone(Entity):
    def __init__(self):
        super().__init__()
        
        # Create basic drone texture
        # This creates a simple colored texture programmatically
        from PIL import Image
        import numpy as np
        
        # Create a 64x64 texture
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        pixels = img.load()
        
        # Draw a simple drone shape
        for x in range(size):
            for y in range(size):
                # Create a cross pattern
                if (x < size//4 or x > 3*size//4) and (y < size//4 or y > 3*size//4):
                    pixels[x, y] = (200, 200, 200, 255)  # Light gray for arms
                elif size//4 <= x <= 3*size//4 and size//4 <= y <= 3*size//4:
                    pixels[x, y] = (255, 0, 0, 255)  # Red for body
                else:
                    pixels[x, y] = (0, 0, 0, 0)  # Transparent
        
        # Save the texture
        img.save('drone_texture.png')
        
        # Visual representation
        self.model = 'cube'
        self.color = color.red
        self.scale = (1, 0.2, 1)
        self.texture = 'drone_texture.png'
        
        # Initial position
        self.initial_position = Vec3(0, 50, 0)  # Increased starting height to 50 units
        self.position = self.initial_position
        
        # Physics properties
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        self.rotation_velocity = Vec3(0, 0, 0)
        
        # Drone properties
        self.mass = 1.0  # kg
        self.max_thrust = 25.0  # Reduced thrust for more gentle lift
        self.battery_level = 100.0  # %
        self.battery_drain_rate = 0.1  # % per second
        self.health = 100.0  # Drone health
        self.is_crashed = False
        
        # Control inputs
        self.thrust = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        
        # Constants
        self.gravity = 4.0  # Reduced gravity for more floaty movement
        self.drag_coefficient = 0.03  # Reduced drag for smoother movement
        self.angular_damping = 0.98  # Increased damping
        self.collision_damage = 10.0  # Damage per collision
        self.collision_cooldown = 1.0  # Seconds between collision damage
        self.last_collision_time = 0
        
        # Add collision box
        self.collider = BoxCollider(self, size=(1, 0.2, 1))
        
    def reset(self):
        # Reset position
        self.position = self.initial_position
        
        # Reset physics
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        self.rotation_velocity = Vec3(0, 0, 0)
        self.rotation = Vec3(0, 0, 0)
        
        # Reset properties
        self.battery_level = 100.0
        self.health = 100.0
        self.is_crashed = False
        self.color = color.red
        
        # Reset controls
        self.thrust = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        self.yaw = 0.0
        
    def update(self):
        if self.is_crashed:
            return
            
        # Calculate forces
        thrust_force = Vec3(0, self.thrust * self.max_thrust, 0)
        gravity_force = Vec3(0, -self.gravity * self.mass, 0)
        drag_force = -self.velocity * self.drag_coefficient
        
        # Calculate acceleration
        self.acceleration = (thrust_force + gravity_force + drag_force) / self.mass
        
        # Update velocity with increased responsiveness
        self.velocity += self.acceleration * time.dt * 1.5  # Reduced multiplier for smoother movement
        
        # Add horizontal movement based on pitch and roll
        forward_force = Vec3(0, 0, self.pitch * 7)  # Reduced force for gentler movement
        right_force = Vec3(self.roll * 7, 0, 0)  # Reduced force for gentler movement
        
        # Apply forces in the direction the drone is facing
        self.velocity += self.rotation * (forward_force + right_force) * time.dt
        
        # Update position
        self.position += self.velocity * time.dt
        
        # Update rotation
        self.rotation_velocity *= self.angular_damping
        self.rotation += self.rotation_velocity * time.dt
        
        # Update battery
        self.battery_level -= self.battery_drain_rate * time.dt
        self.battery_level = max(0, self.battery_level)
        
        # Check for collisions
        self.check_collisions()
        
    def check_collisions(self):
        # Ground collision
        if self.position.y < 0:
            self.handle_collision()
            self.position.y = 0
            self.velocity.y = 0
            
        # Check for collisions with other entities
        hit_info = self.intersects()
        if hit_info.hit and time.time() - self.last_collision_time > self.collision_cooldown:
            self.handle_collision()
            self.last_collision_time = time.time()
            
    def handle_collision(self):
        # Apply damage
        self.health -= self.collision_damage
        
        # Reduce velocity on collision
        self.velocity *= 0.5
        
        # Check if drone is crashed
        if self.health <= 0:
            self.crash()
            
    def crash(self):
        self.is_crashed = True
        self.color = color.gray
        self.velocity = Vec3(0, 0, 0)
        self.rotation_velocity = Vec3(0, 0, 0)
        print("Drone crashed! Health depleted.")
            
    def apply_control(self, thrust, pitch, roll, yaw):
        if self.is_crashed:
            return
            
        self.thrust = thrust
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        
        # Convert control inputs to rotation velocity with increased sensitivity
        self.rotation_velocity = Vec3(
            pitch * 3,  # Reduced rotation speed
            yaw * 3,    # Reduced rotation speed
            roll * 3    # Reduced rotation speed
        ) 