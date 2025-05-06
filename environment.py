from ursina import *
from ursina.shaders import lit_with_shadows_shader
import random
from PIL import Image
import numpy as np

class Environment:
    def __init__(self):
        # Create basic building textures
        self.create_building_textures()
        
        # Create ground
        self.ground = Entity(
            model='plane',
            scale=(100, 1, 100),
            color=color.green,
            texture='white_cube',
            texture_scale=(100, 100),
            collider='box'
        )
        
        # Create sky
        Sky()
        
        # Add lighting
        self.sun = DirectionalLight(
            y=2,
            z=3,
            shadows=True,
            rotation=(45, -45, 0)
        )
        
        # Create buildings and bridges
        self.buildings = []
        self.create_buildings()
        self.create_bridges()
        
    def create_building_textures(self):
        # Create a basic building wall texture
        size = 128
        img = Image.new('RGBA', (size, size), (200, 200, 200, 255))
        pixels = img.load()
        
        # Draw windows
        window_size = size // 8
        for x in range(0, size, window_size * 2):
            for y in range(0, size, window_size * 2):
                # Draw window
                for wx in range(window_size):
                    for wy in range(window_size):
                        if wx == 0 or wy == 0 or wx == window_size-1 or wy == window_size-1:
                            pixels[x + wx, y + wy] = (100, 100, 100, 255)  # Window frame
                        else:
                            pixels[x + wx, y + wy] = (150, 200, 255, 255)  # Window glass
        
        # Save the texture
        img.save('building_texture.png')
        
    def create_buildings(self):
        # Create a grid of buildings
        building_positions = []
        for x in range(-40, 41, 20):  # Spacing buildings 20 units apart
            for z in range(-40, 41, 20):
                if random.random() < 0.7:  # 70% chance to place a building
                    height = random.uniform(15, 30)  # Taller buildings
                    
                    # Create building with texture
                    building = Entity(
                        model='cube',
                        color=color.gray,
                        position=(x, height/2, z),  # Position at half height
                        scale=(
                            random.uniform(4, 6),
                            height,
                            random.uniform(4, 6)
                        ),
                        collider='box',
                        texture='building_texture.png',
                        texture_scale=(4, 4),  # Repeat texture 4 times
                    )
                    
                    self.buildings.append(building)
                    building_positions.append((x, z))
        return building_positions
        
    def create_bridges(self):
        # Create bridges between nearby buildings
        for i, building1 in enumerate(self.buildings):
            for building2 in self.buildings[i+1:]:
                # Calculate distance between buildings
                distance = (building1.position - building2.position).length()
                
                # Create bridge if buildings are close enough
                if 20 < distance < 30:  # Bridge length between 20 and 30 units
                    # Calculate bridge position and rotation
                    mid_point = (building1.position + building2.position) / 2
                    direction = (building2.position - building1.position).normalized()
                    
                    # Calculate bridge length and height
                    bridge_length = distance
                    bridge_height = max(building1.position.y, building2.position.y) + 5  # 5 units above the higher building
                    
                    # Create bridge
                    bridge = Entity(
                        model='cube',
                        color=color.light_gray,
                        position=mid_point,
                        scale=(2, 1, bridge_length),  # Thin bridge
                        collider='box',
                        texture='white_cube',  # Basic texture for bridge
                    )
                    
                    # Rotate bridge to connect buildings
                    bridge.look_at(building2)
                    bridge.rotation_x = 90  # Make bridge horizontal
                    
                    # Add bridge supports
                    support_height = bridge_height - 5
                    for x in [-bridge_length/4, bridge_length/4]:
                        support_pos = mid_point + Vec3(x, -support_height/2, 0)
                        support = Entity(
                            model='cylinder',
                            color=color.gray,
                            position=support_pos,
                            scale=(1, support_height, 1),
                            collider='box',
                            texture='white_cube',  # Basic texture for supports
                        )
                        support.look_at(building2)
            
    def update(self):
        # Update environment elements here
        pass 