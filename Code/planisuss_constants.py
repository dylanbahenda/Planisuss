# planisuss_constants.py
"""
Collection of the main constants defined for the 
"Planisuss" project.

Values can be modified according to the envisioned behavior of the 
simulated world.

---
v 1.00
Stefano Ferrari
2023-02-07
"""

# Game constants

NUMDAYS: int = 100        # Length of the simulation in days

# geometry
NUMCELLS = 20        # size of the (square) grid (NUMCELLS x NUMCELLS)
NUMCELLS_R = 1000    # number of rows of the (potentially non-square) grid
NUMCELLS_C = 1000    # number of columns of the (potentially non-square) grid
GRID_SIZE = NUMCELLS * NUMCELLS

# social groups
NEIGHBORHOOD = 1     # radius of the region that a social group can evaluate to decide the movement
NEIGHBORHOOD_E = 1   # radius of the region that a herd can evaluate to decide the movement
NEIGHBORHOOD_C = 1   # radius of the region that a pride can evaluate to decide the movement

MAX_HERD = 50        # maximum numerosity of a herd
MAX_PRIDE = 30       # maximum numerosity of a pride

# individuals
MAX_ENERGY = 100     # maximum value of Energy
MAX_ENERGY_E = 100   # maximum value of Energy for Erbast
MAX_ENERGY_C = 100   # maximum value of Energy for Carviz

MAX_LIFE = 10000     # maximum value of Lifetime
MAX_LIFE_E = 60     # maximum value of Lifetime for Erbast
MAX_LIFE_C = 60     # maximum value of Lifetime for Carviz

AGING = 1            # energy lost each month
AGING_E = 1          # energy lost each month for Erbast
AGING_C = 1         # energy lost each month for Carviz

GROWING = 1          # Vegetob density that grows per day.
