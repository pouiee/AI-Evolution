import random

org_compendium = []
food_compendium = []


def pass_time(land, turns):
    for org in org_compendium:
        org.move(land, random.randint(-1, 1))
        reproduce(land)
    if turns == 0:
        return
    land.get_env()
    pass_time(land, turns - 1)


def output_org_list():
    for org in org_compendium:
        org.to_string()


def output_food_list():
    for food in food_compendium:
        food.to_string()


def create_first_genome():
    genome = []
    for i in range(4):
        genome.append(random.choice(['AB', 'BA']))
    return genome


def interpret_genome(genome=create_first_genome()):
    traits = {}
    behavior_dict = {
        'AB': 'Hostile',
        'BA': 'Docile',
        'BB': 'Not Viable'
    }
    size_dict = {
        'AB': 'Large',
        'BA': 'Small',
        'BB': 'Not Viable'
    }
    agility_dict = {
        'AB': 'Fast',
        'BA': 'Small',
        'BB': 'Not Viable'
    }
    mutation_dict = {
        'AB': .2,
        'BA': .5,
        'BB': 'Not Viable'
    }
    traits['Behavior'] = behavior_dict.get(genome[0])
    traits['Size'] = size_dict.get(genome[1])
    traits['Agility'] = agility_dict.get(genome[2])
    traits['Mutation Chance'] = mutation_dict.get(genome[3])
    return traits


def mutate(genome):
    mutated_genome = []
    mutation_chance = interpret_genome(genome).get('Mutation Chance')
    for gene in range(len(genome) - 1):
        chance = random.uniform(0.0, mutation_chance)
        if chance < mutation_chance / 4:
            mutated_genome.append('BB')
        elif chance <= mutation_chance / 2:
            if genome == 'AB':
                mutated_genome.append('BA')
            else:
                mutated_genome.append('AB')
        else:
            mutated_genome.append(genome[gene])

    return genome


def inherit(p_1, p_2):
    new_genome = []
    for gene in range(len(p_1.get_genome())):
        if random.randint(0, 10) > 5:
            new_genome.append(p_1.get_genome()[gene])
        else:
            new_genome.append(p_2.get_genome()[gene])
    return mutate(new_genome)


def reproduce(land):
    for x in land.get_display():
        if len(x) == 2:
            Organism(x,
                     inherit(find_org(x[0]), find_org(x[1])))
        elif len(x) % 2 == 0:
            for i in range(len(x)):
                if i % 2 == 0:
                    continue
                Organism(2, inherit(find_org(i), find_org(x[i + 1])))
        elif len(x) > 2:
            for i in range(len(x)):
                if i % 2 != 0:
                    continue
                Organism(2, inherit(find_org(x[0]), find_org(x[1])))


def hunt(predator, prey):
    prey_value = prey.get_health()
    while predator.is_alive() and prey.is_alive():
        predator.hit(prey)
        if prey.is_alive():
            prey.hit(predator)
    if predator.is_alive():
        predator.set_health(prey_value)


def consume(org, food):
    if not org.is_hostile() and food in food_compendium:
        org.set_health(food.get_value())
        food.consumed()
    elif org.is_hostile() and not food.is_hostile():
        hunt(org, food)


def is_occupied(check_pos):
    for org in org_compendium:
        if check_pos == org.get_position():
            return True
    for food in food_compendium:
        if check_pos == food.get_position():
            return True
    return False


def find_org(org_id):
    for org in org_compendium:
        if org_id == org.get_id():
            return org


def get_at_pos(position):
    for org in org_compendium:
        if position == org.get_position():
            return org
    for food in food_compendium:
        if position == food.get_position():
            return food
    return None


def update_env(env, org_1, destination):
    env.add_obj(org_1, destination)


class Organism:

    def __init__(self, pos, genome=create_first_genome()):
        self.position = pos
        self.genome = genome
        self.id = len(org_compendium) + 1
        org_compendium.insert(self.id, self)
        self.features = interpret_genome(genome)
        self.initialize_traits()
        self.alive = True

    def to_string(self):
        print('Id: {} Health: {} Position: {} Genome: {}'
              .format(self.get_id(), self.get_health(), self.get_position(), self.get_genome()))

    def initialize_traits(self):
        self.initialize_health()
        self.initialize_attack()
        self.initialize_speed()
        self.initialize_behavior()

    def initialize_speed(self):
        if self.features['Agility'] == 'Fast':
            self.features['Speed'] = 2
        else:
            self.features['Speed'] = 1

    def get_speed(self):
        return self.features['Speed']

    def initialize_health(self):
        if self.features['Size'] == 'Large':
            self.features['Health'] = random.randint(75, 100)
        else:
            self.features['Health'] = random.randint(30, 55)

    def get_health(self):
        return self.features['Health']

    def initialize_attack(self):
        if self.features['Size'] == 'Large':
            self.features['Attack'] = random.randint(35, 60)
        else:
            self.features['Attack'] = random.randint(15, 25)

    def get_attack(self):
        return self.features['Attack']

    def initialize_behavior(self):
        if self.features['Behavior'] == 'Hostile':
            self.features['Hostile'] = True
        else:
            self.features['Hostile'] = False

    def is_hostile(self):
        return self.features['Hostile']

    def is_alive(self):
        return self.alive

    def death(self):
        self.alive = False
        self.to_string()
        print('Alas! Organism ' + str(self.get_id()) + ' has perished!')
        org_compendium.remove(self)

    def get_position(self):
        return self.position

    def set_position(self, new_position):
        self.position = new_position

    def move(self, env, direction=1):
        movement = self.get_position() + direction * self.get_speed()
        if self.get_position() + movement > env.get_len() or self.get_position() + movement < env.get_len():
            return
        if not is_occupied(movement):
            self.set_position(movement)
            env.modify_pos(self, movement)
        else:
            self.set_position(movement)
            env.modify_pos(self, movement)
            consume(self, get_at_pos(movement))

    def get_genome(self):
        return self.genome

    def get_id(self):
        return self.id

    def set_health(self, health_change):
        self.features['Health'] += health_change

    def hit(self, target):
        target.set_health(-1 * self.get_attack())
        if target.get_health() <= 0:
            target.death()


# insert 'grow' food function here


class Food:

    def __init__(self, food_pos):
        self.position = food_pos
        self.id = len(food_compendium)
        food_compendium.insert(self.id, self)
        self.value = random.randint(10, 15) * random.randint(-1, 1)

    def to_string(self):
        print('Id: {} Food Value: {} Position: {}\n'
              .format(self.get_id(), self.get_value(), self.get_position()))

    def get_position(self):
        return self.position

    def get_id(self):
        return self.id

    def get_value(self):
        return self.value

    def consumed(self):
        food_compendium.remove(self)


class Environment:

    def __init__(self, env_len):
        self.length = env_len
        self.display = [[] for n in range(env_len)]

    def get_len(self):
        return self.length

    def add_obj(self, obj):
        self.get_display()[obj.get_position()].append(obj.get_id())

    def modify_pos(self, obj, destination):
        self.get_display()[destination].append(obj.get_id())
        for org in org_compendium:
            if org.get_position() != destination and org.get_id() == obj.get_id():
                del org
                break

    def get_display(self):
        return self.display

    def get_env(self):
        print(self.display)

    def populate(self):
        for org in org_compendium:
            self.add_obj(org)
        for food in food_compendium:
            self.add_obj(food)
        self.get_env()
