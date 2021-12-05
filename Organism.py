import random

org_compendium = []
food_compendium = []


def output_org_list():
    for org in org_compendium:
        org.to_string()


def output_food_list():
    for food in food_compendium:
        food.to_string()


def create_genome():
    genome = []
    for i in range(3):
        genome.append(random.choice(['A', 'B']))
        genome.append(random.choice(['A', 'B']))
        genome.append(random.choice(['A', 'B']))
    return genome


def genome_interpreter(genome):
    pass


def reproduce(mom1, mom2):
    if mom1 != mom2:
        child = birth(mom1.get_genome, mom2.get_genome)
        if child:
            child.set_position(mom1.get_position)


def birth(p1_genome, p2_genome):
    is_viable = random.randint(1, 40)
    if is_viable > 25:
        baby = Organism(p1_genome * .5, p2_genome * .5)
        return baby
    else:
        return None


def hunt(predator, prey):
    print()
    if prey.get_health() / 2 >= 120 - predator.get_health():
        predator.set_health(predator.get_health() + int(prey.health / 3))
    else:
        predator.set_health(predator.get_health() + int(prey.get_health() / 2))
    print(f'{prey.get_id()} death!\n')
    prey.death()


def consume(org, food):
    if food.edible and not org.is_carnivore():  # increments health due to eating food
        org.health += food.value
    elif org.is_carnivore() and type(Organism):
        hunt(org, food)
    else:  # decrements health due to eating inedible food
        org.health -= food.value


def is_occupied(check_pos):
    for org in org_compendium:
        if check_pos == org.get_position():
            return True
    for food in food_compendium:
        if check_pos == food.get_position():
            return True
    return False


def get_at_pos(position):
    for org in org_compendium:
        if position == org.get_position():
            return org
    for food in food_compendium:
        if position == food.get_position():
            return food
    return None


class Organism:

    def __init__(self, org_pos, genome=create_genome()):
        self.position = org_pos
        self.genome = genome
        self.speed = 1
        self.id = len(org_compendium)
        org_compendium.insert(self.id, self)
        self.health = 25
        self.attack = 5
        self.carnivore = False

    def death(self):
        org_compendium.remove(self)

    def to_string(self):
        print('Health: {}\nId: {}\nPosition: {}\n'
              .format(self.health, self.id, self.position))

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position

    def move(self, direction=1):
        destination = direction * self.speed
        if not is_occupied(destination):
            self.position += destination
        elif is_occupied(destination) and self.is_carnivore() and get_at_pos(destination) is (Herbivore or Carnivore):
            self.position += destination
            hunt(self, get_at_pos(destination))
        elif is_occupied(destination) and not self.is_carnivore() and get_at_pos(destination) is Food:
            self.position += destination
            consume(self, get_at_pos(destination))

    def get_genome(self):
        return self.genome

    def get_speed(self):
        return self.speed

    def get_id(self):
        return self.id

    def get_health(self):
        return self.health

    def set_health(self, health_change):
        self.health += health_change

    def get_attack(self):
        return self.attack

    def hit(self, target):
        target.health -= self.get_attack()

    def is_carnivore(self):
        return self.carnivore


class Herbivore(Organism):

    def __init__(self, org_pos, genome):
        Organism.__init__(self, org_pos, genome)
        self.carnivore = False


class Carnivore(Organism):

    def __init__(self, org_pos, genome):
        Organism.__init__(self, org_pos, genome)
        self.carnivore = True


# insert 'grow' food function here


class Food:

    def __init__(self, food_pos):
        self.position = food_pos
        self.id = len(food_compendium)
        food_compendium.insert(self.id, self)
        self.value = 0
        self.edible = True

    def get_pos(self):
        return self.position

    def is_edible(self):
        return self.edible

    def get_value(self):
        return self.value

    def consumed(self):
        food_compendium.remove(self)


class Strawberry(Food):

    def __init__(self, food_pos):
        Food.__init__(self, food_pos)
        self.value = 15
        self.edible = True


class Trash(Food):

    def __init__(self, food_pos):
        Food.__init__(self, food_pos)
        self.value = -5
        self.edible = False


class Environment:

    def __init__(self, env_len):
        self.length = env_len
        self.display = [0] * env_len

    def set_length(self, new_len):
        self.length = new_len

    def get_env(self):
        print(self.display)
