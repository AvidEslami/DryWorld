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


def terrain_generator(width, height, wall_count=3):
    # Create a 1920 x 1080 grid of 0s
    terrain = [[0] * 1080 for _ in range(1920)]
    for _ in range(wall_count):
        ran_y =  random.randint(0, 1079)
        for x in range(1920):
            terrain[x][ran_y] = 1
    for _ in range(wall_count):
        ran_x =  random.randint(0, 1919)
        for y in range(1080):
            terrain[ran_x][y] = 1
    return terrain

class EntitySimulation:
    def __init__(self, num_creatures = 0, generated_terrain = None):
        # Initialize your simulation state here
        self.creature_list = []
        for _ in range(num_creatures):
            creature = {
                "position": (np.random.uniform(0, SCREEN_WIDTH), np.random.uniform(0, SCREEN_HEIGHT)),
                "velocity": (np.random.choice([-1, 1]), np.random.choice([-1, 1]))
            }
            self.creature_list.append(creature)

        
        self.terrain = generated_terrain



    def update(self, delta_time: float):
        # Update your simulation state here
        for creature in self.creature_list:
            # Simple movement logic: move according to velocity
            new_x = creature["position"][0] + creature["velocity"][0]
            new_y = creature["position"][1] + creature["velocity"][1]
            

            # Keep creatures within bounds of the screen
            new_x = max(0, min(SCREEN_WIDTH-1, new_x))
            new_y = max(0, min(SCREEN_HEIGHT-1, new_y))
            
            # Check for collisions with terrain (walls)
            if self.terrain[int(new_x)][int(new_y)] == 1:
                # If there's a wall, reverse velocity
                creature["velocity"] = (-creature["velocity"][0], -creature["velocity"][1])
            else:
                # If no wall, update position
                creature["position"] = (new_x, new_y)

            creature["position"] = (new_x, new_y)

class EntityRenderer:
    def __init__(self, num_creatures = 0, generated_terrain = None):
        self.sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        for _ in range(num_creatures):
            sprite = arcade.SpriteCircle(radius=8, color=random.choice(FULL_COLOR_LIST))
            self.sprite_list.append(sprite)

        for row in range(len(generated_terrain[0])):
            for col in range(len(generated_terrain)):
                if generated_terrain[col][row] == 1:
                    wall_sprite = arcade.SpriteSolidColor(1, 1, arcade.color.WHITE)
                    wall_sprite.center_x = col
                    wall_sprite.center_y = row
                    self.wall_list.append(wall_sprite)

        # self.wall_list.draw()

    def draw(self, EntitySimulator):
        # Clear the sprite list
        # self.sprite_list.clear()
        for sprite, creature in zip(self.sprite_list, EntitySimulator.creature_list):
            sprite.center_x, sprite.center_y = creature["position"]

        self.sprite_list.draw()
        self.wall_list.draw()

class DryWorldOrchestrator(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "DryWorld", resizable=False, 
                        #  style="borderless",
                        fullscreen=True, 
                        update_rate=1/TARGET_FPS, 
                        draw_rate=1/TARGET_FPS)
        arcade.set_background_color(arcade.color.BLACK)
        
        self.terrain = terrain_generator(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.simulation = EntitySimulation(num_creatures=CREATURE_COUNT, generated_terrain=self.terrain)
        self.renderer = EntityRenderer(num_creatures=CREATURE_COUNT, generated_terrain=self.terrain)

    def on_update(self, delta_time: float):
        self.simulation.update(delta_time)

    def on_draw(self):
        self.clear()
        self.renderer.draw(self.simulation)

if __name__ == "__main__":
    window = DryWorldOrchestrator()
    arcade.run()