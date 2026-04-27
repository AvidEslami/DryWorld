import arcade
import numpy as np
import random

SCREEN_WIDTH = arcade.get_display_size()[0]
SCREEN_HEIGHT = arcade.get_display_size()[1]

CREATURE_COUNT = 500
TARGET_FPS = 60
FULL_COLOR_LIST = []
for r in range(0, 256, 8):
    for g in range(0, 256, 8):
        for b in range(0, 256, 8):
            FULL_COLOR_LIST.append((r, g, b))
print(f"Generated {len(FULL_COLOR_LIST)} colors for rendering.")


def generate_tile_maze(width, height):
    # Maze dimensions MUST be odd numbers (e.g., 21x21) to ensure 
    # walls and paths alternate correctly and don't overlap edges.
    width = width if width % 2 != 0 else width + 1
    height = height if height % 2 != 0 else height + 1

    # 1. Start with a solid block of walls (1s)
    maze = np.ones((height, width), dtype=int)

    def carve_path(r, c):
        maze[r, c] = 0  # Mark current cell as a path (0)
        
        # Define the 4 directions. We jump TWO spaces at a time so we leave walls between paths.
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions) # Pick a random direction to dig
        
        for dr, dc in directions:
            next_r, next_c = r + dr, c + dc
            
            # Check if the next cell is inside the grid and is currently a wall
            if 0 < next_r < height-1 and 0 < next_c < width-1 and maze[next_r, next_c] == 1:
                # Knock down the wall in between us and the target
                maze[r + dr//2, c + dc//2] = 0
                # Jump to the target and repeat!
                carve_path(next_r, next_c)

    # Start digging at coordinates (1, 1)
    carve_path(1, 1)
    
    return maze

class EntitySimulation:
    def __init__(self, num_creatures = 0):
        # Initialize your simulation state here
        self.creature_list = []
        for _ in range(num_creatures):
            creature = {
                "position": (np.random.uniform(0, SCREEN_WIDTH), np.random.uniform(0, SCREEN_HEIGHT)),
                "velocity": (np.random.choice([-1, 1]), np.random.choice([-1, 1]))
            }
            self.creature_list.append(creature)

        
        self.maze = generate_tile_maze(60, 30)  # Generate a 21x21 maze



    def update(self, delta_time: float):
        # Update your simulation state here
        for creature in self.creature_list:
            # Simple movement logic: move according to velocity
            new_x = creature["position"][0] + creature["velocity"][0]
            new_y = creature["position"][1] + creature["velocity"][1]
            
            # Keep creatures within bounds of the screen
            new_x = max(0, min(SCREEN_WIDTH, new_x))
            new_y = max(0, min(SCREEN_HEIGHT, new_y))
            
            creature["position"] = (new_x, new_y)

class EntityRenderer:
    def __init__(self, num_creatures = 0):
        self.sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        for _ in range(num_creatures):
            sprite = arcade.SpriteCircle(radius=8, color=random.choice(FULL_COLOR_LIST))
            self.sprite_list.append(sprite)

    def draw(self, EntitySimulator):
        # Clear the sprite list
        # self.sprite_list.clear()
        for sprite, creature in zip(self.sprite_list, EntitySimulator.creature_list):
            sprite.center_x, sprite.center_y = creature["position"]

        self.sprite_list.draw()

        # Draw maze walls
        maze = EntitySimulator.maze
        for row in range(maze.shape[0]):
            for col in range(maze.shape[1]):
                
                # If it's a 1, it's a wall. Create a sprite!
                if maze[row, col] == 1:
                    wall_sprite = arcade.SpriteSolidColor(30, 30, arcade.color.SLATE_GRAY)
                    
                    # Calculate its X, Y coordinates
                    wall_sprite.center_x = col * 30 + (30 / 2)
                    wall_sprite.center_y = row * 30 + (30 / 2)
                    
                    self.wall_list.append(wall_sprite)
        self.wall_list.draw()

class DryWorldOrchestrator(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "DryWorld", resizable=False, 
                        #  style="borderless",
                        fullscreen=True, 
                        update_rate=1/TARGET_FPS, 
                        draw_rate=1/TARGET_FPS)
        arcade.set_background_color(arcade.color.BLACK)
        

        self.simulation = EntitySimulation(num_creatures=CREATURE_COUNT)
        self.renderer = EntityRenderer(num_creatures=CREATURE_COUNT)

    def on_update(self, delta_time: float):
        self.simulation.update(delta_time)

    def on_draw(self):
        self.clear()
        self.renderer.draw(self.simulation)

if __name__ == "__main__":
    window = DryWorldOrchestrator()
    arcade.run()