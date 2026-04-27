import arcade
import numpy as np

# Grab full screen dimensions from system
SCREEN_WIDTH = arcade.get_display_size()[0]
SCREEN_HEIGHT = arcade.get_display_size()[1]

def fitness_function(state):
    # print(state)
    # return state[0] + state[1]  # Expriment: fitness is just the sum of x and y coordinates
    # return -((state[0]-100)**2 + (state[1]-100)**2)  # Experiment: fitness is how close the cell is to (100, 100)
    return -((state[0]-1820)**2 + (state[1]-980)**2)  # Experiment: fitness is how close the cell is to (1000, 100)


class ConvergenceExperiment(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Convergence Experiment", resizable=False, style="borderless")
        arcade.set_background_color(arcade.color.BLACK)
        self.cell = arcade.SpriteCircle(radius=20, color=arcade.color.GREEN)
        self.cell.center_x = SCREEN_WIDTH // 2
        self.cell.center_y = SCREEN_HEIGHT // 2



    def on_update(self, delta_time: float):
        # Every 2 seconds, the cell creates a new cell in every direction, +x, -x, +y, -y
        # Then run fitness function on each cell, and keep the one with highest fitness as self.cell
        new_cell_candidates = []
        parent_pos = (self.cell.center_x, self.cell.center_y)
        dirs = [(0,1), (0,-1), (1,0), (-1,0)]
        for dx, dy in dirs:
            new_cell_candidates.append((parent_pos[0]+dx, parent_pos[1]+dy))

        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.cell)

        for candidate in new_cell_candidates:
            fitness = fitness_function(candidate)
            if fitness > fitness_function((self.cell.center_x, self.cell.center_y)):
                self.cell.center_x, self.cell.center_y = candidate

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()



if __name__ == "__main__":
    window = ConvergenceExperiment()
    arcade.run()