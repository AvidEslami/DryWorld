import arcade
import arcade.camera
import numpy as np

# Window Constants
INITIAL_WIDTH = 1280
INITIAL_HEIGHT = 720
SCREEN_TITLE = "Display-Agnostic Aquarium Sim"

# Simulation Constants
NUM_CREATURES = 50
CREATURE_SPEED = 200.0

class AquariumSim(arcade.Window):
    def __init__(self):
        # resizable=True is critical for letting the user (or OS) change the window size
        super().__init__(INITIAL_WIDTH, INITIAL_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)
        
        # 1. Initialize the modern Camera2D
        self.camera = arcade.camera.Camera2D()
        
        # 2. Setup rendering
        self.creatures_list = arcade.SpriteList()
        
        # 3. Setup mathematical state (NumPy matrix for performance)
        # Columns: [x, y, velocity_x, velocity_y]
        self.state = np.zeros((NUM_CREATURES, 4), dtype=np.float64)
        
        # Populate the initial state and sprites
        for i in range(NUM_CREATURES):
            # Random starting positions within the initial window
            self.state[i, 0] = np.random.uniform(0, INITIAL_WIDTH)
            self.state[i, 1] = np.random.uniform(0, INITIAL_HEIGHT)
            
            # Random velocities
            angle = np.random.uniform(0, 2 * np.pi)
            self.state[i, 2] = np.cos(angle) * CREATURE_SPEED
            self.state[i, 3] = np.sin(angle) * CREATURE_SPEED
            
            # Create a sprite for each creature
            sprite = arcade.SpriteCircle(radius=8, color=arcade.color.CORAL)
            sprite.center_x = self.state[i, 0]
            sprite.center_y = self.state[i, 1]
            self.creatures_list.append(sprite)

    def on_resize(self, width: int, height: int):
        """
        Called automatically whenever the window is resized.
        """
        super().on_resize(width, height)
        
        # Match the camera viewport to the new physical window dimensions
        self.camera.match_window()

    def on_update(self, delta_time: float):
        """
        Vectorized simulation logic.
        """
        # 1. Update all positions at once using their velocity vectors
        self.state[:, 0] += self.state[:, 2] * delta_time
        self.state[:, 1] += self.state[:, 3] * delta_time

        # 2. Dynamic boundary collisions using current window dimensions (self.width, self.height)
        # X-axis bounds
        out_of_bounds_x_low = self.state[:, 0] <= 0
        out_of_bounds_x_high = self.state[:, 0] >= self.width
        
        # Reverse velocity and clamp position
        self.state[out_of_bounds_x_low, 2] *= -1
        self.state[out_of_bounds_x_low, 0] = 0
        
        self.state[out_of_bounds_x_high, 2] *= -1
        self.state[out_of_bounds_x_high, 0] = self.width

        # Y-axis bounds
        out_of_bounds_y_low = self.state[:, 1] <= 0
        out_of_bounds_y_high = self.state[:, 1] >= self.height
        
        # Reverse velocity and clamp position
        self.state[out_of_bounds_y_low, 3] *= -1
        self.state[out_of_bounds_y_low, 1] = 0
        
        self.state[out_of_bounds_y_high, 3] *= -1
        self.state[out_of_bounds_y_high, 1] = self.height

        # 3. Sync mathematical state to visual sprites
        for i, sprite in enumerate(self.creatures_list):
            sprite.center_x = self.state[i, 0]
            sprite.center_y = self.state[i, 1]

    def on_draw(self):
        """
        Render the frame.
        """
        self.clear()
        
        # Activate the camera's coordinate system
        with self.camera.activate():
            self.creatures_list.draw()

if __name__ == "__main__":
    sim = AquariumSim()
    arcade.run()