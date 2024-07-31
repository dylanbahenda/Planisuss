'''

Ntegano Bahenda Yvon Dylan - 515657
Pietrasanta Sebastiano - 513054

'''


import random

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button
import planisuss_constants as const


class Cell:
    """
    Class representing a cell in the world.

    Attributes:
    - coords: Coordinates of the cell.
    - is_water: Indicates if the cell is a water cell.
    - vegetob_density: Density of vegetation in the cell.
    - erbasts: List of Erbast instances in the cell.
    - carvizes: List of Carviz instances in the cell.
    """

    def __init__(self, coords, is_water=False):
        """
        Initialize a Cell instance.

        Parameters:
        - coords: Coordinates of the cell.
        - is_water: Indicates if the cell is a water cell (default is False).
        """
        self.coords = coords
        self.is_water = is_water
        self.vegetob_density = 0
        self.erbasts = []
        self.carvizes = []

    def grow(self):
        """
        Simulate the growth of vegetation in the cell.
        """
        if not self.is_water and self.vegetob_density < 100:
            self.vegetob_density += const.GROWING

    def move_erbast(self, destination):
        """
        Move Erbast from this cell to the specified destination cell based on social group decisions.

        Parameters:
        - destination: The target cell to move Erbast to.
        """
        erb_move_decision = random.random() < 0.5

        for erbast in self.erbasts:
            erbast_decision = erbast.social_attitude > 0.1
            final_erb_decision = erb_move_decision and erbast_decision

            if final_erb_decision and len(destination.erbasts) < const.MAX_HERD:
                erbast.energy -= 7
                destination.erbasts.append(erbast)
                self.erbasts.remove(erbast)

    def move_carviz(self, destination):
        """
        Move Carviz from this cell to the specified destination cell based on social group decisions.

        Parameters:
        - destination: The target cell to move Carviz to.
        """
        car_move_decision = random.random() < 0.5

        for carviz in self.carvizes:
            carviz_decision = carviz.social_attitude > 0.2
            final_car_decision = car_move_decision and carviz_decision

            if final_car_decision:
                carviz.energy -= 5
                destination.carvizes.append(carviz)
                self.carvizes.remove(carviz)

        if len(destination.carvizes) > const.MAX_PRIDE:
            prides = []
            current_pride = []

            for carviz in destination.carvizes:
                if carviz.social_attitude > 0.2:
                    current_pride.append(carviz)
                else:
                    if current_pride:
                        prides.append(current_pride)
                    current_pride = [carviz]

            if current_pride:
                prides.append(current_pride)

            while len(prides) > 1:
                pride1 = prides.pop(0)
                pride2 = prides.pop(0)
                winner_pride = fight(pride1, pride2)
                prides.insert(0, winner_pride)

            destination.carvizes = prides[0]


    def graze(self):
        """
        Simulate the grazing behavior of Erbast in the cell.
        """
        sorted_list = sorted((erbast for erbast in self.erbasts if erbast.energy < 100), key=lambda x: x.energy)

        if self.vegetob_density < len(sorted_list):
            for i in range(self.vegetob_density):
                sorted_list[i].energy += 1
            new_list = sorted_list[self.vegetob_density:]
            for erbast in new_list:
                erbast.social_attitude -= 0.05
            self.vegetob_density = 0
        else:
            for erbast in self.erbasts:
                erbast.energy += 1
                self.vegetob_density -= 1
            if self.vegetob_density > 0:
                self.graze()

    def hunt(self):
        """
        Simulate the hunt behavior of Carviz in the cell.
        """
        strongest_erbast = max(self.erbasts, key=lambda erbast: erbast.energy)
        hunt_success = random.random() < 0.3
        if hunt_success:
            prey_energy = strongest_erbast.energy
            lowest_energy_carviz = min(self.carvizes, key=lambda carviz: carviz.energy)
            for carviz in self.carvizes:
                carviz.energy += prey_energy // len(self.carvizes)
                if carviz == lowest_energy_carviz:
                    carviz.energy += prey_energy % len(self.carvizes)
                carviz.social_attitude += 0.05
            self.erbasts.remove(strongest_erbast)
            for erbast in self.erbasts:
                erbast.social_attitude += 0.05
        else:
            for carviz in self.carvizes:
                carviz.social_attitude -= 0.05

    def spawn(self):
        """
        Simulate the spawning and aging of Erbast and Carviz in the cell.
        """
        for erbast in self.erbasts:
            erbast.age += 1
            if erbast.energy <= 0:
                self.erbasts.remove(erbast)
            if erbast.age % 10 == 0:
                erbast.energy -= const.AGING_E
            if erbast.age >= erbast.lifetime and len(self.erbasts) + 1 < const.MAX_HERD:
                if len(self.erbasts) + 1 < const.MAX_HERD:
                    self.erbasts.append(Erbast(erbast.energy // 2, erbast.social_attitude))
                    self.erbasts.append(Erbast(erbast.energy // 2, erbast.social_attitude))
                self.erbasts.remove(erbast)

        for carviz in self.carvizes:
            carviz.age += 1
            if carviz.energy <= 0:
                self.carvizes.remove(carviz)
            if carviz.age % 10 == 0:
                carviz.energy -= const.AGING_C
            if carviz.age >= carviz.lifetime:
                if len(self.carvizes) + 1 < const.MAX_HERD and len(self.carvizes) + 1 < const.MAX_PRIDE:
                    self.carvizes.append(Carviz(carviz.energy // 2, carviz.social_attitude))
                    self.carvizes.append(Carviz(carviz.energy // 2, carviz.social_attitude))
                self.carvizes.remove(carviz)


class Erbast:
    """
    Class representing Erbast entities.

    Attributes:
    - energy: Represents the energy level of an Erbast instance.
    - lifetime: Represents the maximum lifetime of an Erbast instance.
    - age: Represents the current age of an Erbast instance.
    - social_attitude: Represents the social attitude of an Erbast instance,
                       initialized with a default value obtained from random.random().
    """

    def __init__(self, energy, attitude=random.random()):
        """
        Initialize an Erbast instance with the given energy and optional attitude.

        Parameters:
        - energy: The energy level of the Erbast instance.
        - attitude: The social attitude of the Erbast instance (default is a random value).
        """
        self.energy = energy
        self.lifetime = const.MAX_LIFE_E
        self.age = 0
        self.social_attitude = attitude


class Carviz:
    """
    Class representing Carviz entities.

    Attributes:
    - energy: Represents the energy level of a Carviz instance.
    - lifetime: Represents the maximum lifetime of a Carviz instance.
    - age: Represents the current age of a Carviz instance.
    - social_attitude: Represents the social attitude of a Carviz instance,
                       initialized with a default value obtained from random.random().
    """

    def __init__(self, energy, attitude=random.random()):
        """
        Initialize a Carviz instance with the given energy and optional attitude.

        Parameters:
        - energy: The energy level of the Carviz instance.
        - attitude: The social attitude of the Carviz instance (default is a random value).
        """
        self.energy = energy
        self.lifetime = const.MAX_LIFE_C
        self.age = 0
        self.social_attitude = attitude


def fight(pride1, pride2):
    """
    Simulate the fighting behavior of Carviz in the cell.
    Args:
        - pride1: List of Carviz instances in the first pride.
        - pride2: List of Carviz instances in the second pride.

    Returns:
        - winner_pride: List of Carviz instances representing the winning pride.
    """
    total_energy_pride1 = sum(carviz.energy for carviz in pride1)
    total_energy_pride2 = sum(carviz.energy for carviz in pride2)

    total_energy = total_energy_pride1 + total_energy_pride2
    win_prob_pride1 = total_energy_pride1 / total_energy if total_energy != 0 else 0.5

    if random.random() < win_prob_pride1:
        winner_pride = pride1
    else:
        winner_pride = pride2

    for carviz in winner_pride:
        carviz.social_attitude += 0.05

    return winner_pride


def Create_world():
    """
    Create a world of cells.

    The function iterates through each cell in the world, initializes it,
    and marks cells as water based on certain conditions.

    Conditions for marking a cell as water:
    - Cells at the edges of the world are marked as water.
    - A cell has a 5% chance of being marked as water.

    Returns:
    - world: A 2D array representing the world of cells.
    """
    world = [[(i, j) for i in range(const.NUMCELLS)] for j in range(const.NUMCELLS)]

    for i in range(const.NUMCELLS):
        for j in range(const.NUMCELLS):
            # Initialize a Cell at coordinates (i, j)
            world[i][j] = Cell((i, j))

            # Mark cells as water based on conditions
            if i == 0 or j == 0 or i == const.NUMCELLS - 1 or j == const.NUMCELLS - 1 or random.random() < 0.05:
                world[i][j].is_water = True

    return world


def Initialize_world():
    """
    Initialize the world with Vegetob, Erbast, and Carviz populations.

    The function iterates through each cell in the world and initializes:
    - Vegetob density for non-water cells.
    - Erbast population with a 40% chance, generating between 1 and 30 Erbast.
    - Carviz population with a 10% chance, generating between 1 and 20 Carviz.

    Returns:
    - world: A 2D array representing the world of cells.
    """
    for row in range(const.NUMCELLS):
        for col in range(const.NUMCELLS):
            if not world[row][col].is_water:
                world[row][col].vegetob_density = random.randint(30, 100)
                if random.random() < 0.4:  # 40% chance of Erbast
                    for _ in range(random.randint(1, 30)):
                        world[row][col].erbasts.append(Erbast(energy=random.randint(50, 80)))
                if random.random() < 0.1:  # 10% chance of Carviz
                    for _ in range(random.randint(1, 20)):
                        world[row][col].carvizes.append(Carviz(energy=random.randint(50, 80)))


world = Create_world()

Initialize_world()

print(world[5][5].erbasts)

for i in range(const.NUMCELLS):
    for j in range(const.NUMCELLS):
        print(world[i][j].vegetob_density, end=" ")
    print()


def get_neighborhood_cells(cell):
    """
    Get the cells in the neighborhood of the given cell.
    Args:
        - cell: object of class Cell
            representing the cell for which the neighborhood is to be found.

    Returns:
        - list of objects of class Cell
            representing the cells in the neighborhood of the given cell.
    """
    adjacent_non_water_cells = []

    for i in range(-const.NEIGHBORHOOD, const.NEIGHBORHOOD + 1):
        for j in range(-const.NEIGHBORHOOD, const.NEIGHBORHOOD + 1):
            if i == 0 and j == 0:
                continue  # Skip the current cell
            neighbor_coords = (cell.coords[0] + i, cell.coords[1] + j)
            neighbor_cell = world[neighbor_coords[0]][neighbor_coords[1]]
            if neighbor_cell and not neighbor_cell.is_water:
                adjacent_non_water_cells.append(neighbor_cell)

    return adjacent_non_water_cells


for i in range(len(get_neighborhood_cells(world[5][5]))):
    print(get_neighborhood_cells(world[5][5])[i].coords)


def simulate_day():
    """
    Simulate one day of growth and movement.
    The function iterates through each cell in the world and performs the following actions:
    - Grow Vegetob.
    - Move Erbast.
    - Move Carviz.
    - Hunting btn Pride and Erbast.
    - Spawning new Erbast and Carviz.
    """
    for row in range(len(world)):
        for col in range(len(world[row])):
            current_cell = world[row][col]
            if not current_cell.is_water:
                neighbor_cells = get_neighborhood_cells(current_cell)

                # Grow Vegetob
                current_cell.grow()
                if all(neighbor_cell.vegetob_density > 100 for neighbor_cell in neighbor_cells):
                    current_cell.erbasts = []
                    current_cell.carvizes = []

                # Move Erbast
                if current_cell.erbasts:
                    poss_dest_cells = []
                    for neighbor_cell in neighbor_cells:
                        if len(neighbor_cell.erbasts) + len(neighbor_cell.carvizes) < const.MAX_HERD:
                            poss_dest_cells.append(neighbor_cell)
                    if poss_dest_cells:
                        dest_cell = random.choice(poss_dest_cells)
                        current_cell.move_erbast(dest_cell)

                # Move Carviz
                if current_cell.carvizes:
                    poss_dest_cells = []
                    for neighbor_cell in neighbor_cells:
                        if len(neighbor_cell.erbasts) + len(neighbor_cell.carvizes) < const.MAX_PRIDE:
                            poss_dest_cells.append(neighbor_cell)
                    if poss_dest_cells:
                        dest_cell = random.choice(poss_dest_cells)
                        current_cell.move_carviz(dest_cell)

                # Graze
                if current_cell.erbasts:
                    current_cell.graze()

                # Hunt
                if current_cell.carvizes and current_cell.erbasts:
                    current_cell.hunt()

                # Spawn
                if current_cell.erbasts or current_cell.carvizes:
                    current_cell.spawn()


# A function to get the vegetation map of the world.
def get_vegetation_map():
    """
    Get the vegetation map of the world.

    Returns:
        - vegetation_map: A 2D array representing the vegetation map of the world.
    """
    vegetation_map = np.zeros((const.NUMCELLS, const.NUMCELLS))

    for row in range(const.NUMCELLS):
        for col in range(const.NUMCELLS):
            if world[row][col].is_water:
                vegetation_map[row][col] = -1
            else:
                vegetation_map[row][col] = world[row][col].vegetob_density
    return vegetation_map


# Setting up the plot

fig = plt.figure(figsize=(10, 5))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 0.7], hspace=0.4, wspace=0.2)

# Axes
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

# Title of main window
fig.canvas.manager.set_window_title("Planisuss")

# Background color
fig.set_facecolor("#DBCCB1")
ax2.set_facecolor("#DBCCB1")

ax1.set_xticks([])  # Remove x-axis ticks for ax1
ax1.set_yticks([])  # Remove y-axis ticks for ax1

# Time text
time_text = ax1.text(0.99, 0.99, '', transform=ax1.transAxes, ha='right', va='top', fontsize=12)

# Custom colormap
cmap = plt.cm.get_cmap('Greens', 256)
new_cmap = cmap(np.linspace(0, 1, 256))
new_cmap[0] = np.array([173 / 255, 216 / 255, 230 / 255, 1])
new_cmap = plt.cm.colors.ListedColormap(new_cmap)

# Vegetation map plot
img = ax1.imshow(get_vegetation_map(), cmap=new_cmap, interpolation='nearest', vmin=-1, vmax=100)

# Lists to track the number of Erbast and Carviz
num_erbasts = []
num_carvizes = []


# Update function for the animation
def update(frame):
    """
    Update function for the animation.
    Args:
        - frame: The current frame number.

    Returns:
        - img: The updated vegetation map plot.
        - ax1: The updated Erbast and Carviz positions.
        - ax2: The updated population plot.
    """
    # Simulate one day of growth and movement
    simulate_day()
    img.set_data(get_vegetation_map())
    ax1.set_title('Planisuss!', style='normal')  # Map title

    # Update the time text
    time_text.set_text(f'Days: {frame}')

    # Plot Erbast and Carviz
    ax1.collections.clear()  # Clear the plot

    # Initialize lists for scatter plot
    erbast_x = []
    erbast_y = []
    erbast_sizes = []
    carviz_x = []
    carviz_y = []
    carviz_sizes = []

    erbast_count = 0
    carviz_count = 0

    for row in range(const.NUMCELLS):
        for col in range(const.NUMCELLS):
            erbast_num = len(world[row][col].erbasts)
            carviz_num = len(world[row][col].carvizes)

            if erbast_num > 0:
                erbast_x.append(col)
                erbast_y.append(row)
                erbast_sizes.append(erbast_num * 3)
                erbast_count += erbast_num

            if carviz_num > 0:
                carviz_x.append(col)
                carviz_y.append(row)
                carviz_sizes.append(carviz_num * 3)
                carviz_count += carviz_num

    # Plot Erbast positions with sizes
    ax1.scatter(erbast_x, erbast_y, s=erbast_sizes, color='darkgoldenrod', edgecolor='yellow', label='Erbast')
    # Plot Carviz positions with sizes
    ax1.scatter(carviz_x, carviz_y, s=carviz_sizes, color='darkred', edgecolor='red', label='Carviz')

    # Update population counts
    num_erbasts.append(erbast_count)
    num_carvizes.append(carviz_count)

    # Clear previous plots
    ax2.clear()

    # Plot the population counts
    ax2.plot(num_erbasts, color='darkgoldenrod', label='Erbast')
    ax2.plot(num_carvizes, color='darkred', label='Carviz')

    # Set title and labels
    ax2.set_title('Population', style='normal')
    ax2.set_xlabel('Days')
    ax2.set_ylabel('Number')

    # Set x-axis and y-axis limits and ticks
    ax2.set_xlim(0, const.NUMDAYS)  # Adjust limits to fit your data
    ax2.set_ylim(0, 2200)
    ax2.set_xticks(np.arange(0, const.NUMDAYS + 10, 10))
    ax2.set_yticks(np.arange(0, 2200, 200))

    # Set the legend
    legend = ax2.legend(loc='upper right')
    legend.get_frame().set_facecolor('#DBCCB1')
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_linewidth(0.4)

    return img, ax1, ax2, time_text


speed = 200


# Button callback functions
def on_click_start(event):
    """
    Callback function for the start button.
    """
    ani.event_source.start()


def on_click_stop(event):
    """
    Callback function for the stop button.
    """
    ani.event_source.stop()


def decrease_speed():
    """
    Decrease the animation speed by 100 ms.
    """
    speed += 100


def on_click_slow_down(event):
    """
    Callback function for the slow-down button
    """
    decrease_speed()
    ani.event_source.stop()
    ani.event_source.interval = speed
    ani.event_source.start()


def increase_speed():
    """
    Increase the animation speed by 100 ms.
    """
    speed -= 100


def on_click_speed_up(event):
    """
    Callback function for the speed-up button.
    """
    increase_speed()
    ani.event_source.stop()
    ani.event_source.interval = speed
    ani.event_source.start()


# Create the buttons
ax_pause = fig.add_axes([0.15, 0.025, 0.08, 0.05])
ax_resume = fig.add_axes([0.24, 0.025, 0.08, 0.05])
ax_slow_down = fig.add_axes([0.35, 0.025, 0.08, 0.05])
ax_speed_up = fig.add_axes([0.44, 0.025, 0.08, 0.05])

pause_button = Button(ax_pause, 'Pause', color='#FBCCB1', hovercolor='#CC7722')
resume_button = Button(ax_resume, 'Resume', color='#ABCCB1', hovercolor='#CC7722')
slow_down_button = Button(ax_slow_down, 'Slow-down', color='#CCCCB1', hovercolor='#CC7722')
speed_up_button = Button(ax_speed_up, 'Speed-up', color='#CCCCB1', hovercolor='#CC7722')

pause_button.on_clicked(on_click_stop)
resume_button.on_clicked(on_click_start)
slow_down_button.on_clicked(on_click_slow_down)
speed_up_button.on_clicked(on_click_speed_up)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=const.NUMDAYS, interval=speed , blit=False, repeat=False)

# Show the animation
plt.show()