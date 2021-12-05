from Organism import *

land = Environment(6)

example_hostile_genome = ['AB', 'AB', 'AB', 'AB']
example_docile_genome = ['BA', 'BA', 'AB', 'BA']

for i in range(4):
    i = Organism(random.randint(0,5))
land.populate()
land.get_env()
pass_time(land, 5)
land.get_env()
